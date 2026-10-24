# 01_inspect_raw.py
# Purpose: load the raw Superstore CSV and take a first look. No cleaning yet.

from pathlib import Path

import pandas as pd

# Show all columns and wider output, so nothing is hidden with "..."
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# 1. Build the path to the raw file
raw_file = Path(__file__).resolve().parent.parent / "data" / "raw" / "Sample - Superstore.csv"

# 2. Load the CSV. Some Superstore files contain special characters that
#    fail with the default encoding, so we try a few common ones.
df = None
for encoding in ["utf-8", "cp1252", "latin-1"]:
    try:
        df = pd.read_csv(raw_file, encoding=encoding)
        print(f"Loaded successfully with encoding: {encoding}\n")
        break
    except UnicodeDecodeError:
        print(f"Encoding {encoding} failed, trying the next one...")

# 3. First look at the data
print("Shape (rows, columns):", df.shape)

print("\nColumn names:")
for name in df.columns:
    print(" -", name)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types and missing values:")
df.info()