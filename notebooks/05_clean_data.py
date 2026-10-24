# 05_clean_data.py
# Purpose: apply our documented cleaning decisions and save a clean dataset.
# The raw file is never modified.

from pathlib import Path

import numpy as np
import pandas as pd

project = Path(__file__).resolve().parent.parent
raw_file = project / "data" / "raw" / "Sample - Superstore.csv"
clean_file = project / "data" / "processed" / "superstore_clean.csv"

df = pd.read_csv(raw_file, encoding="cp1252")

# Remember the original totals so we can prove we did not lose or change any money
rows_before = len(df)
sales_before = df["Sales"].sum()
profit_before = df["Profit"].sum()

# 1. Remove leading/trailing spaces from Product Name
df["Product Name"] = df["Product Name"].str.strip()

# 2. Convert dates from text to real dates (month/day/year)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")

# 3. Postal Code: make it 5-character text, restoring lost leading zeros
df["Postal Code"] = df["Postal Code"].astype(str).str.zfill(5)

# 4. Flag (do not delete) the possible duplicate: identical in every column except Row ID
df["Possible Duplicate"] = df.drop(columns="Row ID").duplicated(keep="first")

# 5. Add helper columns for monthly analysis
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()  # first day of month

# 6. Safety checks: stop with an error if anything unexpected changed
assert len(df) == rows_before, "Row count changed!"
assert np.isclose(df["Sales"].sum(), sales_before), "Total sales changed!"
assert np.isclose(df["Profit"].sum(), profit_before), "Total profit changed!"
assert (df["Product Name"] != df["Product Name"].str.strip()).sum() == 0
assert df["Postal Code"].str.len().eq(5).all()

# 7. Save the clean file (dates are written as yyyy-mm-dd)
df.to_csv(clean_file, index=False, encoding="utf-8")

# 8. Read the saved file back to confirm it loads correctly
check = pd.read_csv(clean_file, dtype={"Postal Code": str}, parse_dates=["Order Date", "Ship Date", "Order Month"])
print("Saved to:", clean_file)
print("Rows:", len(check), "| Columns:", check.shape[1])
print("Total Sales:  ", round(check["Sales"].sum(), 2))
print("Total Profit: ", round(check["Profit"].sum(), 2))
print("Flagged possible duplicates:", check["Possible Duplicate"].sum())
print("Example postal codes:", check["Postal Code"].head(3).tolist())
print(check[["Order Date", "Order Month", "Order Year"]].dtypes)