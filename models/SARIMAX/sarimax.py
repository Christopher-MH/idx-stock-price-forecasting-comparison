import sys
from pathlib import Path
utils_path = Path(__file__).parent.parent.parent / "utils"
sys.path.append(str(utils_path))

from data_splitting import split
from evaluation import evaluate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX

def list_ticker_name(tickers, processed_dataset_path):
    for f in Path(processed_dataset_path).glob("*.csv"):
        tickers.append(f.name)

def load_data(ticker, processed_dataset_path):
    dataset = pd.read_csv(processed_dataset_path / ticker, parse_dates = ["time"], index_col = "time")

    exog = dataset[["open", "high", "low", "Volume"]].shift(1).dropna()
    close = dataset["close"].loc[exog.index]

    training_close, validation_close, testing_close = split(close)
    training_exog, validation_exog, testing_exog = split(exog)

    return dataset, training_close, validation_close, testing_close, training_exog, validation_exog, testing_exog

def adf_test(time_series):
    result = adfuller(time_series)
    return result[1]

def find_d(time_series):
    d = 0
    current = time_series
    while True:
        p_value = adf_test(current)
        if p_value <= 0.05 or d >= 2:
            break

        current = current.diff().dropna()
        d += 1
    
    return d

def aic_grid_search(training_data, training_exog, d, m = 5, D = 0):
    best_pdq = (0, d, 0)
    best_seasonal = (0, D, 0, m)
    best_aic = float('inf')

    for p in range(3):
        for q in range(3):
            for P in range(3):
                for Q in range(3):
                    try:
                        model = SARIMAX(training_data, training_exog, order = (p, d, q), seasonal_order = (P, D, Q, m))
                        fitted = model.fit(disp = False)
                        if fitted.aic < best_aic:
                            best_aic = fitted.aic
                            best_pdq = (p, d, q)
                            best_seasonal = (P, D, Q, m)

                    except Exception as e:
                        continue

    return best_pdq, best_seasonal

def plot_results(dataset, ticker_name, testing_data, predictions, order, seasonal):
    context_days = 30
    recent_history = dataset["close"].iloc[-(len(testing_data) + context_days):]

    plt.figure(figsize = (14, 6), constrained_layout = True)
    plt.plot(recent_history.index, recent_history.values, label = "Actual", color = "black", linewidth = 1)
    plt.plot(testing_data.index, predictions, label = "Predicted", color = "red", linewidth = 1.5, linestyle = "--")
    plt.axvline(x = testing_data.index[0], color = "blue", linestyle = ":", alpha = 0.5, label = "Training cutoff")

    plt.title(f"SARIMAX{order}{seasonal} - {ticker_name} Daily Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()

    plt.grid(True, alpha = 0.3)

    target_path = Path(__file__).parent.parent.parent / "results" / "plots" / "SARIMAX"
    plt.savefig(target_path / f"{ticker_name}.png", dpi = 150)
    plt.close() 

def sarimax():
    tickers = []
    results = []

    processed_dataset_path = Path(__file__).parent.parent.parent / "dataset" / "processed"
    list_ticker_name(tickers, processed_dataset_path)
    for ticker in tickers:
        dataset, training_close, validation_close, testing_close, training_exog, validation_exog, testing_exog = load_data(ticker, processed_dataset_path)

        d = find_d(training_close)
        order, seasonal = aic_grid_search(training_close, training_exog, d)

        # Model
        history = list(training_close.values) + list(validation_close.values)
        exog_history = list(training_exog.values) + list(validation_exog.values)
        prediction = []

        for i in range(len(testing_close)):
            try:
                model = SARIMAX(history, exog = exog_history, order = order, seasonal_order = seasonal, enforce_stationarity = False, enforce_invertibility = False)
                fitted = model.fit(disp = False)
                current_exog = testing_exog.values[i].reshape(1, -1)
                yhat = fitted.forecast(steps = 1, exog = current_exog)
                prediction.append(yhat[0])
            except Exception:
                prediction.append(prediction[-1] if prediction else history[-1])

            history.append(testing_close.iloc[i])
            exog_history.append(testing_exog.values[i])

        # Evaluation
        predictions = np.array(prediction)
        actuals = testing_close.values
        mae, mse, rmse, mape = evaluate(predictions, actuals)

        ticker_name = ticker.replace(".csv", "")
        results.append({
            "ticker": ticker_name,
            "model": "sarimax",
            "MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE": mape,
            "parameter": f"{order}{seasonal}",
        })

        # Plot
        plot_results(dataset, ticker_name, testing_close, predictions, order, seasonal)

    target_path = Path(__file__).parent.parent.parent / "results"
    pd.DataFrame(results).to_csv(target_path / "SARIMAX_evaluation.csv", index = False)

sarimax()