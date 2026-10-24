# 10_category_region.py
# Purpose: performance by category, sub-category and region, plus the two loss months.

from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 45)

project = Path(__file__).resolve().parent.parent
df = pd.read_csv(
    project / "data" / "processed" / "superstore_clean.csv",
    dtype={"Postal Code": str},
    parse_dates=["Order Date", "Ship Date", "Order Month"],
)


def summarize(group_col):
    """Sales, profit, margin and average discount for one grouping column."""
    out = df.groupby(group_col).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Avg_Discount=("Discount", "mean"),
        Lines=("Row ID", "count"),
    )
    out["Profit Margin"] = out["Profit"] / out["Sales"]   # ratio of totals
    # Safety check: each summary must add back to the overall totals
    assert np.isclose(out["Sales"].sum(), df["Sales"].sum())
    assert np.isclose(out["Profit"].sum(), df["Profit"].sum())
    return out.sort_values("Profit", ascending=False)


rounding = {"Sales": 0, "Profit": 0, "Avg_Discount": 3, "Profit Margin": 3}

print("=== BY CATEGORY ===")
print(summarize("Category").round(rounding))

print("\n=== BY REGION ===")
print(summarize("Region").round(rounding))

print("\n=== BY SUB-CATEGORY (sorted by profit) ===")
print(summarize("Sub-Category").round(rounding))

print("\n=== THE TWO LOSS MONTHS: 3 biggest losing rows in each ===")
cols = ["Order ID", "Sub-Category", "Product Name", "Sales", "Discount", "Profit"]
for month in ["2014-07-01", "2015-01-01"]:
    rows = df[df["Order Month"] == pd.Timestamp(month)]
    print(f"\n{month[:7]}  (month profit: {rows['Profit'].sum():,.2f})")
    print(rows.nsmallest(3, "Profit")[cols].round(2).to_string(index=False))