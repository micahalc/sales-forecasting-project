# setup_check.py
# Purpose: confirm our libraries work and see what files are in data/raw.

from pathlib import Path

import pandas
import numpy
import matplotlib
import statsmodels
import openpyxl

print("pandas:", pandas.__version__)
print("numpy:", numpy.__version__)
print("matplotlib:", matplotlib.__version__)
print("statsmodels:", statsmodels.__version__)
print("openpyxl:", openpyxl.__version__)

# Find the data/raw folder relative to this file's location
raw_folder = Path(__file__).resolve().parent.parent / "data" / "raw"
print("\nFiles in data/raw:")
for file in raw_folder.iterdir():
    print(" -", file.name)