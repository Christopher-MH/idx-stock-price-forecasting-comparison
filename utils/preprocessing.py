from pathlib import Path
import pandas as pd

def list_file_name(dataset, dataset_path):
    for f in Path(dataset_path).glob("*.csv"):
        dataset.append(f.name)

def convert_file_name(name, i):
    tmp = name[i].split("_")
    tmp_2 = tmp[2].split(",")
    new_name = tmp_2[0]
    new_name = new_name + ".csv"
    return new_name

def clean_dataset(dataset, dataset_path, dataset_dir):
    for i in range(len(dataset)):
        source_path = dataset_path/dataset[i]

        file_name = convert_file_name(dataset, i)
        destination_path = dataset_dir/"processed"/file_name

        df = pd.read_csv(source_path)

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time", "open", "high", "low", "close", "Volume"])
        df = df.drop_duplicates(subset=["time"])
        df = df[(df["time"] >= "2020-04-01") & (df["time"] <= "2025-12-31")]
        df = df.sort_values("time").reset_index(drop=True)

        df.to_csv(destination_path, index=False)


preprocessing_path = Path(__file__).parent.parent
dataset_dir = preprocessing_path/"dataset"
banking_dataset_path = dataset_dir/"raw"/"banking"
energy_dataset_path = dataset_dir/"raw"/"energy"

banking_dataset = []
energy_dataset = []

list_file_name(banking_dataset, banking_dataset_path)
list_file_name(energy_dataset, energy_dataset_path)

clean_dataset(banking_dataset, banking_dataset_path, dataset_dir)
clean_dataset(energy_dataset, energy_dataset_path, dataset_dir)