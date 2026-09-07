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
    training_data, validation_data, testing_data = split(dataset["close"])
    return dataset, training_data, validation_data, testing_data

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

def grid_search(train_data, d, max_pq, criterion):
    best_p, best_q = 0, 0
    best_score = float('inf')
    for i in range(max_pq):
        for j in range(max_pq):
            try:
                model = SARIMAX(train_data, order = (i, d, j), enforce_stationarity = False, enforce_invertibility = False)
                fitted = model.fit(disp = False)
                score = fitted.aic if criterion == "AIC" else fitted.bic
                if score < best_score:
                    best_score = score
                    best_p, best_q = i, j
            except Exception:
                continue
    return best_p, best_q

def run_config(config, tickers, processed_dataset_path):
    config_results = []
    for ticker in tickers:
        dataset, training_data, validation_data, testing_data = load_data(ticker, processed_dataset_path)

        d = find_d(training_data)
        p, q = grid_search(training_data, d, config["max_pq"], config["criterion"])

        history = list(training_data.values) + list(validation_data.values)
        prediction = []
        for i in range(len(testing_data)):
            model = SARIMAX(history, order = (p, d, q), enforce_stationarity = False, enforce_invertibility = False)
            fitted = model.fit(disp = False)
            prediction.append(fitted.forecast(steps = 1)[0])
            history.append(testing_data.iloc[i])

        predictions = np.array(prediction)
        actuals = testing_data.values
        mae, mse, rmse, mape = evaluate(predictions, actuals)

        config_results.append({
            "config": config["name"],
            "criterion": config["criterion"],
            "range": f"0-{config['max_pq'] - 1}",
            "ticker": ticker.replace(".csv", ""),
            "order": f"({p},{d},{q})",
            "MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE": mape,
        })
    return config_results


def plot_comparison(df, output_path):
    metrics = ["MAE", "MSE", "RMSE", "MAPE"]

    fig, axes = plt.subplots(2, 2, figsize = (14, 10), constrained_layout = True)
    fig.suptitle("ARIMA Tuning - Average Metrics per Configuration", fontsize = 14)

    for ax, metric in zip(axes.flat, metrics):
        avg = df.groupby("config")[metric].mean().reset_index()

        ax.bar(avg["config"], avg[metric], color="steelblue")
        ax.set_title(f"Average {metric} per Configuration")
        ax.set_xlabel("Configuration")
        ax.set_ylabel(f"Average {metric}" + (" (%)" if metric == "MAPE" else ""))
        ax.tick_params(axis = "x", rotation = 45)
        ax.grid(True, axis = "y", alpha = 0.3)

        for i, v in enumerate(avg[metric]):
            ax.text(i, v, f"{v:.2f}", ha = "center", va = "bottom", fontsize = 8)

    fig.savefig(output_path / "arima_tuning_comparison.png", dpi = 150)
    plt.close()


def arima_tuning():
    # 6 configurations = 2 information criteria x 3 ranges
    configs = [
        {"name": "AIC_0-3", "criterion": "AIC", "max_pq": 4},
        {"name": "AIC_0-5", "criterion": "AIC", "max_pq": 6},
        {"name": "AIC_0-9", "criterion": "AIC", "max_pq": 10},
        {"name": "BIC_0-3", "criterion": "BIC", "max_pq": 4},
        {"name": "BIC_0-5", "criterion": "BIC", "max_pq": 6},
        {"name": "BIC_0-9", "criterion": "BIC", "max_pq": 10},
    ]

    tickers = []
    processed_dataset_path = Path(__file__).parent.parent.parent / "dataset" / "processed"
    list_ticker_name(tickers, processed_dataset_path)

    output_path = Path(__file__).parent / "results"
    output_path.mkdir(parents = True, exist_ok = True)

    all_results = []
    for config in configs:
        config_results = run_config(config, tickers, processed_dataset_path)
        all_results.extend(config_results)

        pd.DataFrame(all_results).to_csv(output_path / "arima_tuning.csv", index = False)

    df = pd.DataFrame(all_results)
    plot_comparison(df, output_path)

arima_tuning()