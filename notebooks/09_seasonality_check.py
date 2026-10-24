# 09_seasonality_check.py
# Purpose: identify loss-making months, best/worst months, and test for a repeating yearly pattern.

from pathlib import Path

import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

project = Path(__file__).resolve().parent.parent
monthly = pd.read_csv(
    project / "data" / "processed" / "monthly_sales.csv",
    parse_dates=["Order Month"],
)
monthly["Year"] = monthly["Order Month"].dt.year
monthly["Month"] = monthly["Order Month"].dt.month

print("=== MONTHS WITH A LOSS ===")
loss = monthly.loc[monthly["Profit"] < 0, ["Order Month", "Sales", "Profit", "Profit Margin"]]
print(loss.round({"Sales": 2, "Profit": 2, "Profit Margin": 3}).to_string(index=False))

print("\n=== 5 HIGHEST AND 5 LOWEST SALES MONTHS ===")
cols = ["Order Month", "Sales", "Profit"]
print("Highest:")
print(monthly.nlargest(5, "Sales")[cols].round(2).to_string(index=False))
print("Lowest:")
print(monthly.nsmallest(5, "Sales")[cols].round(2).to_string(index=False))

# Sales by calendar month (rows) and year (columns)
pivot = monthly.pivot(index="Month", columns="Year", values="Sales")
print("\n=== SALES BY MONTH AND YEAR ===")
print(pivot.round(0))

# Share of each year's sales that fell in each month.
# This removes the effect of overall growth, so years are comparable.
share = pivot / pivot.sum()
share["Average Share"] = share.mean(axis=1)
print("\n=== SHARE OF ANNUAL SALES BY MONTH ===")
print("(if sales were perfectly even, every cell would be about 0.083)")
print(share.round(3))