# 03_quality_checks.py
# Purpose: look for data quality problems. Read-only: nothing is changed or saved.

from pathlib import Path

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

raw_file = Path(__file__).resolve().parent.parent / "data" / "raw" / "Sample - Superstore.csv"
df = pd.read_csv(raw_file, encoding="cp1252")

print("=== 1. DUPLICATES ===")
print("Fully identical rows:", df.duplicated().sum())
print("Duplicate Row IDs:", df["Row ID"].duplicated().sum())
# Same data in every column except Row ID
print("Duplicates ignoring Row ID:", df.drop(columns="Row ID").duplicated().sum())

print("\n=== 2. MISSING OR BLANK VALUES ===")
print("Missing per column (all should be 0):")
print(df.isna().sum()[df.isna().sum() > 0] if df.isna().any().any() else "none")

text_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]
blank_count = sum((df[c].str.strip() == "").sum() for c in text_cols)
spaces_count = sum((df[c] != df[c].str.strip()).sum() for c in text_cols)
print("Blank text cells:", blank_count)
print("Text cells with extra leading/trailing spaces:", spaces_count)

print("\n=== 3. CATEGORY VALUES (look for typos or odd labels) ===")
for col in ["Ship Mode", "Segment", "Country", "Region", "Category"]:
    print(f"\n{col}:")
    print(df[col].value_counts())
print("\nSub-Category:")
print(df["Sub-Category"].value_counts())

print("\n=== 4. NUMERIC FIELDS ===")
print(df[["Sales", "Quantity", "Discount", "Profit"]].describe())
print("\nRows with Sales <= 0:", (df["Sales"] <= 0).sum())
print("Rows with Quantity <= 0:", (df["Quantity"] <= 0).sum())
print("Rows with Discount outside 0 to 1:", ((df["Discount"] < 0) | (df["Discount"] > 1)).sum())
print("Rows with Profit < 0 (losses):", (df["Profit"] < 0).sum())
print("Rows with Profit = 0:", (df["Profit"] == 0).sum())

print("\n=== 5. CONSISTENCY ===")
print("Orders with more than one Order Date:",
      (df.groupby("Order ID")["Order Date"].nunique() > 1).sum())
print("Customer IDs with more than one name:",
      (df.groupby("Customer ID")["Customer Name"].nunique() > 1).sum())
print("Product IDs with more than one product name:",
      (df.groupby("Product ID")["Product Name"].nunique() > 1).sum())

print("\n=== 6. SHORT POSTAL CODES: which states? ===")
print(df.loc[df["Postal Code"] < 10000, "State"].value_counts())