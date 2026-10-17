
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
