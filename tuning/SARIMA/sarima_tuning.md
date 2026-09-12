# SARIMA Tuning Comparison
Documentation of hyperparameter tuning experiments for the SARIMA model on daily stock price forecasting. The goal of this experiment is to test the model's sensitivity to hyperparameter choices, rather than to maximize absolute performance.

## 1. Parameters
SARIMA has more parameters that can be tested (p, d, q, P, D, Q, S) than ARIMA. However, based on the tuning experiment of SARIMA, widening the grid search range beyond 0-3 provided no improvement in accuracy. The tuning focuses on the seasonal-specific parameters unique to SARIMA and the selection criterion.

This experiment tests the following parameters:
| No | Parameter | Values Tested | Reason |
|---|---|---|---|
| 1 | Selection criterion | AIC, BIC | To test whether the choice of information criterion, AIC (favors prediction accuracy) vs BIC (penalizes model complexity more heavily), affects the selected orders and performance |
| 2 | Seasonal period  | 5, 20 | To test whether weekly (5 workdays) or monthly (20 workdays) seasonality can produce results with better performance |

Other parameters (ADF threshold = 0.05, maximum d = 2) are held fixed, following standard practice in comparable literatures and research papers. To save time and computing power, grid search range for SARIMA are fixed at 0-3 since it has been tested in ARIMA before.

## 2. Experiment Configurations
| Configuration | Information Criterion | Seasonality |
|---|---|---|
| AIC_5 | AIC | 5 |
| AIC_20 | AIC | 20 |
| BIC_5 | BIC | 5 |
| BIC_20 | BIC | 20 |

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
| ADRO | (0,1,3)(0,0,3,5) | (0,1,3)(0,0,3,20) | (0,1,3)(0,0,3,5) | (0,1,3)(0,0,3,20) |
| BBCA | (0,1,3)(2,0,3,5) | (0,1,3)(0,0,3,20) | (0,1,3)(2,0,3,5) | (0,1,3)(0,0,3,20) |
| BBNI | (0,1,3)(2,0,3,5) | (0,1,3)(0,0,3,20) | (0,1,3)(0,0,3,5) | (0,1,3)(0,0,3,20) |
| BBRI | (3,1,3)(3,0,3,5) | (2,1,3)(3,0,3,20) | (0,1,3)(0,0,3,5) | (0,1,3)(0,0,3,20) |
| BBTN | (1,0,3)(1,0,3,5) | (1,0,3)(1,0,3,20) | (1,0,3)(0,0,3,5) | (1,0,3)(1,0,3,20) |
| BMRI | (0,1,3)(3,0,3,5) | (0,1,3)(0,0,3,20) | (0,1,3)(0,0,3,5) | (0,1,3)(0,0,3,20) |
| ITMG | (2,1,3)(0,0,3,5) | (1,1,3)(0,0,3,20) | (0,1,3)(0,0,3,5) | (1,1,3)(0,0,3,20) |
| MEDC | (2,1,3)(0,0,3,5) | (2,1,3)(0,0,3,20) | (0,1,3)(0,0,3,5) | (1,1,3)(0,0,3,20) |
| PGAS | (1,0,3)(1,0,3,5) | (3,0,3)(1,0,3,20) | (1,0,1)(0,0,3,5) | (3,0,0)(3,0,0,20) |
| PTBA | (0,1,3)(1,0,3,5) | (0,1,3)(0,0,3,20) | (0,1,3)(0,0,3,5) | (0,1,3)(0,0,3,20) |

Runtime: 117.389,03 seconds

### 3.3 Plot
The results produced by tuning can be compiled and summarised into a 2x2 plot:

![SARIMA Tuning Plot](results/SARIMA_tuning_comparison.png)

## 4. Analysis
This is a brief analysis of the results produced by tuning.

### 4.1 Effect of Selection Criterion (AIC vs BIC)
The use of AIC or BIC as the selection criterion have negligible effect on performance. Averaged across both configurations, AIC achieved MAPE of 1.3827% MAPE and BIC 1.3923%. The difference is less than 0.01 percentage points. BIC selected simpler orders, for example in ticker PGAS: BIC_5 selected (1,0,1), where AIC_5 selected (1,0,3). However, this simplification produced no meaningful change in accuracy.

### 4.2 Effect of Seasonal Period
The seasonal period had no meaningful effect on accuracy: weekly(s=5) averaged 1.3911% MAPE and monthly(s=20) averaged 1.3839%, a difference of less than 0.01 percentage points. About 68% of all fitted models selected a seasonal autoregressive order (P) of 0, indicating the models found little to no exploitable seasonal structure. This strongly suggests daily stock prices exhibit weak seasonality at both weekly and monthly scales, consistent with their near-random-walk behavior. The seasonal component of SARIMA therefore provided little benefit over the non-seasonal ARIMA structure.

