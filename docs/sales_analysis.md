# E-Commerce Sales Analysis Report

## 1. Overview

This report presents the SQL-based analysis of historical e-commerce transactions from the UCI Online Retail dataset.

The objective is to evaluate sales performance, identify trends in purchasing activity, and extract meaningful business insights from the cleaned data stored in MySQL.

**Dataset:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

**Reporting period:** December 2010 – December 2011

**Database:** MySQL 8.4

**Cleaned transaction records:** 536,641

**SQL queries:** [View Sales Analysis SQL](../sql/sales_Analysis.sql)

### Analysis Scope

The dataset includes several transaction types, including sales, cancellations, adjustments, zero-price transactions, and bad-debt records.

For the analyses in this report, gross sales metrics include only transactions classified as `SALE`.

This allows us to measure positive sales activity separately from cancellations and other transaction types.

---

## 2. Analysis 1 — Gross Sales Revenue

### Business Question

How much gross sales revenue did the retailer generate during the reporting period?

### Methodology

Gross sales revenue is calculated by multiplying `Quantity` by `UnitPrice` for each transaction classified as `SALE`, then summing the results.

**Formula:**

Gross Sales Revenue = SUM(Quantity × UnitPrice)

Cancellations, adjustments, zero-price transactions, and bad-debt records are excluded.

### Results

| Metric | Value |
|---|---:|
| Gross sales revenue | **£10,642,110.80** |
| SALE transaction lines | 524,878 |

### Business Insights

The retailer recorded approximately **£10.64 million in gross sales revenue** during the reporting period.

This provides a baseline for evaluating monthly performance, product contributions, and customer purchasing behavior.

### Limitations

Gross sales revenue does not account for cancellations, refunds, operational costs, or other adjustments.

Therefore, it should not be interpreted as net revenue or profit.

**SQL implementation:** Query 1 in [sales_Analysis.sql](../sql/sales_Analysis.sql).

---

## 3. Analysis 2 — Monthly Sales Performance

### Business Question

How did gross sales revenue and sales invoice volume change over time?

### Methodology

Transactions classified as `SALE` were grouped by calendar month.

For each month, two metrics were calculated:

- **Gross Revenue:** Total value of SALE transaction lines.
- **Total Invoices:** Number of distinct invoice identifiers containing SALE transaction lines.

Using `COUNT(DISTINCT InvoiceNo)` prevents invoices containing multiple product lines from being counted multiple times.

### Results

| Month | Total Invoices | Gross Revenue |
|---|---:|---:|
| December 2010 | 1,559 | £821,452.73 |
| January 2011 | 1,086 | £689,811.61 |
| February 2011 | 1,100 | £522,545.56 |
| March 2011 | 1,454 | £716,215.26 |
| April 2011 | 1,246 | £536,968.49 |
| May 2011 | 1,681 | £769,296.61 |
| June 2011 | 1,533 | £760,547.01 |
| July 2011 | 1,475 | £718,076.12 |
| August 2011 | 1,361 | £757,841.38 |
| September 2011 | 1,837 | £1,056,435.19 |
| October 2011 | 2,040 | £1,151,263.73 |
| November 2011 | 2,769 | £1,503,866.78 |
| December 2011 | 819 | £637,790.33 |

### Key Findings

**1. November 2011 was the strongest month.**

November generated £1,503,866.78 in gross revenue from 2,769 distinct sales invoices.

It recorded both the highest monthly gross revenue and the highest invoice count.

**2. Sales activity increased significantly between September and November 2011.**

Gross revenue exceeded £1 million in each of these three months.

This period also showed increasing invoice counts, suggesting stronger purchasing activity.

**3. February 2011 recorded the lowest gross revenue among the complete reporting months.**

Revenue reached £522,545.56.

**4. December 2011 is an incomplete reporting month.**

The dataset ends on December 9, 2011.

Therefore, the lower total revenue and invoice count in December should not be interpreted as evidence of a decline in business performance.

