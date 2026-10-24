# 07_kpis_and_yearly.py
# Purpose: calculate the project KPIs and a year-by-year summary.
# Definitions match reports/project_brief.md.

from pathlib import Path

import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

project = Path(__file__).resolve().parent.parent
clean_file = project / "data" / "processed" / "superstore_clean.csv"

df = pd.read_csv(
    clean_file,
    dtype={"Postal Code": str},
    parse_dates=["Order Date", "Ship Date", "Order Month"],
)

# ---------- Overall KPIs ----------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = total_profit / total_sales          # ratio of totals
orders = df["Order ID"].nunique()                   # distinct orders
units = df["Quantity"].sum()
avg_order_value = total_sales / orders
avg_discount = df["Discount"].mean()
loss_lines = (df["Profit"] < 0).sum()

print("=== OVERALL KPIs ===")
print(f"Total Sales:          ${total_sales:,.2f}")
print(f"Total Profit:         ${total_profit:,.2f}")
print(f"Profit Margin:        {profit_margin:.2%}")
print(f"Number of Orders:     {orders:,}")
print(f"Units Sold:           {units:,}")
print(f"Average Order Value:  ${avg_order_value:,.2f}")
print(f"Average Discount:     {avg_discount:.2%}")
print(f"Loss-Making Lines:    {loss_lines:,} of {len(df):,} ({loss_lines / len(df):.1%})")

# ---------- Year-by-year summary ----------
yearly = df.groupby("Order Year").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Units=("Quantity", "sum"),
)
yearly["Profit Margin"] = yearly["Profit"] / yearly["Sales"]
yearly["Sales Growth vs Prior Year"] = yearly["Sales"].pct_change()
yearly["Avg Order Value"] = yearly["Sales"] / yearly["Orders"]

print("\n=== YEARLY SUMMARY ===")
print(yearly.round({
    "Sales": 2, "Profit": 2, "Profit Margin": 3,
    "Sales Growth vs Prior Year": 3, "Avg Order Value": 2,
}))