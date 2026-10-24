# 12_outlier_concentration.py
# Purpose: measure how much a small number of large order lines drive sales,
# and which months depend most on a single line. Read-only.

from pathlib import Path

import pandas as pd

pd.set_option("display.width", 220)
pd.set_option("display.max_colwidth", 50)

project = Path(__file__).resolve().parent.parent
df = pd.read_csv(
    project / "data" / "processed" / "superstore_clean.csv",
    dtype={"Postal Code": str},
    parse_dates=["Order Date", "Ship Date", "Order Month"],
)

# ---------- 1. How concentrated is sales in the biggest lines? ----------
ranked = df.sort_values("Sales", ascending=False)
total_sales = df["Sales"].sum()
print("=== SHARE OF TOTAL SALES FROM THE LARGEST ORDER LINES ===")
for pct in [0.01, 0.05, 0.10]:
    k = int(len(df) * pct)
    share = ranked.head(k)["Sales"].sum() / total_sales
    print(f"Top {pct:.0%} of lines ({k} rows): {share:.1%} of sales")

print("\nTypical line size (median):", round(df["Sales"].median(), 2))
print("99th percentile line size: ", round(df["Sales"].quantile(0.99), 2))

# ---------- 2. Months that depend most on one single line ----------
monthly_total = df.groupby("Order Month")["Sales"].sum()
idx = df.groupby("Order Month")["Sales"].idxmax()        # row of the biggest line in each month
biggest = df.loc[idx, ["Order Month", "Product Name", "Sales"]].set_index("Order Month")
biggest["Month Total"] = monthly_total
biggest["Share of Month"] = biggest["Sales"] / biggest["Month Total"]

print("\n=== 8 MONTHS WHERE ONE LINE IS THE LARGEST SHARE OF SALES ===")
print(biggest.sort_values("Share of Month", ascending=False).head(8).round(3))

# ---------- 3. How different would monthly sales look without the biggest lines? ----------
cap = df["Sales"].quantile(0.99)
trimmed = df[df["Sales"] <= cap].groupby("Order Month")["Sales"].sum()
compare = pd.DataFrame({"Actual": monthly_total, "Without top 1% lines": trimmed})
compare["Difference"] = compare["Actual"] - compare["Without top 1% lines"]
print("\n=== 6 MONTHS WITH THE BIGGEST DIFFERENCE ===")
print(compare.sort_values("Difference", ascending=False).head(6).round(0))