### 4.3 Cross-Sector Consistency
Under AIC_5, energy tickers averaged 1.3354% MAPE and banking tickers 1.4269%, another difference of less than 0.1 percentage points, consistent across configurations (BIC_5: energy 1.3523%, banking 1.4496%). Similar to ARIMA, individual ticker characteristics influenced forecasting error more than the sector it is in.

## 5. Conclusion
Each SARIMA tuning generally performs the same with all four configurations producing average MAPE within a narrow band (1.3812%–1.4009%). The majority of models selected a seasonal AR order of 0, indicating minimal exploitable seasonality in daily stock prices at either weekly or monthly scales. SARIMA's added seasonal complexity thus provided little benefit over the simpler ARIMA model. The seasonal grid search was also computationally expensive, AIC_20 required approximately 20 hours, but yielded no accuracy gain. These findings reinforce the ARIMA conclusion that daily stock prices are adequately modeled by low-order, largely non-seasonal terms and offer limited predictable structure for traditional models to exploit. BIC with weekly seasonality (s=5) was selected for consistency with the ARIMA configuration and BIC's preference for simpler orders. As all configurations performed within a negligible margin (1.38%–1.40% MAPE), this choice prioritizes methodological consistency and model simplicity without sacrificing accuracy.

## Raw Full Results
Complete raw results are available [here](results/SARIMA_tuning.csv).

