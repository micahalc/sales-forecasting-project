# 15_candidate_models.py
# Purpose: compare candidate forecasting models using rolling-origin evaluation.
# Every forecast is built from training data that comes BEFORE its test window.

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.simplefilter("ignore", ConvergenceWarning)  # optimizer notices; results are still valid
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)
project = Path(__file__).resolve().parent.parent
monthly = pd.read_csv(project / "data" / "processed" / "monthly_sales.csv",
                      parse_dates=["Order Month"])
sales = monthly.set_index("Order Month")["Sales"].asfreq("MS")
H = 6  # forecast horizon in months


# ---------- Candidate models: each takes training data, returns H forecasts ----------
def seasonal_naive(train):
    """Each future month = the same month one year earlier."""
    return np.array([train.iloc[-12 + i] for i in range(H)])


def seasonal_naive_growth(train):
    """Seasonal naive, scaled by the growth of the last 12 months vs the 12 before."""
    growth = train.iloc[-12:].sum() / train.iloc[-24:-12].sum()
    return seasonal_naive(train) * growth


def holt_winters_no_trend(train):
    model = ExponentialSmoothing(train, trend=None, seasonal="add", seasonal_periods=12,
                                 initialization_method="estimated")
    return model.fit().forecast(H).values


def holt_winters_damped(train):
    model = ExponentialSmoothing(train, trend="add", damped_trend=True, seasonal="add",
                                 seasonal_periods=12, initialization_method="estimated")
    return model.fit().forecast(H).values


models = {
    "Seasonal Naive": seasonal_naive,
    "Seasonal Naive x Growth": seasonal_naive_growth,
    "Holt-Winters (no trend)": holt_winters_no_trend,
    "Holt-Winters (damped trend)": holt_winters_damped,
}


# ---------- Rolling-origin evaluation ----------
rows = []
for train_size in [30, 36, 42]:
    train = sales.iloc[:train_size]
    test = sales.iloc[train_size:train_size + H]
    assert train.index.max() < test.index.min()      # training always precedes testing
    window = f"{test.index.min():%b %Y} to {test.index.max():%b %Y}"
    for name, model in models.items():
        pred = model(train)
        error = test.values - pred
        rows.append({
            "Window": window, "Model": name,
            "MAE": np.abs(error).mean(),
            "RMSE": np.sqrt((error ** 2).mean()),
            "MAPE %": (np.abs(error) / test.values).mean() * 100,
            "Bias (actual minus forecast, total)": error.sum(),
        })

results = pd.DataFrame(rows)

print("=== MAE BY TEST WINDOW (lower is better) ===")
print(results.pivot(index="Model", columns="Window", values="MAE").round(0))

print("\n=== AVERAGE ACROSS THE THREE WINDOWS ===")
average = results.groupby("Model")[["MAE", "RMSE", "MAPE %"]].mean().sort_values("MAE")
print(average.round(1))

print("\n=== TOTAL BIAS BY WINDOW (positive = forecast was too LOW) ===")
print(results.pivot(index="Model", columns="Window",
                    values="Bias (actual minus forecast, total)").round(0))

# ---------- Detail for the final window (the one we used for baselines) ----------
train = sales.iloc[:42]
test = sales.iloc[42:]
detail = pd.DataFrame({"Actual": test}, index=test.index)
for name, model in models.items():
    detail[name] = model(train)
print("\n=== JUL-DEC 2017: ACTUAL VS EACH MODEL ===")
print(detail.round(0))