# Project Brief: Sales Performance and Forecasting Report

## Business problem
Management needs evidence-based insight into historical sales and profit to
support sales planning, budgeting, and inventory decisions, plus a six-month
revenue forecast.

## Scope
- Data: Sample - Superstore.csv, orders from 2014-01-03 to 2017-12-30
- Forecast horizon: the six months after the data ends (Jan-Jun 2018).
  This is a practice forecast on historical data.
- Currency: not stated in the file; assumed to be USD.

## Key business questions
1. How have monthly sales and profit changed from 2014 to 2017?
2. Is there a repeating seasonal pattern in sales?
3. Which categories, sub-categories, and regions drive sales and profit?
4. Which products and sub-categories lose money, and what role do discounts play?
5. What is a reasonable forecast of monthly sales for the next six months,
   and how accurate is the method on data it has not seen?

## KPI definitions (used identically in Excel and Python)
| KPI | Definition |
|---|---|
| Total Sales | Sum of Sales |
| Total Profit | Sum of Profit |
| Profit Margin | Total Profit / Total Sales (ratio of totals, not an average of row margins) |
| Number of Orders | Count of distinct Order ID |
| Units Sold | Sum of Quantity |
| Average Order Value | Total Sales / Number of Orders |
| Average Discount | Mean of Discount across rows |
| Loss-Making Lines | Count of rows where Profit < 0 |

## Time definitions
- Month = calendar month of Order Date (not Ship Date)
- Forecast target = Total Sales per month