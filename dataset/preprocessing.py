import shutil
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd

preprocessing_file_path = Path(__file__).parent
dataset_perbankan_path = preprocessing_file_path/"raw"/"perbankan"
# dataset_energi_path = preprocessing_file_path/"raw"/"energi"
dataset_energi_path = preprocessing_file_path/"test"

# Function
def daftar_nama_file(list_nama_file, path):
    for f in Path(path).glob("*.csv"):
        list_nama_file.append(f.name)

def ubah_nama(list_nama_file, i):
    tmp = list_nama_file[i].split("_")
    tmp_2 = tmp[2].split(",")
    nama_file = tmp_2[0]
    nama_file = nama_file + ".csv"
    return nama_file


file_perbankan = []
daftar_nama_file(file_perbankan, dataset_perbankan_path)
file_energi = []
daftar_nama_file(file_energi, dataset_energi_path)
# print(file_perbankan)
# print(file_energi)

for i in range(len(file_energi)):
    source_path = dataset_energi_path/file_energi[i]
    nama_file = ubah_nama(file_energi, i)

    destination_path = preprocessing_file_path/"processed"/nama_file
    print(destination_path)

    shutil.copy(source_path, destination_path)

    df = pd.read_csv(destination_path)

    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    df = df[(df["time"] >= "2020-04-01") & (df["time"] <= "2025-12-30")]

    df.to_csv(destination_path, index=False)


# struktur dataset: time, open, high, low, close, volume
# struct/class
# class Dataset:
#     def __init__(self, time, open, high, low, close, volume):
#         x = time.split("-")
#         self.time_y = x[0]
#         self.time_m = x[1]
#         self.time_d = x[2]

#         self.open = open
#         self.high = high
#         self.low = low
#         self.close = close
#         self.volume = volume