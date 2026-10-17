
-- ==================================================
-- E-COMMERCE SALES ANALYSIS
-- ==================================================

-- 1. Gross sales revenue
-- Includes only transactions classified as SALE.

SELECT
    ROUND(SUM(Quantity * UnitPrice), 2)
        AS GrossSalesRevenue
FROM transactions
WHERE TransactionType = 'SALE';


-- 2. Monthly gross sales revenue
-- Groups sales by calendar month.

SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS SalesMonth,
    COUNT(DISTINCT InvoiceNo) AS TotalInvoices,
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossRevenue
FROM transactions
WHERE TransactionType = 'SALE'
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY SalesMonth;


-- ==================================================
-- 3. AVERAGE INVOICE VALUE BY MONTH
-- ==================================================
-- Business question:
-- Is revenue growth driven by more invoices
-- or higher average spending per invoice?


SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS SalesMonth,
    COUNT(DISTINCT InvoiceNo) AS TotalInvoices,
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossRevenue,
    ROUND(
        SUM(Quantity * UnitPrice) /
        COUNT(DISTINCT InvoiceNo),
        2
    ) AS AvgInvoiceValue
FROM transactions
WHERE TransactionType = 'SALE'
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY SalesMonth;

-- ==================================================
-- 4. TOP 10 PRODUCTS BY GROSS REVENUE
-- ==================================================

SELECT
    StockCode,
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossRevenue,
    SUM(Quantity) AS UnitsSold,
    COUNT(DISTINCT InvoiceNo) AS InvoiceCount
FROM transactions
WHERE TransactionType = 'SALE'
GROUP BY StockCode
ORDER BY GrossRevenue DESC
LIMIT 10;


-- 5. TOP 10 COUNTRIES BY GROSS REVENUE

SELECT
    Country,
    COUNT(DISTINCT InvoiceNo) AS TotalInvoices,
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossRevenue
FROM transactions
WHERE TransactionType = 'SALE'
GROUP BY Country
ORDER BY GrossRevenue DESC
LIMIT 10;

-- ==================================================
-- 6. TOP 10 CUSTOMERS BY GROSS REVENUE
-- ==================================================

SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS TotalInvoices,
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossRevenue
FROM transactions
WHERE TransactionType = 'SALE'
  AND CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY GrossRevenue DESC
LIMIT 10;
