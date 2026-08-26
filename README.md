# **ANALISIS KOMPARATIF MODEL TIME SERIES TRADISIONAL DAN DEEP LEARNING UNTUK PREDIKSI HARGA SAHAM DI BURSA EFEK INDONESIA (BEI)**
This repository contains the thesis project of **Christopher Mannuel Hendrata** and **Mochammad Aqsa Sandhy Pradipta**.

A comparative study of five time-series forecasting models **(ARIMA, SARIMA, LSTM, GRU, Transformer)** to predict IDX stock prices across two contrasting sectors consistently placing in **LQ45**, which are **Banking(stable, high volume)** & **Energy(high volatility)**.

## Methodologies
1. Export Data using TradingView Premium
2. Preprocessing:
    - Remove missing/empty values
    - Duplicate removal
    - Filter date (1 April 2020 - 30 December 2025) 
    - Sort date by ASC
3. Data Splitting
4. Train Models
5. Test Models
6. Evaluate Models

## Models Evaluated
1. Traditional Time Series
    - ARIMA (Auto Regressive Integrated Moving Average)
    - SARIMA (Seasonal Auto Regressive Integrated Moving Average)
2. Deep Learning
    - GRU (Gated Recurrent Unit)
    - LSTM (Long-Short Term Memory)
    - Transformer

## Results
***🚧 Work in progress...***

## How to run
1. pip install -r requirements.txt
2. python utils/preprocessing.py
3. ***🚧 Work in progress...***

## Repository Structure
```bash
Thesis/
├── dataset/
│ ├── raw/          # raw TradingView exports
│ │ ├── energy/
│ │ └── banking/
│ └── processed/    # cleaned dataset
├── models/
│ ├── ARIMA/
│ ├── SARIMA/
│ ├── LSTM/
│ ├── GRU/
│ └── Transformer/
├── utils/          # preprocessing, data splitting, other utils
├── results/        # results produced by model
│ └── plots/          
├── requirements.txt
└── README.md
```

## Dataset Format
Each CSV file contains daily OHLCV data:

| time | open | high | low | close | Volume |
| --- | --- | --- | --- | --- | --- |
| date (YYYY-MM-DD) | float | float | float | float | integer |

## Tech Stack
- Python
- Pandas
- Numpy
- Matplotlib
- TensorFlow
- Statsmodels
- ***🚧 Work in progress...***

## Citation
This project is licensed under the MIT License, you're free to use, modify,
and build on it. If you find it useful in your own work or research, a mention
of the authors (Christopher Mannuel Hendrata & Mochammad Aqsa Sandhy Pradipta)
would be greatly appreciated.