# Cleaning Log

Raw file: data/raw/Sample - Superstore.csv (9,994 rows, 21 columns, read with cp1252)
Clean file: data/processed/superstore_clean.csv (9,994 rows, 24 columns)
Script: notebooks/05_clean_data.py

## Verified before cleaning
- No missing values, no blank cells, no fully identical rows
- All 48 months from 2014-01 to 2017-12 present; no unreadable dates
- No orders shipped before they were placed
- No impossible values (Sales > 0, Quantity > 0, Discount between 0 and 1)

## Decisions
| Issue | Finding | Decision | Reason |
|---|---|---|---|
| Possible duplicate | 1 row matches another in every column except Row ID | Kept, flagged in "Possible Duplicate" | Cannot tell an error from a genuine repeat line; negligible effect on totals |
| Trailing spaces | 16 Product Name cells | Removed | No information lost; prevents split groups |
| Product ID with multiple names | 32 IDs map to more than one name | Left unchanged; use Product Name for product rankings | Product ID is not a reliable unique key |
| Extreme sales and losses | Largest items are copiers, 3D printers, binding machines | Kept | Internally consistent and plausible |
| Negative profit | 1,871 rows (about 18.7%) | Kept | Real business results |
| Dates as text | Order Date, Ship Date stored as text | Converted (month/day/year) | Needed for monthly analysis |
| Postal Code | 449 values lost a leading zero | Stored as 5-character text | Cause was numeric format; not used in analysis |

## Columns added
Possible Duplicate, Order Year, Order Month (first day of the order's month)

## Verification after cleaning
Row count unchanged. Total Sales 2,297,200.86 and Total Profit 286,397.02 unchanged.

## Assumptions
- Currency not stated in the file; assumed USD.
- Month is based on Order Date, not Ship Date.