### Business Interpretation

The results reveal a particularly strong period of sales activity during September, October, and November 2011.

This pattern may be consistent with seasonal purchasing behavior, but additional analysis is needed to establish its causes.

Potential follow-up investigations include identifying which products, countries, and customer groups contributed most to the increase.

**SQL implementation:** Query 2 in [sales_Analysis.sql](../sql/sales_Analysis.sql).

---

## 4. Analysis 3 — Average Invoice Value

### Business Question

Was revenue growth driven primarily by an increase in the number of invoices or by higher average spending per invoice?

### Methodology

Average invoice value measures the average gross sales amount associated with each distinct sales invoice.

**Formula:**

Average Invoice Value = Gross Sales Revenue / Number of Distinct Sales Invoices

Only records classified as `SALE` are included.

### Results

| Month | Total Invoices | Average Invoice Value |
|---|---:|---:|
| December 2010 | 1,559 | £526.91 |
| January 2011 | 1,086 | £635.19 |
| February 2011 | 1,100 | £475.04 |
| March 2011 | 1,454 | £492.58 |
| April 2011 | 1,246 | £430.95 |
| May 2011 | 1,681 | £457.64 |
| June 2011 | 1,533 | £496.12 |
| July 2011 | 1,475 | £486.83 |
| August 2011 | 1,361 | £556.83 |
| September 2011 | 1,837 | £575.09 |
| October 2011 | 2,040 | £564.34 |
| November 2011 | 2,769 | £543.11 |
| December 2011 | 819 | £778.74 |

### Key Findings

**1. Average invoice value decreased between September and November 2011.**

| Metric | September 2011 | November 2011 |
|---|---:|---:|
| Gross revenue | £1,056,435.19 | £1,503,866.78 |
| Total invoices | 1,837 | 2,769 |
| Average invoice value | £575.09 | £543.11 |

Despite higher total revenue, average invoice value decreased by approximately 5.6%.

**2. November's stronger revenue was primarily associated with increased invoice volume.**

The number of distinct sales invoices increased by approximately 50.7% between September and November.

This increase occurred alongside a decrease in average invoice value.

Therefore, invoice volume was the main driver of revenue growth over this period.

**3. December 2011 recorded the highest reported average invoice value.**

December's average invoice value was £778.74.

However, December is an incomplete reporting month, so this result should be interpreted cautiously.

**4. April 2011 recorded the lowest average invoice value.**

The average invoice value was £430.95.

This suggests that sales invoices in April were smaller in monetary value on average than in other reported months.

### Business Interpretation

Revenue growth does not necessarily mean that customers are spending more per purchase.

In this dataset, the September–November revenue increase was accompanied by more sales invoices but lower average invoice values.

This distinction is important because businesses can increase revenue through different mechanisms, including:

- Increasing the number of purchases.
- Increasing the average value of purchases.
- Combining both approaches.

The findings suggest that increasing sales invoice volume was particularly important during the retailer's strongest reporting period.

**SQL implementation:** Query 3 in [sales_Analysis.sql](../sql/sales_Analysis.sql).

---

## 5. Analysis 4 — Top 10 StockCodes by Gross Revenue

### Business Question

Which StockCodes generated the highest gross sales revenue?

### Methodology

Transactions classified as `SALE` were grouped by `StockCode`.

For each StockCode, the following metrics were calculated:

- Gross sales revenue
- Total units sold
- Number of distinct invoices

The results were sorted by gross revenue in descending order, and the top 10 were selected.

### Results

