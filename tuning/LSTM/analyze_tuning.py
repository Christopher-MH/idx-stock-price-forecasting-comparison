import sys
from pathlib import Path

import pandas as pd

def analyze_tuning(csv_path):
    df = pd.read_csv(csv_path)

    avg_metrics = (
        df.groupby("config")[["MAE", "MSE", "RMSE", "MAPE"]]
        .mean()
        .round(4)
        .reset_index()
    )

    orders = df.pivot(index = "ticker", columns = "config", values = "order")


    output_dir = Path(csv_path).parent
    avg_metrics.to_csv(output_dir / "sarima_tuning_averages.csv", index = False)
    orders.to_csv(output_dir / "sarima_tuning_orders.csv")

    return avg_metrics, orders


if __name__ == "__main__":
    csv_path = Path(__file__).parent / "results" / "sarima_tuning.csv"

    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])

    analyze_tuning(csv_path)