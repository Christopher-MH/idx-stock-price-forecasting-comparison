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

    top5 = avg_metrics.sort_values("MAPE").head(5)

    output_dir = Path(csv_path).parent
    avg_metrics.to_csv(output_dir / "sarima_tuning_averages.csv", index = False)
    top5.to_csv(output_dir / "sarima_tuning_top5.csv", index = False)

    return avg_metrics, top5

if __name__ == "__main__":
    csv_path = Path(__file__).parent / "results" / "sarima_tuning.csv"

    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])

    analyze_tuning(csv_path)