# 13_region_category_chart.py
# Purpose: chart sales and profit margin by region and by category.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

project = Path(__file__).resolve().parent.parent
df = pd.read_csv(
    project / "data" / "processed" / "superstore_clean.csv",
    dtype={"Postal Code": str},
    parse_dates=["Order Date", "Ship Date", "Order Month"],
)
fig_dir = project / "outputs" / "figures"
dollars = FuncFormatter(lambda x, pos: f"${x:,.0f}")


def summarize(col):
    out = df.groupby(col).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    out["Margin %"] = out["Profit"] / out["Sales"] * 100   # ratio of totals
    return out.sort_values("Sales", ascending=False)


region = summarize("Region")
category = summarize("Category")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Top row: sales; bottom row: profit margin. Left = region, right = category.
axes[0, 0].bar(region.index, region["Sales"], color="#4C72B0")
axes[0, 0].set_title("Sales by Region", fontweight="bold")
axes[0, 0].yaxis.set_major_formatter(dollars)

axes[1, 0].bar(region.index, region["Margin %"], color="#55A868")
axes[1, 0].set_title("Profit Margin by Region (%)", fontweight="bold")

axes[0, 1].bar(category.index, category["Sales"], color="#4C72B0")
axes[0, 1].set_title("Sales by Category", fontweight="bold")
axes[0, 1].yaxis.set_major_formatter(dollars)

axes[1, 1].bar(category.index, category["Margin %"], color="#55A868")
axes[1, 1].set_title("Profit Margin by Category (%)", fontweight="bold")

# Label each margin bar with its value
for ax in (axes[1, 0], axes[1, 1]):
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha="center", va="bottom", fontsize=9)
for ax in axes.flat:
    ax.grid(axis="y", alpha=0.3)

fig.suptitle("Sales and Profit Margin: Regions and Categories, 2014-2017",
             fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(fig_dir / "region_category_summary.png", dpi=150)
print("Saved:", fig_dir / "region_category_summary.png")
plt.show()