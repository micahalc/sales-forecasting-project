# 16_final_forecast.py
# Purpose: refit the chosen model on all 48 months, forecast Jan-Jun 2018,
# add a rough uncertainty range from backtest errors, save table and chart.

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.simplefilter("ignore", ConvergenceWarning)
pd.set_option("display.width", 200)

project = Path(__file__).resolve().parent.parent
monthly = pd.read_csv(project / "data" / "processed" / "monthly_sales.csv",
                      parse_dates=["Order Month"])
sales = monthly.set_index("Order Month")["Sales"].asfreq("MS")
H = 6


def fit_forecast(train, damped=False):
    """Holt-Winters with a 12-month seasonal pattern; optional damped trend."""
    model = ExponentialSmoothing(
        train,
        trend="add" if damped else None,
        damped_trend=damped,
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated",
    )
    return model.fit().forecast(H)


# ---------- 1. Backtest errors for the chosen model (training always before test) ----------
ratios = []
holdout_pred = None
for train_size in [30, 36, 42]:
    train = sales.iloc[:train_size]
    test = sales.iloc[train_size:train_size + H]
    assert train.index.max() < test.index.min()
    pred = fit_forecast(train)
    assert (pred.values > 0).all(), "Forecast should be positive"
    ratios.extend((test.values / pred.values).tolist())   # >1 means the forecast was too low
    if train_size == 42:
        holdout_pred = pred                                # Jul-Dec 2017 prediction

ratios = np.array(ratios)
low_ratio, median_ratio, high_ratio = np.quantile(ratios, [0.10, 0.50, 0.90])
print("Backtest forecasts used for the range:", len(ratios))
print(f"Actual / forecast ratio: 10th pct {low_ratio:.2f} | median {median_ratio:.2f} | 90th pct {high_ratio:.2f}")

# ---------- 2. Final forecast: refit on ALL 48 months ----------
final = fit_forecast(sales)
final_damped = fit_forecast(sales, damped=True)
assert final.index.min() == pd.Timestamp("2018-01-01") and len(final) == H

table = pd.DataFrame({
    "Forecast": final,
    "Low (10th pct)": final * low_ratio,
    "High (90th pct)": final * high_ratio,
    "Damped-trend comparison": final_damped,
})
table.index.name = "Month"

print("\n=== FORECAST, JAN-JUN 2018 (USD) ===")
print(table.round(0))

same_period_2017 = sales.loc["2017-01-01":"2017-06-01"].sum()
print(f"\nForecast total, Jan-Jun 2018:        ${final.sum():,.0f}")
print(f"Actual total, Jan-Jun 2017:          ${same_period_2017:,.0f}")
print(f"Change vs same period of 2017:       {final.sum() / same_period_2017 - 1:+.1%}")
print(f"Damped-trend model, same total:      ${final_damped.sum():,.0f}")

out_file = project / "outputs" / "forecasts" / "sales_forecast_jan_jun_2018.csv"
table.round(2).to_csv(out_file)
print("\nSaved:", out_file)

# ---------- 3. Chart ----------
dollars = FuncFormatter(lambda x, pos: f"${x:,.0f}")
test = sales.iloc[-H:]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(sales.index, sales, color="#4C72B0", label="Historical sales (actual)")
ax.plot(test.index, test, color="black", marker="o", linewidth=2,
        label="Held-out actual (Jul-Dec 2017)")
ax.plot(holdout_pred.index, holdout_pred, color="#DD8452", linestyle="--", marker="s",
        label="Model prediction for held-out period (trained to Jun 2017)")
ax.plot(final.index, final, color="#C44E52", marker="o", label="Forecast Jan-Jun 2018")
ax.fill_between(final.index, table["Low (10th pct)"], table["High (90th pct)"],
                color="#C44E52", alpha=0.2, label="Rough range (10th-90th percentile of past errors)")
ax.axvline(pd.Timestamp("2017-06-15"), color="grey", linewidth=0.8)
ax.set_title("Monthly Sales: History, Held-Out Test, and Six-Month Forecast",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Monthly sales (USD)")
ax.yaxis.set_major_formatter(dollars)
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(project / "outputs" / "figures" / "final_forecast.png", dpi=150)
plt.show()