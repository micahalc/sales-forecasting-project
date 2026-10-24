# 02_check_dates.py
# Purpose: verify date coverage before deciding on a forecasting approach.
# Read-only: we do not change the raw data.

from pathlib import Path

import pandas as pd

raw_file = Path(__file__).resolve().parent.parent / "data" / "raw" / "Sample - Superstore.csv"
df = pd.read_csv(raw_file, encoding="cp1252")

# Convert the text dates into real dates (month/day/year).
# errors="coerce" turns anything unreadable into NaT (a missing date) so we can count it.
order_dates = pd.to_datetime(df["Order Date"], format="%m/%d/%Y", errors="coerce")
ship_dates = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y", errors="coerce")

print("Unreadable Order Dates:", order_dates.isna().sum())
print("Unreadable Ship Dates:", ship_dates.isna().sum())

print("\nEarliest order date:", order_dates.min().date())
print("Latest order date:  ", order_dates.max().date())

# Which months appear in the data, and are any missing in between?
months_present = order_dates.dt.to_period("M").unique()
all_months = pd.period_range(order_dates.min(), order_dates.max(), freq="M")
missing_months = [str(m) for m in all_months if m not in months_present]

print("\nMonths present:", len(months_present))
print("Months expected between first and last date:", len(all_months))
print("Missing months:", missing_months if missing_months else "none")

# Does any order ship before it was placed? That would be suspicious.
print("\nRows where Ship Date is before Order Date:", (ship_dates < order_dates).sum())

# Rows per year, to see how the data is spread
print("\nRows per year:")
print(order_dates.dt.year.value_counts().sort_index())

# Postal Code check: how many values have fewer than 5 digits?
print("\nPostal codes with fewer than 5 digits:", (df["Postal Code"] < 10000).sum())