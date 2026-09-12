# LSTM Tuning Comparison
Documentation of hyperparameter tuning experiments for the LSTM model on daily stock price forecasting. The goal of this experiment is to test the model's sensitivity to hyperparameter choices, rather than to maximize absolute performance.

## 1. Parameters
LSTM has more parameters that can be tested (p, d, q, P, D, Q, S) than LSTM. However, based on the tuning experiment of LSTM, widening the grid search range beyond 0-3 provided no improvement in accuracy. The tuning focuses on the seasonal-specific parameters unique to LSTM and the selection criterion.

This experiment tests the following parameters:
| No | Parameter | Values Tested | Reason |
|---|---|---|---|
| 1 | Window Size | 30, 60, 90 |  |
| 2 | Units | 32, 64, 128 |  |
| 3 | Layers | 1, 2, 3 |  |
| 4 | Dropout Rate | 0.1, 0.2, 0.3, 0.4 |  |

Other parameters (ADF threshold = 0.05, maximum d = 2) are held fixed, following standard practice in comparable literatures and research papers. To save time and computing power, grid search range for LSTM are fixed at 0-3 since it has been tested in LSTM before.

## 2. Experiment Configurations
| Configuration | Information Criterion | Seasonality |
|---|---|---|
| Combination_001 | AIC | 5 |
| Combination_002 | AIC | 20 |
| Combination_003 | BIC | 5 |
| Combination_004 | BIC | 20 |

Each configuration is run across all 10 tickers using a (80% training/10% validation/10% testing) split.

## 3. Results by Configuration
### 3.1 Average Metrics per Configuration
| Configuration | MAE (avg) | MSE (avg) | RMSE (avg) | MAPE (avg) |
|---|---|---|---|---|
| AIC_5 | 55.0788 | 9387.5498 | 78.2428 | 1.3812 |
| AIC_20 | 55.1618 | 9431.6902 | 78.3329 | 1.3842 |
| BIC_5 | 55.3181 | 9316.2038 | 78.2773 | 1.4009 |
| BIC_20 | 55.1382 | 9435.877 | 78.3542 | 1.3836 |

### 3.2 Selected Orders per Configuration
This table shows whether different criteria / ranges select different orders.

| Ticker | AIC_5 | AIC_20 | BIC_5 | BIC_20 |
|---|---|---|---|---|
| ADRO |  |  |  |  |
| BBCA |  |  |  |  |
| BBNI |  |  |  |  |
| BBRI |  |  |  |  |
| BBTN |  |  |  |  |
| BMRI |  |  |  |  |
| ITMG |  |  |  |  |
| MEDC |  |  |  |  |
| PGAS |  |  |  |  |
| PTBA |  |  |  |  |

Runtime: 4800 seconds (AIC_5), 72000 seconds (AIC_20), 4200 seconds (BIC_5), 43589.03 seconds (BIC_20)

### 3.3 Plot
The results produced by tuning can be compiled and summarised into a 2x2 plot:

![LSTM Tuning Plot](results/LSTM_tuning_comparison.png)

## 4. Analysis
This is a brief analysis of the results produced by tuning.

### 4.1 Effect of Selection Criterion (AIC vs BIC)
The use of AIC or BIC as the selection criterion have negligible effect on performance. Averaged across both configurations, AIC achieved MAPE of 1.3827% MAPE and BIC 1.3923%. The difference is less than 0.01 percentage points. BIC selected simpler orders, for example in ticker PGAS: BIC_5 selected (1,0,1), where AIC_5 selected (1,0,3). However, this simplification produced no meaningful change in accuracy.

### 4.2 Effect of Seasonal Period
The seasonal period had no meaningful effect on accuracy: weekly(s=5) averaged 1.3911% MAPE and monthly(s=20) averaged 1.3839%, a difference of less than 0.01 percentage points. About 68% of all fitted models selected a seasonal autoregressive order (P) of 0, indicating the models found little to no exploitable seasonal structure. This strongly suggests daily stock prices exhibit weak seasonality at both weekly and monthly scales, consistent with their near-random-walk behavior. The seasonal component of LSTM therefore provided little benefit over the non-seasonal LSTM structure.

### 4.3 Cross-Sector Consistency
Under AIC_5, energy tickers averaged 1.3354% MAPE and banking tickers 1.4269%, another difference of less than 0.1 percentage points, consistent across configurations (BIC_5: energy 1.3523%, banking 1.4496%). Similar to LSTM, individual ticker characteristics influenced forecasting error more than the sector it is in.

