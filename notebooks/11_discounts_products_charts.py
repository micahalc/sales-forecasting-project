# 11_discounts_products_charts.py
# Purpose: profit by discount band, top/bottom products, and two saved charts.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

pd.set_option("display.width", 220)
pd.set_option("display.max_colwidth", 60)

project = Path(__file__).resolve().parent.parent
df = pd.read_csv(
    project / "data" / "processed" / "superstore_clean.csv",
    dtype={"Postal Code": str},
    parse_dates=["Order Date", "Ship Date", "Order Month"],
)
fig_dir = project / "outputs" / "figures"
dollars = FuncFormatter(lambda x, pos: f"${x:,.0f}")

# ---------- 1. Profit by discount band ----------
bands = pd.cut(
    df["Discount"],
    bins=[-0.001, 0.0, 0.2, 0.4, 0.6, 0.8],
    labels=["0%", "1-20%", "21-40%", "41-60%", "61-80%"],
)
by_band = df.groupby(bands, observed=True).agg(
    Lines=("Row ID", "count"),
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
)
by_band["Profit Margin"] = by_band["Profit"] / by_band["Sales"]
print("=== PROFIT BY DISCOUNT BAND ===")
print(by_band.round({"Sales": 0, "Profit": 0, "Profit Margin": 3}))

# ---------- 2. Top and bottom 10 products by total profit ----------
# We group by Product Name because Product ID is not a reliable key (see cleaning log)
by_product = df.groupby("Product Name").agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum")
).sort_values("Profit", ascending=False)
print("\n=== TOP 10 PRODUCTS BY PROFIT ===")
print(by_product.head(10).round(0))
print("\n=== BOTTOM 10 PRODUCTS BY PROFIT ===")
print(by_product.tail(10).round(0))

# ---------- 3. Chart: profit by sub-category ----------
sub = df.groupby("Sub-Category")["Profit"].sum().sort_values()
colors = ["#C44E52" if v < 0 else "#55A868" for v in sub]  # red = loss, green = profit

fig1, ax1 = plt.subplots(figsize=(9, 7))
ax1.barh(sub.index, sub.values, color=colors)
ax1.axvline(0, color="black", linewidth=0.8)
ax1.set_title("Total Profit by Sub-Category, 2014-2017", fontsize=13, fontweight="bold")
ax1.set_xlabel("Profit (USD)")
ax1.xaxis.set_major_formatter(dollars)
ax1.grid(axis="x", alpha=0.3)
fig1.tight_layout()
fig1.savefig(fig_dir / "profit_by_subcategory.png", dpi=150)

# ---------- 4. Chart: profit margin by discount band ----------
fig2, ax2 = plt.subplots(figsize=(8, 5))
margin_colors = ["#C44E52" if v < 0 else "#4C72B0" for v in by_band["Profit Margin"]]
ax2.bar(by_band.index.astype(str), by_band["Profit Margin"] * 100, color=margin_colors)
ax2.axhline(0, color="black", linewidth=0.8)
ax2.set_title("Profit Margin by Discount Band", fontsize=13, fontweight="bold")
ax2.set_xlabel("Discount applied")
ax2.set_ylabel("Profit margin (%)")
ax2.grid(axis="y", alpha=0.3)
fig2.tight_layout()
fig2.savefig(fig_dir / "margin_by_discount_band.png", dpi=150)

print("\nSaved charts to:", fig_dir)
plt.show()