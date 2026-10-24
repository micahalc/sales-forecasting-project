# 08_monthly_trend_chart.py
# Purpose: chart monthly sales and profit, and save the figure to outputs/figures.

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

project = Path(__file__).resolve().parent.parent
monthly = pd.read_csv(
    project / "data" / "processed" / "monthly_sales.csv",
    parse_dates=["Order Month"],
)
figure_file = project / "outputs" / "figures" / "monthly_sales_profit_trend.png"

# A 3-month rolling average smooths month-to-month noise so the trend is easier to see
monthly["Sales 3M Avg"] = monthly["Sales"].rolling(window=3).mean()

# Format axis numbers as dollars, e.g. $60,000
dollars = FuncFormatter(lambda x, pos: f"${x:,.0f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

# Top panel: sales
ax1.plot(monthly["Order Month"], monthly["Sales"], marker="o", markersize=4,
         color="#4C72B0", label="Monthly sales")
ax1.plot(monthly["Order Month"], monthly["Sales 3M Avg"], linewidth=2.5,
         color="#DD8452", label="3-month average")
ax1.set_title("Monthly Sales, Jan 2014 to Dec 2017", fontsize=13, fontweight="bold")
ax1.set_ylabel("Sales (USD)")
ax1.yaxis.set_major_formatter(dollars)
ax1.legend()
ax1.grid(alpha=0.3)

# Bottom panel: profit
ax2.plot(monthly["Order Month"], monthly["Profit"], marker="o", markersize=4,
         color="#55A868")
ax2.axhline(0, color="black", linewidth=0.8)  # zero line: below it means a loss
ax2.set_title("Monthly Profit", fontsize=13, fontweight="bold")
ax2.set_ylabel("Profit (USD)")
ax2.yaxis.set_major_formatter(dollars)
ax2.grid(alpha=0.3)

# X-axis: a label every 6 months
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

fig.tight_layout()
fig.savefig(figure_file, dpi=150)
print("Saved:", figure_file)
plt.show()