## 5. Conclusion
Each LSTM tuning generally performs the same with all four configurations producing average MAPE within a narrow band (1.3812%–1.4009%). The majority of models selected a seasonal AR order of 0, indicating minimal exploitable seasonality in daily stock prices at either weekly or monthly scales. LSTM's added seasonal complexity thus provided little benefit over the simpler LSTM model. The seasonal grid search was also computationally expensive, AIC_20 required approximately 20 hours, but yielded no accuracy gain. These findings reinforce the LSTM conclusion that daily stock prices are adequately modeled by low-order, largely non-seasonal terms and offer limited predictable structure for traditional models to exploit. BIC with weekly seasonality (s=5) was selected for consistency with the LSTM configuration and BIC's preference for simpler orders. As all configurations performed within a negligible margin (1.38%–1.40% MAPE), this choice prioritizes methodological consistency and model simplicity without sacrificing accuracy.

## Raw Full Results
Complete raw results are available [here](results/LSTM_tuning.csv).

| config | criterion | s | ticker | order | MAE | MSE | RMSE | MAPE |
|---|---|---|---|---|---|---|---|---|
| AIC_5 | AIC | 5 | ADRO |  |  |  |  |  |
| AIC_5 | AIC | 5 | BBCA |  |  |  |  |  |
| AIC_5 | AIC | 5 | BBNI |  |  |  |  |  |
| AIC_5 | AIC | 5 | BBRI |  |  |  |  |  |
| AIC_5 | AIC | 5 | BBTN |  |  |  |  |  |
| AIC_5 | AIC | 5 | BMRI |  |  |  |  |  |
| AIC_5 | AIC | 5 | ITMG |  |  |  |  |  |
| AIC_5 | AIC | 5 | MEDC |  |  |  |  |  |
| AIC_5 | AIC | 5 | PGAS |  |  |  |  |  |
| AIC_5 | AIC | 5 | PTBA |  |  |  |  |  |
| AIC_20 | AIC | 20 | ADRO |  | |  |  |  |
| AIC_20 | AIC | 20 | BBCA |  | |  |  |  |
| AIC_20 | AIC | 20 | BBNI |  | |  |  |  |
| AIC_20 | AIC | 20 | BBRI |  | |  |  |  |
| AIC_20 | AIC | 20 | BBTN |  | |  |  |  |
| AIC_20 | AIC | 20 | BMRI |  | |  |  |  |
| AIC_20 | AIC | 20 | ITMG |  | |  |  |  |
| AIC_20 | AIC | 20 | MEDC |  | |  |  |  |
| AIC_20 | AIC | 20 | PGAS |  | |  |  |  |
| AIC_20 | AIC | 20 | PTBA |  | |  |  |  |
| BIC_5 | BIC | 5 | ADRO |  |  |  |  |  |
| BIC_5 | BIC | 5 | BBCA |  |  |  |  |  |
| BIC_5 | BIC | 5 | BBNI |  |  |  |  |  |
| BIC_5 | BIC | 5 | BBRI |  |  |  |  |  |
| BIC_5 | BIC | 5 | BBTN |  |  |  |  |  |
| BIC_5 | BIC | 5 | BMRI |  |  |  |  |  |
| BIC_5 | BIC | 5 | ITMG |  |  |  |  |  |
| BIC_5 | BIC | 5 | MEDC |  |  |  |  |  |
| BIC_5 | BIC | 5 | PGAS |  |  |  |  |  |
| BIC_5 | BIC | 5 | PTBA |  |  |  |  |  |
| BIC_20 | BIC | 20 | ADRO |  | |  |  |  |
| BIC_20 | BIC | 20 | BBCA |  | |  |  |  |
| BIC_20 | BIC | 20 | BBNI |  | |  |  |  |
| BIC_20 | BIC | 20 | BBRI |  | |  |  |  |
| BIC_20 | BIC | 20 | BBTN |  | |  |  |  |
| BIC_20 | BIC | 20 | BMRI |  | |  |  |  |
| BIC_20 | BIC | 20 | ITMG |  | |  |  |  |
| BIC_20 | BIC | 20 | MEDC |  | |  |  |  |
| BIC_20 | BIC | 20 | PGAS |  | |  |  |  |
| BIC_20 | BIC | 20 | PTBA |  | |  |  |  |