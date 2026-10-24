# 06_monthly_table.py
# Purpose: aggregate the clean data to one row per month for trend analysis and forecasting.

from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("display.width", 200)

project = Path(__file__).resolve().parent.parent
clean_file = project / "data" / "processed" / "superstore_clean.csv"
monthly_file = project / "data" / "processed" / "monthly_sales.csv"

df = pd.read_csv(
    clean_file,
    dtype={"Postal Code": str},
    parse_dates=["Order Date", "Ship Date", "Order Month"],
)

# One row per month. Definitions match the project brief.
monthly = df.groupby("Order Month").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),   # distinct orders, not rows
    Units=("Quantity", "sum"),
).reset_index()

# Profit margin = total profit / total sales (ratio of totals)
monthly["Profit Margin"] = monthly["Profit"] / monthly["Sales"]

# Safety checks: the monthly table must add up to the clean dataset
assert len(monthly) == 48, "Expected 48 months"
assert np.isclose(monthly["Sales"].sum(), df["Sales"].sum()), "Sales do not match"
assert np.isclose(monthly["Profit"].sum(), df["Profit"].sum()), "Profit does not match"
assert monthly["Orders"].sum() == df["Order ID"].nunique(), "Orders do not add up"
monthly.to_csv(monthly_file, index=False)

print("Saved to:", monthly_file)
print("Months:", len(monthly))
print("Total distinct orders in the dataset:", df["Order ID"].nunique())
print("\nFirst 6 months:")
print(monthly.head(6).round({"Sales": 2, "Profit": 2, "Profit Margin": 3}))
print("\nLast 6 months:")
print(monthly.tail(6).round({"Sales": 2, "Profit": 2, "Profit Margin": 3}))
print("\nMonthly Sales summary:")
print(monthly["Sales"].describe().round(2))