# Data Dictionary: Sample - Superstore.csv

Source: Kaggle "Superstore Dataset" (downloaded Oct 2026)
Raw file: data/raw/Sample - Superstore.csv (read with cp1252 encoding)
Grain: one row = one product line within an order (Order ID repeats)
Meanings below are inferred from column names and sample values.

| Column | Meaning |
|---|---|
| Row ID | Sequential row number |
| Order ID | Order identifier; repeats across product lines |
| Order Date | Date the order was placed (month/day/year text) |
| Ship Date | Date the order was shipped |
| Ship Mode | Shipping method (e.g. Second Class, Standard Class) |
| Customer ID | Customer identifier |
| Customer Name | Customer name |
| Segment | Customer segment (e.g. Consumer, Corporate) |
| Country | Country of the order |
| City | City of the order |
| State | State of the order |
| Postal Code | Postal code (to check for lost leading zeros) |
| Region | Sales region (e.g. South, West) |
| Product ID | Product identifier |
| Category | Top-level product category (e.g. Furniture, Office Supplies) |
| Sub-Category | Product sub-category |
| Product Name | Product description |
| Sales | Revenue of the line (currency not stated; assumed USD) |
| Quantity | Units sold on the line |
| Discount | Discount rate as a fraction (0.45 = 45%) |
| Profit | Profit of the line; can be negative |