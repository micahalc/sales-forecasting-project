# 04_investigate_issues.py
# Purpose: look closely at the issues found in 03_quality_checks. Read-only.

from pathlib import Path

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 45)

raw_file = Path(__file__).resolve().parent.parent / "data" / "raw" / "Sample - Superstore.csv"
df = pd.read_csv(raw_file, encoding="cp1252")

print("=== A. THE DUPLICATE ROW (ignoring Row ID) ===")
no_id = df.drop(columns="Row ID")
dup_mask = no_id.duplicated(keep=False)  # keep=False shows BOTH copies
print(df.loc[dup_mask, ["Row ID", "Order ID", "Order Date", "Product ID",
                        "Product Name", "Sales", "Quantity", "Profit"]])

print("\n=== B. CELLS WITH EXTRA SPACES: which columns? ===")
text_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]
for col in text_cols:
    n = (df[col] != df[col].str.strip()).sum()
    if n > 0:
        print(f"{col}: {n} cells")
        print(df.loc[df[col] != df[col].str.strip(), col].head(3).apply(repr).to_string())

print("\n=== C. PRODUCT IDs WITH MORE THAN ONE NAME (first 3 examples) ===")
names_per_id = df.groupby("Product ID")["Product Name"].nunique()
multi_ids = names_per_id[names_per_id > 1].index[:3]
for pid in multi_ids:
    print(f"\n{pid}:")
    print(df.loc[df["Product ID"] == pid, "Product Name"].value_counts().to_string())

print("\n=== D. EXTREME VALUES ===")
cols = ["Order ID", "Order Date", "Sub-Category", "Product Name",
        "Sales", "Quantity", "Discount", "Profit"]
print("\n5 largest Sales rows:")
print(df.nlargest(5, "Sales")[cols])
print("\n5 largest losses:")
print(df.nsmallest(5, "Profit")[cols])
print("\n5 largest profits:")
print(df.nlargest(5, "Profit")[cols])

print("\n=== E. LOSSES AND DISCOUNT ===")
print("Loss rows by discount level (count of rows):")
print(df.loc[df["Profit"] < 0, "Discount"].value_counts().sort_index().to_string())
print("\nTotal profit by discount level:")
print(df.groupby("Discount")["Profit"].sum().round(0).to_string())