| StockCode | Gross Revenue | Units Sold | Invoice Count |
|---|---:|---:|---:|
| DOT | £206,248.77 | 706 | 706 |
| 22423 | £174,156.54 | 13,851 | 1,988 |
| 23843 | £168,469.60 | 80,995 | 1 |
| 85123A | £104,462.75 | 37,641 | 2,198 |
| 47566 | £99,445.23 | 18,283 | 1,685 |
| 85099B | £94,159.81 | 48,371 | 2,089 |
| 23166 | £81,700.92 | 78,033 | 247 |
| POST | £78,101.88 | 3,150 | 1,126 |
| M | £77,750.27 | 6,984 | 289 |
| 23084 | £66,870.03 | 30,739 | 994 |

### Key Findings

**1. StockCode DOT generated the highest gross revenue.**

DOT generated £206,248.77 across 706 invoices.

However, this identifier may represent a charge rather than a physical product.

**2. StockCode 22423 generated £174,156.54.**

It appeared on 1,988 distinct invoices, suggesting frequent purchasing activity.

**3. StockCode 23843 recorded an unusually large quantity on a single invoice.**

The recorded quantity was 80,995 units, generating £168,469.60 in gross revenue.

This result warrants further investigation before drawing conclusions about typical product demand.

### Business Interpretation

High revenue does not necessarily correspond to high quantities sold or high purchasing frequency.

Some StockCodes generate substantial revenue through large individual transactions, while others appear across many invoices.

The current ranking is preliminary because the dataset contains identifiers that may represent postage, manual charges, or other non-merchandise transactions.

**SQL implementation:** Query 4 in [sales_Analysis.sql](../sql/sales_Analysis.sql).

---

## 6. Analysis 5 — Revenue by Country

### Business Question

Which customer countries contributed the most gross sales revenue?

### Methodology

Transactions classified as `SALE` were grouped by `Country`.

For each country, the analysis calculated:

- Total gross sales revenue
- Number of distinct sales invoices

The countries were ranked by gross revenue.

The `Country` field represents the customer's country of residence, not necessarily the shipping destination.

### Results

| Country | Total Invoices | Gross Revenue |
|---|---:|---:|
| United Kingdom | 18,019 | £9,001,744.09 |
| Netherlands | 94 | £285,446.34 |
| EIRE | 288 | £283,140.52 |
| Germany | 457 | £228,678.40 |
| France | 392 | £209,625.37 |
| Australia | 57 | £138,453.81 |
| Spain | 90 | £61,558.56 |
| Switzerland | 54 | £57,067.60 |
| Belgium | 98 | £41,196.34 |
| Sweden | 36 | £38,367.83 |

### Key Findings

**1. The United Kingdom dominates gross sales revenue.**

The United Kingdom generated approximately £9 million, representing around 84.6% of total gross sales revenue.

**2. The Netherlands and EIRE are the next highest-revenue customer countries.**

The Netherlands generated £285,446.34, followed by EIRE with £283,140.52.

**3. Invoice volume and revenue rankings differ.**

Germany recorded 457 invoices and generated £228,678.40, while the Netherlands recorded only 94 invoices but generated higher gross revenue.

This illustrates how average invoice values can vary between customer countries.

### Business Interpretation

The retailer's revenue is highly concentrated among customers residing in the United Kingdom.

International customer countries contribute a smaller share of gross revenue, but some generate substantial revenue from relatively few invoices.

**SQL implementation:** Query 5 in [sales_Analysis.sql](../sql/sales_Analysis.sql).

---

## 7. Analysis 6 — Top 10 Customers by Gross Revenue

### Business Question

Which identified customers generated the highest gross sales revenue?

### Methodology

Transactions classified as `SALE` were grouped by `CustomerID`.

Records with missing customer identifiers were excluded to avoid treating all unidentified customers as one customer.

For each identified customer, the analysis calculated:

- Number of distinct sales invoices
- Total gross sales revenue

### Results

| CustomerID | Total Invoices | Gross Revenue |
|---|---:|---:|
| 14646 | 73 | £280,206.02 |
| 18102 | 60 | £259,657.30 |
| 17450 | 46 | £194,390.79 |
| 16446 | 2 | £168,472.50 |
| 14911 | 201 | £143,711.17 |
| 12415 | 21 | £124,914.53 |
| 14156 | 55 | £117,210.08 |
| 17511 | 31 | £91,062.38 |
| 16029 | 63 | £80,850.84 |
| 12346 | 1 | £77,183.60 |

