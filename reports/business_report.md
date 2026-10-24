# Sales Performance and Forecasting Report

*Practice project using the Sample - Superstore dataset (orders from January 2014 to December 2017). The currency is not stated in the file and is assumed to be USD.*

## 1. Executive summary

Over the four years in the data, the business earned \$286K of profit on \$2.30M of sales, a margin of 12.5%. Sales grew from \$484K in 2014 to \$733K in 2017, but orders grew faster than sales because the average order value fell.

Three findings matter most for planning:

1. **Heavy discounts coincide with losses.** Order lines discounted by more than 20% lost about \$135K combined, equal to about 47% of total profit. Lines with no discount earned a 29.5% margin.
2. **Furniture is the weak spot.** It generated \$742K of sales but only \$18K of profit (a 2.5% margin), against about 17% for Technology and Office Supplies. Tables and Bookcases lost money overall.
3. **Sales are seasonal.** September, November and December each had an above-average share of sales in all four years, while January and February were below average every year.

A model forecasts about **\$314K of sales for January to June 2018**, 22% above the same months of 2017. The range is wide, and a second model suggests about \$360K, so the forecast should be used as a planning range, not a single number. The data ends in December 2017, so this is a practice forecast on historical data, not a live prediction.

## 2. Business problem and objectives

Management needs evidence to support sales planning, budgeting and inventory decisions. This project answers five questions:

1. How have monthly sales and profit changed from 2014 to 2017?
2. Is there a repeating seasonal pattern?
3. Which categories, sub-categories and regions drive sales and profit?
4. Which products lose money, and what role do discounts play?
5. What is a reasonable forecast of monthly sales for the next six months, and how accurate is the method on data it has not seen?

## 3. Dataset and methodology

**Data.** The file has 9,994 order lines and 21 columns, covering orders placed from 3 January 2014 to 30 December 2017. All 48 months are present. One row is one product line within an order, so Order ID repeats. The data contains 5,009 distinct orders and 1,850 distinct product names.

**Tools.** Python (pandas, NumPy, Matplotlib, statsmodels) for cleaning, analysis and forecasting.

**KPI definitions** (used consistently throughout):

- Profit margin = total profit divided by total sales (a ratio of totals, not an average of row margins)
- Number of orders = count of distinct Order IDs
- Month = calendar month of the order date

## 4. Data quality and cleaning decisions

The raw file was checked before any change was made. It has no missing values, no blank cells, no impossible values, and no orders shipped before they were placed.

| Issue | Decision | Reason |
|---|---|---|
| 1 row matches another in every column except Row ID | Kept and flagged | Cannot tell an error from a genuine repeat; negligible effect on totals |
| 16 product names had trailing spaces | Removed | No information lost; prevents split groups |
| 32 Product IDs map to more than one product name | Left unchanged; products ranked by name | Product ID is not a reliable unique key |
| Very large orders and large losses | Kept | Plausible and internally consistent |
| 1,871 loss-making lines (18.7%) | Kept | Real business results |
| Dates stored as text | Converted to dates | Needed for monthly analysis |
| Postal codes had lost leading zeros | Stored as 5-character text | Not used in the analysis |

After cleaning, the row count, total sales (\$2,297,200.86) and total profit (\$286,397.02) were unchanged. The full log is in `reports/cleaning_log.md`.

## 5. Historical sales performance

| Year | Sales | Profit | Orders | Profit margin |
|---|---|---|---|---|
| 2014 | \$484K | \$49.5K | 969 | 10.2% |
| 2015 | \$471K | \$61.6K | 1,038 | 13.1% |
| 2016 | \$609K | \$81.8K | 1,315 | 13.4% |
| 2017 | \$733K | \$93.4K | 1,687 | 12.7% |

- Sales dipped 2.8% in 2015, then grew 29.5% in 2016 and 20.4% in 2017.
- Orders rose every year (up about 74% from 2014 to 2017), while sales rose about 51%. The average order value fell from \$499.74 to \$434.63. The data does not show why.
- Only 2 of 48 months lost money: July 2014 and January 2015. Each is mostly explained by a few heavily discounted lines.
- **Seasonality:** September, November and December together made up about 43% of annual sales, against 25% if sales were spread evenly.
- A few large orders matter. The largest 1% of lines (99 rows) made up 19.6% of all sales, and one Cisco order was about 41% of March 2014 sales. Part of the seasonal pattern may therefore come from one-off large purchases.

## 6. Category, region and product insights

| Category | Sales | Profit | Margin |
|---|---|---|---|
| Technology | \$836K | \$145K | 17.4% |
| Office Supplies | \$719K | \$122K | 17.0% |
| Furniture | \$742K | \$18K | 2.5% |

| Region | Sales | Profit | Margin | Avg. discount |
|---|---|---|---|---|
| West | \$725K | \$108K | 14.9% | 10.9% |
| East | \$679K | \$92K | 13.5% | 14.5% |
| South | \$392K | \$47K | 11.9% | 14.7% |
| Central | \$501K | \$40K | 7.9% | 24.0% |

- **Sub-categories.** Three lost money overall: Tables (-\$17.7K), Bookcases (-\$3.5K) and Supplies (-\$1.2K). Copiers were the most profitable (\$55.6K profit, 37.2% margin, from only 68 order lines). Supplies lost money despite a low average discount (7.7%), so discounts do not explain every loss.
- **Discounts.** Profit falls as the discount rises:

