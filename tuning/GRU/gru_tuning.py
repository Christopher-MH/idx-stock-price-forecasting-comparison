import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import tensorflow as tf
import random

SEED = 1
np.random.seed(SEED)
tf.random.set_seed(SEED)
random.seed(SEED)

from pathlib import Path
utils_path = Path(__file__).parent.parent.parent / "utils"
sys.path.append(str(utils_path))

from data_splitting import split
from evaluation import evaluate

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

def list_ticker_name(tickers, processed_dataset_path):
    for f in Path(processed_dataset_path).glob("*.csv"):
        tickers.append(f.name)

def load_data(ticker, processed_dataset_path):
    dataset = pd.read_csv(processed_dataset_path / ticker, parse_dates = ["time"], index_col = "time")
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

def build_model(window_size, units, layers, dropout):
    model = Sequential()
    for layer_idx in range(layers):
        return_seq = layer_idx < layers - 1
        if layer_idx == 0:
            model.add(GRU(units, return_sequences = return_seq, input_shape = (window_size, 5)))
        else:
            model.add(GRU(units, return_sequences = return_seq))
        model.add(Dropout(dropout))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss = 'mse')
    return model

def run_config(config, tickers, processed_dataset_path):
    window_size = config["window"]
    config_results = []

    for ticker in tickers:
        dataset, training_data, validation_data, testing_data = load_data(ticker, processed_dataset_path)

        training_scaled, validation_scaled, testing_scaled, scaler = minmax_scaling(training_data, validation_data, testing_data)

        X_training, y_training = create_windows(training_scaled, window_size)
        X_validation, y_validation = create_windows(validation_scaled, window_size)

        bridge = np.concatenate([validation_scaled[-window_size:], testing_scaled])
        X_testing, y_testing = create_windows(bridge, window_size)

        # Build
        model = build_model(window_size, config["units"], config["layers"], config["dropout"])

        # Train
        early_stop = EarlyStopping(monitor = 'val_loss', patience = 10, restore_best_weights = True)

        model.fit(
            X_training, y_training,
            validation_data = (X_validation, y_validation),
            epochs = 100,
            batch_size = 32,
            callbacks = [early_stop],
            verbose = 0
        )

        # Test
        predictions = model.predict(X_testing, verbose = 0)

        temp_prediction = np.zeros((len(predictions), 5)) # prediction dari GRU
        temp_prediction[:, 3] = predictions[:, 0]
        real_predictions = scaler.inverse_transform(temp_prediction)[:, 3]

        temp_actual = np.zeros((len(y_testing), 5)) # actual dari Dataset
        temp_actual[:, 3] = y_testing
        real_actuals = scaler.inverse_transform(temp_actual)[:, 3]

        mae, mse, rmse, mape = evaluate(real_predictions, real_actuals)

        config_results.append({
            "config": config["name"],
            "window": config["window"],
            "units": config["units"],
            "layers": config["layers"],
            "dropout": config["dropout"],
            "ticker": ticker.replace(".csv", ""),
            "MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE": mape,
        })
    return config_results

def plot_top(df_top, output_path):
    plt.figure(figsize = (12, 6), constrained_layout = True)
    plt.bar(df_top["config"], df_top["MAPE"], color = "steelblue")
    plt.title("GRU Tuning - Top 5 Configurations by Average MAPE")
    plt.xlabel("Configuration")
    plt.ylabel("Average MAPE (%)")
    plt.xticks(rotation = 45)
    plt.grid(True, axis = "y", alpha = 0.3)
    for i, v in enumerate(df_top["MAPE"]):
        plt.text(i, v, f"{v:.3f}", ha = "center", va = "bottom", fontsize = 9)
    plt.savefig(output_path / "gru_tuning_top5.png", dpi = 150)
    plt.close()

def gru_tuning():
    # full grid: 3 x 3 x 3 x 4 = 108 configurations
    windows = [20, 40, 60]
    units_list = [32, 64, 128]
    layers_list = [1, 2, 3]
    dropouts = [0.1, 0.2, 0.3, 0.4]

    configs = []
    counter = 1
    for w in windows:
        for u in units_list:
            for l in layers_list:
                for dr in dropouts:
                    configs.append({
                        "name": f"Combination_{counter:03d}",
                        "window": w, "units": u, "layers": l, "dropout": dr,
                    })
                    counter += 1

    tickers = []
    processed_dataset_path = Path(__file__).parent.parent.parent / "dataset" / "processed"
    list_ticker_name(tickers, processed_dataset_path)

    output_path = Path(__file__).parent / "results"
    output_path.mkdir(parents = True, exist_ok = True)

    # --- RESUME LOGIC: load already-completed configs and skip them ---
    full_csv = output_path / "gru_tuning_full.csv"
    if full_csv.exists():
        existing = pd.read_csv(full_csv)
        # keep only fully-complete configs (all 10 tickers); drop any partial one
        counts = existing.groupby("config").size()
        complete_configs = set(counts[counts >= len(tickers)].index)
        existing = existing[existing["config"].isin(complete_configs)]
        all_results = existing.to_dict("records")
        done_configs = complete_configs
        print(f"Resuming — {len(done_configs)} configs already complete, skipping them.")
    else:
        all_results = []
        done_configs = set()
    # -----------------------------------------------------------------

    for idx, config in enumerate(configs, 1):
        if config["name"] in done_configs:
            continue

        print(f"[{idx}/{len(configs)}] {config['name']} | window = {config['window']} units = {config['units']} layers = {config['layers']} dropout = {config['dropout']}")
        config_results = run_config(config, tickers, processed_dataset_path)
        all_results.extend(config_results)

        pd.DataFrame(all_results).to_csv(full_csv, index = False)

    df = pd.DataFrame(all_results)

    avg = df.groupby(["config", "window", "units", "layers", "dropout"])[["MAE", "MSE", "RMSE", "MAPE"]].mean().round(4).reset_index()
    avg_ranked = avg.sort_values("MAPE").reset_index(drop = True)

    avg_ranked.to_csv(output_path / "gru_tuning_ranked.csv", index = False)
    top5 = avg_ranked.head(5)
    top5.to_csv(output_path / "gru_tuning_top5.csv", index = False)

    plot_top(top5, output_path)

    print("\nTop 5 configurations by average MAPE:")
    print(top5[["config", "window", "units", "layers", "dropout", "MAPE"]].to_string(index=False))

gru_tuning()