| config | criterion | s | ticker | order | MAE | MSE | RMSE | MAPE |
|---|---|---|---|---|---|---|---|---|
| AIC_5 | AIC | 5 | ADRO | (0,1,3)(0,0,3,5) | 31.94171447583797 | 2093.5149230797138 | 45.75494424736756 | 1.7444289402533657 |
| AIC_5 | AIC | 5 | BBCA | (0,1,3)(2,0,3,5) | 98.33545772652488 | 17643.24548150585 | 132.82787915759948 | 1.1970100569439128 |
| AIC_5 | AIC | 5 | BBNI | (0,1,3)(2,0,3,5) | 57.426403123386166 | 6369.977238642882 | 79.8121371637352 | 1.3586820301500169 |
| AIC_5 | AIC | 5 | BBRI | (3,1,3)(3,0,3,5) | 53.10697723179472 | 4988.64057638807 | 70.63030919080045 | 1.3748669597272545 |
| AIC_5 | AIC | 5 | BBTN | (1,0,3)(1,0,3,5) | 23.040027268647197 | 1052.0101737663197 | 32.434706315401094 | 1.8971281494482535 |
| AIC_5 | AIC | 5 | BMRI | (0,1,3)(3,0,3,5) | 61.37869634904717 | 6648.415240886718 | 81.53781479097117 | 1.3070517232174979 |
| AIC_5 | AIC | 5 | ITMG | (2,1,3)(0,0,3,5) | 153.81471614165008 | 50619.98850864356 | 224.9888630769167 | 0.6809903076107554 |
| AIC_5 | AIC | 5 | MEDC | (2,1,3)(0,0,3,5) | 25.502477703429776 | 1216.9209706057748 | 34.8843943706319 | 1.9318339290673971 |
| AIC_5 | AIC | 5 | PGAS | (1,0,3)(1,0,3,5) | 23.54889501850553 | 1124.218427123798 | 33.529366637677455 | 1.3772312681954366 |
| AIC_5 | AIC | 5 | PTBA | (0,1,3)(1,0,3,5) | 22.692379819504925 | 2118.5664760506297 | 46.02788802509441 | 0.9424750256621475 |
| AIC_20 | AIC | 20 | ADRO | (0,1,3)(0,0,3,20) | 32.17725813323305 | 2087.221099670115 | 45.68611495487568 | 1.7568619082671144 |
| AIC_20 | AIC | 20 | BBCA | (0,1,3)(0,0,3,20) | 98.62778022092081 | 17789.121207717613 | 133.3758644122602 | 1.2000365794797665 |
| AIC_20 | AIC | 20 | BBNI | (0,1,3)(0,0,3,20) | 57.41526694909409 | 6363.954834615436 | 79.77439961927283 | 1.3587312064348802 |
| AIC_20 | AIC | 20 | BBRI | (2,1,3)(3,0,3,20) | 53.49590690108382 | 4951.915197484012 | 70.36984579693217 | 1.3839464919949547 |
| AIC_20 | AIC | 20 | BBTN | (1,0,3)(1,0,3,20) | 22.783127699663815 | 1031.2582139658398 | 32.11320933768283 | 1.8769519581766931 |
| AIC_20 | AIC | 20 | BMRI | (0,1,3)(0,0,3,20) | 61.22987521777102 | 6680.9478601506335 | 81.7370653996743 | 1.3051222811489764 |
| AIC_20 | AIC | 20 | ITMG | (1,1,3)(0,0,3,20) | 153.7846350649683 | 50941.121748329264 | 225.70139952674035 | 0.6807958962203828 |
| AIC_20 | AIC | 20 | MEDC | (2,1,3)(0,0,3,20) | 25.755307615772686 | 1225.501576796988 | 35.007164649496936 | 1.9512006419455326 |
| AIC_20 | AIC | 20 | PGAS | (3,0,3)(1,0,3,20) | 23.694130664895056 | 1117.6137046328738 | 33.4307299446613 | 1.3879914784467515 |
| AIC_20 | AIC | 20 | PTBA | (0,1,3)(0,0,3,20) | 22.654428789810552 | 2128.2466235830166 | 46.132923423332024 | 0.9403456563503088 |
| BIC_5 | BIC | 5 | ADRO | (0,1,3)(0,0,3,5) | 31.94171447583797 | 2093.5149230797138 | 45.75494424736756 | 1.7444289402533657 |
| BIC_5 | BIC | 5 | BBCA | (0,1,3)(2,0,3,5) | 98.33545772652488 | 17643.24548150585 | 132.82787915759948 | 1.1970100569439128 |
| BIC_5 | BIC | 5 | BBNI | (0,1,3)(0,0,3,5) | 57.048520487603454 | 6330.685506817839 | 79.56560504902755 | 1.3498382946608405 |
| BIC_5 | BIC | 5 | BBRI | (0,1,3)(0,0,3,5) | 53.16903577934641 | 4981.8998455506335 | 70.58257465940608 | 1.3766742696978438 |
| BIC_5 | BIC | 5 | BBTN | (1,0,3)(0,0,3,5) | 24.574879236913997 | 1168.7912525138345 | 34.187589159135435 | 2.0202497532181214 |
| BIC_5 | BIC | 5 | BMRI | (0,1,3)(0,0,3,5) | 61.22110128563467 | 6625.24986207086 | 81.3956378565268 | 1.3041982464663222 |
| BIC_5 | BIC | 5 | ITMG | (0,1,3)(0,0,3,5) | 153.85762855074077 | 49803.83124546446 | 223.16771998984186 | 0.6812466460398745 |
| BIC_5 | BIC | 5 | MEDC | (0,1,3)(0,0,3,5) | 25.794269435808744 | 1224.8166275952865 | 34.99738029617769 | 1.9558621771153033 |
| BIC_5 | BIC | 5 | PGAS | (1,0,1)(0,0,3,5) | 24.46849424911103 | 1182.1848933552246 | 34.382915719223476 | 1.4338808532521223 |
| BIC_5 | BIC | 5 | PTBA | (0,1,3)(0,0,3,5) | 22.76990903493436 | 2107.818354335285 | 45.91098293802133 | 0.9459818224124046 |
| BIC_20 | BIC | 20 | ADRO | (0,1,3)(0,0,3,20) | 32.17725813323305 | 2087.221099670115 | 45.68611495487568 | 1.7568619082671144 |
| BIC_20 | BIC | 20 | BBCA | (0,1,3)(0,0,3,20) | 98.62778022092081 | 17789.121207717613 | 133.3758644122602 | 1.2000365794797665 |
| BIC_20 | BIC | 20 | BBNI | (0,1,3)(0,0,3,20) | 57.41526694909409 | 6363.954834615436 | 79.77439961927283 | 1.3587312064348802 |
| BIC_20 | BIC | 20 | BBRI | (0,1,3)(0,0,3,20) | 53.38715700236791 | 5004.463064774023 | 70.74222971305063 | 1.3817860741937014 |
| BIC_20 | BIC | 20 | BBTN | (1,0,3)(1,0,3,20) | 22.783127699663815 | 1031.2582139658398 | 32.11320933768283 | 1.8769519581766931 |
| BIC_20 | BIC | 20 | BMRI | (0,1,3)(0,0,3,20) | 61.22987521777102 | 6680.9478601506335 | 81.7370653996743 | 1.3051222811489764 |
| BIC_20 | BIC | 20 | ITMG | (1,1,3)(0,0,3,20) | 153.7846350649683 | 50941.121748329264 | 225.70139952674035 | 0.6807958962203828 |
| BIC_20 | BIC | 20 | MEDC | (1,1,3)(0,0,3,20) | 25.8207439643884 | 1224.2182174653262 | 34.98882989562992 | 1.9581116629443303 |
| BIC_20 | BIC | 20 | PGAS | (3,0,0)(3,0,0,20) | 23.501993603272396 | 1108.216902153685 | 33.28989189158903 | 1.3775855806648438 |
| BIC_20 | BIC | 20 | PTBA | (0,1,3)(0,0,3,20) | 22.654428789810552 | 2128.2466235830166 | 46.132923423332024 | 0.9403456563503088 |