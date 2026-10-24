# 14_baseline_forecasts.py
# Purpose: chronological train/test split and simple baseline forecasts.
# The test period is never used to build a forecast.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

pd.set_option("display.width", 200)

project = Path(__file__).resolve().parent.parent
monthly = pd.read_csv(project / "data" / "processed" / "monthly_sales.csv",
                      parse_dates=["Order Month"])
sales = monthly.set_index("Order Month")["Sales"].asfreq("MS")   # one value per month start

# ---------- 1. Chronological split ----------
HORIZON = 6
train = sales.iloc[:-HORIZON]
test = sales.iloc[-HORIZON:]

assert len(train) == 42 and len(test) == 6
assert train.index.max() < test.index.min(), "Training data must come before test data"
print("Train:", train.index.min().date(), "to", train.index.max().date(), f"({len(train)} months)")
print("Test: ", test.index.min().date(), "to", test.index.max().date(), f"({len(test)} months)")

# ---------- 2. Baseline forecasts (built from training data only) ----------
naive = pd.Series(train.iloc[-1], index=test.index)
avg3 = pd.Series(train.iloc[-3:].mean(), index=test.index)
seasonal_naive = pd.Series(
    [train.loc[d - pd.DateOffset(years=1)] for d in test.index], index=test.index
)

forecasts = pd.DataFrame({
    "Actual": test,
    "Naive": naive,
    "3-Month Avg": avg3,
    "Seasonal Naive": seasonal_naive,
})
print("\n=== TEST PERIOD: ACTUAL VS BASELINE FORECASTS ===")
print(forecasts.round(0))


# ---------- 3. Accuracy metrics ----------
def accuracy(actual, predicted):
    error = actual - predicted
    return {
        "MAE": error.abs().mean(),                          # average miss, in dollars
        "RMSE": np.sqrt((error ** 2).mean()),               # like MAE but punishes big misses more
        "MAPE %": (error.abs() / actual).mean() * 100,      # average miss as a % of actual
    }


results = pd.DataFrame({
    name: accuracy(test, forecasts[name])
    for name in ["Naive", "3-Month Avg", "Seasonal Naive"]
}).T
print("\n=== BASELINE ACCURACY (lower is better) ===")
print(results.round(1))

# ---------- 4. Chart ----------
dollars = FuncFormatter(lambda x, pos: f"${x:,.0f}")
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(train.index, train, color="#4C72B0", label="Training data")
ax.plot(test.index, test, color="black", marker="o", linewidth=2, label="Actual (test)")
ax.plot(test.index, naive, linestyle="--", label="Naive")
ax.plot(test.index, avg3, linestyle="--", label="3-month average")
ax.plot(test.index, seasonal_naive, linestyle="--", label="Seasonal naive")
ax.axvline(test.index.min(), color="grey", linewidth=0.8)
ax.set_title("Baseline Forecasts vs Actual Sales (Jul-Dec 2017)", fontsize=13, fontweight="bold")
ax.set_ylabel("Monthly sales (USD)")
ax.yaxis.set_major_formatter(dollars)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(project / "outputs" / "figures" / "baseline_forecasts.png", dpi=150)
plt.show()