| Discount | Order lines | Profit | Margin |
|---|---|---|---|
| 0% | 4,798 | \$321.0K | 29.5% |
| 1-20% | 3,803 | \$100.8K | 11.9% |
| 21-40% | 460 | -\$35.8K | -15.3% |
| 41-60% | 215 | -\$28.9K | -40.7% |
| 61-80% | 718 | -\$70.6K | -122.6% |

  In the 61-80% band, losses were larger than sales. This is an association, not proof of cause. Discounts may have been given to products that were already low margin, or to clear stock, and this data cannot separate those explanations.
- **Products.** Of 1,850 distinct products, 301 (about 16%) lost money overall. The most profitable, the Canon imageCLASS 2200 Advanced Copier, earned \$25.2K, about 9% of all profit. The largest loss came from the Cubify CubeX 3D Printer (Double Head Print) at -\$8.9K.
- **Regions.** Central had the lowest margin and the highest average discount. Whether discounts explain this, or whether Central sells a different product mix, was not tested.

## 7. Forecast methodology and accuracy

**Target.** Total sales per calendar month (48 months, January 2014 to December 2017).

**Split.** Chronological, never shuffled. Models were fitted on January 2014 to June 2017 (42 months) and tested on July to December 2017 (6 months).

**Baselines.** Naive (repeat the last month), 3-month average, and seasonal naive (same month last year). Seasonal naive was the best baseline, with an average miss of about \$20.5K per month (MAPE 25.4%) on the final test window. It forecast \$380K for July to December 2017, against actual sales of \$476K.

**Candidate models.** Seasonal naive, seasonal naive scaled by recent growth, Holt-Winters exponential smoothing with a 12-month seasonal pattern and no trend, and the same with a damped trend. Because six test months is a small sample, each was evaluated on three rolling windows, always training only on earlier data:

| Training data | Test window |
|---|---|
| Jan 2014 to Jun 2016 | Jul to Dec 2016 |
| Jan 2014 to Dec 2016 | Jan to Jun 2017 |
| Jan 2014 to Jun 2017 | Jul to Dec 2017 |

**Results** (average across the three windows):

| Model | MAE | RMSE | MAPE |
|---|---|---|---|
| Holt-Winters (no trend) | \$10,952 | \$13,398 | 17.9% |
| Holt-Winters (damped trend) | \$11,217 | \$13,307 | 20.0% |
| Seasonal naive x growth | \$13,025 | \$16,185 | 24.3% |
| Seasonal naive | \$14,695 | \$17,487 | 23.7% |

**Selected model.** Holt-Winters without a trend. It had the lowest average error, was never worse than second place in any window, and is easy to explain: a base level plus a repeating yearly pattern. No model won every window, and the two Holt-Winters versions are too close to call a true winner. Every model forecast July to December 2017 too low. The selected model was \$81K too low in total that period, which was unusually strong.

**Final forecast.** The selected model was refitted on all 48 months to forecast January to June 2018. The range is the 10th to 90th percentile of the ratio of actual to forecast sales across the 18 test months, so it is an approximation and not a statistical guarantee.

## 8. Six-month forecast

| Month | Forecast | Low (10th pct) | High (90th pct) | Damped-trend comparison |
|---|---|---|---|---|
| Jan 2018 | \$43,851 | \$37,087 | \$66,198 | \$49,392 |
| Feb 2018 | \$34,574 | \$29,241 | \$52,193 | \$41,472 |
| Mar 2018 | \$70,540 | \$59,658 | \$106,488 | \$74,998 |
| Apr 2018 | \$53,054 | \$44,869 | \$80,090 | \$61,271 |
| May 2018 | \$56,746 | \$47,992 | \$85,664 | \$67,930 |
| Jun 2018 | \$55,685 | \$47,094 | \$84,062 | \$65,186 |
| **Total** | **\$314,449** | | | **\$360,250** |

The forecast total is 22.4% above the same months of 2017 (\$256,909). The damped-trend model is about 15% higher, so two reasonable models disagree by a meaningful amount.

![Monthly sales: history, held-out test and six-month forecast](../outputs/figures/final_forecast.png)

## 9. Recommendations

1. **Review discounts above 20%.** These lines lost about \$135K combined. Find out which products receive them and why before changing policy, because the data shows an association, not a cause.
2. **Review Furniture pricing, starting with Tables and Bookcases.** Sales are high but profit is small. Check costs, discounts and pricing for these items.
3. **Investigate discounting in the Central region.** Its margin is the lowest and its discounts the highest. Compare its product mix with other regions.
4. **Plan budgets and inventory around the forecast range, not a single figure.** Expect a slow January and February and a stronger March, and prepare for the September to December peak seen in every year.
5. **Monitor monthly.** Track forecast against actual sales, profit margin by discount band, and orders against average order value, and refresh the model as new data arrives.

## 10. Limitations and future improvements

- Only 48 months of data and a small test set, so accuracy and ranges are approximate.
- A few very large orders can move a month by 25% or more, and the model cannot predict them.
- The same test windows were used to choose the model and to measure its accuracy, so the reported error is a best-case estimate.
- The currency is not stated, and Superstore is a sample dataset, not a real company.
- The data ends in December 2017, so the forecast is a practice exercise, not a live prediction.
- Future work: more history, forecasts by category or region, other time-series models, and a closer look at which products receive heavy discounts and why.