### Key Findings

**1. Customer 14646 generated the highest gross revenue.**

This customer generated £280,206.02 across 73 distinct sales invoices.

**2. Customer 14911 recorded more invoices than the highest-revenue customer.**

Customer 14911 recorded 201 invoices but generated £143,711.17.

This shows that higher purchasing frequency does not necessarily translate into higher total spending.

**3. Customer 16446 generated substantial revenue from only two invoices.**

This customer generated £168,472.50 from two invoices, indicating unusually high invoice values.

### Business Interpretation

Customer value cannot be evaluated using purchase frequency alone.

A customer with relatively few invoices may generate more revenue than a customer who purchases frequently.

Combining purchasing frequency with monetary value can provide a stronger foundation for future customer segmentation.

**SQL implementation:** Query 6 in [sales_Analysis.sql](../sql/sales_Analysis.sql).

---

## 8. Overall Findings

The six SQL analyses provide an initial overview of sales performance, purchasing activity, product identifiers, customer countries, and identified customers.

| Metric | Finding |
|---|---|
| Total gross sales revenue | £10,642,110.80 |
| Highest-revenue month | November 2011 |
| Highest monthly invoice count | November 2011 |
| Highest average invoice value | December 2011 (partial month) |
| Highest-revenue StockCode | DOT |
| Highest-revenue customer country | United Kingdom |
| United Kingdom's share of gross revenue | Approximately 84.6% |
| Highest-revenue identified customer | Customer 14646 |
| Main driver of September–November revenue growth | Increased invoice volume |

### Main Business Takeaway

The retailer experienced strong revenue growth during September–November 2011, primarily associated with increasing invoice counts.

Sales revenue was heavily concentrated among customers residing in the United Kingdom.

Product and customer analyses also demonstrate that revenue, transaction frequency, and quantities sold provide different perspectives on business performance.

Together, these findings establish a foundation for an interactive business intelligence dashboard.

---

## 9. Analysis Limitations

The following limitations should be considered when interpreting the results:

1. **Historical data:** The dataset covers transactions from 2010–2011 and does not represent current retail conditions.
2. **Incomplete months:** December 2010 and December 2011 contain partial reporting periods.
3. **Gross revenue only:** The analyses exclude cancellations and other non-sale transaction types.
4. **Missing customer identifiers:** Some transactions cannot be associated with known customers.
5. **Invoice-based metrics:** Distinct invoice identifiers are used rather than transaction-line counts.
6. **No profit calculation:** Product costs and operating expenses are unavailable.
7. **Product-code limitations:** Some StockCodes may represent non-product charges, so the product ranking requires refinement before being interpreted as merchandise performance.
8. **Unusual transactions:** Large quantities and high-value invoices have not been individually validated.
9. **No causal conclusions:** Observed patterns do not independently establish why purchasing behavior changed.

---

## 10. Next Phase — Power BI Dashboard

The initial SQL analysis phase is complete.

The next phase will focus on building an interactive dashboard using Power BI Desktop.

### Planned Dashboard Features

- Gross sales revenue KPI
- Total sales invoices KPI
- Average invoice value KPI
- Monthly revenue trends
- Revenue by customer country
- Top StockCodes by gross revenue
- Top customers by gross revenue
- Interactive date and country filters

The dashboard will be connected to the MySQL database and will use the cleaned transaction data.

Product rankings will be labeled appropriately until non-merchandise codes are separated.

---

## 11. SQL Source Code

All six SQL queries are maintained in:

**[sql/sales_Analysis.sql](../sql/sales_Analysis.sql)**

The SQL file contains the executable queries, while this report documents their results, methodology, business interpretations, and limitations.