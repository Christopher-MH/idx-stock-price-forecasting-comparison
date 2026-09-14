import sys
from pathlib import Path
utils_path = Path(__file__).parent.parent.parent / "utils"
sys.path.append(str(utils_path))

from data_splitting import split
from evaluation import evaluate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

def list_ticker_name(tickers, processed_dataset_path):
    for f in Path(processed_dataset_path).glob("*.csv"):
        tickers.append(f.name)

def load_data(ticker, processed_dataset_path):
    dataset = pd.read_csv(processed_dataset_path / ticker, parse_dates=["time"], index_col="time")
    training_data, validation_data, testing_data = split(dataset[["open", "high", "low", "close", "Volume"]])
    return dataset, training_data, validation_data, testing_data

def minmax_scaling(training_data, validation_data, testing_data):
    scaler = MinMaxScaler()
    training_scaled = scaler.fit_transform(training_data)
    validation_scaled = scaler.transform(validation_data)
    testing_scaled = scaler.transform(testing_data)
    return training_scaled, validation_scaled, testing_scaled, scaler

def create_windows(dataset, window_size):
    X, y = [], []
    for i in range(len(dataset) - window_size):
        X.append(dataset[i : i + window_size])
        y.append(dataset[i + window_size, 3])
    return np.array(X), np.array(y)

def plot_results(dataset, ticker_name, testing_data, real_predictions, window_size):
    context_days = 30
    prediction_dates = testing_data.index
    recent_history = dataset["close"].iloc[-(len(testing_data) + context_days):]

    plt.figure(figsize = (14, 6), constrained_layout = True)
    plt.plot(recent_history.index, recent_history.values, label = "Actual", color = "black", linewidth = 1)
    plt.plot(prediction_dates, real_predictions, label = "Predicted", color = "red", linewidth = 1.5, linestyle = "--")
    plt.axvline(x = testing_data.index[0], color = "blue", linestyle = ":", alpha = 0.5, label = "Training cutoff")

    plt.title(f"LSTM - {ticker_name} Daily Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()

    plt.grid(True, alpha = 0.3)

    target_path = Path(__file__).parent.parent.parent / "results" / "plots" / "LSTM"
    plt.savefig(target_path / f"{ticker_name}.png", dpi = 150)
    plt.close()

def lstm():
    tickers = []
    results = []

    processed_dataset_path = Path(__file__).parent.parent.parent / "dataset" / "processed"
    list_ticker_name(tickers, processed_dataset_path)
    for ticker in tickers:
        dataset, training_data, validation_data, testing_data = load_data(ticker, processed_dataset_path)

        training_scaled, validation_scaled, testing_scaled, scaler = minmax_scaling(training_data, validation_data, testing_data)

        window_size = 30
        X_training, y_training = create_windows(training_scaled, window_size)
        X_validation, y_validation = create_windows(validation_scaled, window_size)

        bridge = np.concatenate([validation_scaled[-window_size:], testing_scaled])
        X_testing, y_testing = create_windows(bridge, window_size) 

        # Build
        model = Sequential()
        model.add(LSTM(128, return_sequences = True, input_shape = (window_size, 5)))
        model.add(Dropout(0.15))
        model.add(LSTM(128))
        model.add(Dropout(0.15))
        model.add(Dense(1))

        model.compile(optimizer = 'adam', loss = 'mse')

        # Train
        early_stop = EarlyStopping(monitor = 'val_loss', patience = 10, restore_best_weights = True)

        history = model.fit(
            X_training, y_training,
            validation_data = (X_validation, y_validation),
            epochs = 100,
            batch_size = 32,
            callbacks = [early_stop]
        )

        # with open('model.pkl', 'wb') as file:
        #     pickle.dump(model, file)

        # Test
        predictions = model.predict(X_testing)

        temp_prediction = np.zeros((len(predictions), 5)) # prediction dari LSTM
        temp_prediction[:, 3] = predictions[:, 0]
        real_predictions = scaler.inverse_transform(temp_prediction)[:, 3]

        temp_actual = np.zeros((len(y_testing), 5)) # actual dari Dataset
        temp_actual[:, 3] = y_testing
        real_actuals = scaler.inverse_transform(temp_actual)[:, 3]

        mae, mse, rmse, mape = evaluate(real_predictions, real_actuals)

        ticker_name = ticker.replace(".csv", "")
        results.append({
            "ticker": ticker_name,
            "model": "LSTM",
            "MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE": mape,
            "parameter": f"window = {window_size}, units = 128, layers = 2, dropout = 0.15",
        })

        plot_results(dataset, ticker_name, testing_data, real_predictions, window_size)

    target_path = Path(__file__).parent.parent.parent / "results"
    pd.DataFrame(results).to_csv(target_path / "LSTM_evaluation.csv", index = False)

lstm()