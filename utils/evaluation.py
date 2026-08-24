import numpy as np

def evaluate(predictions, actuals):
    mae = np.mean(np.abs(actuals - predictions))
    mse = np.mean((actuals - predictions) ** 2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
    return mae, mse, rmse, mape