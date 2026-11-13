
-- 1. Category-wise sales and profitability
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC;


-- 2. Regional performance ranking
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin
FROM superstore
GROUP BY Region
ORDER BY Profit_Margin DESC;


-- 3. Top 10 loss-making products
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Total_Loss
FROM superstore
GROUP BY "Product Name"
HAVING SUM(Profit) < 0
ORDER BY Total_Loss ASC
LIMIT 10;


-- 4. Discount impact
SELECT
    Discount,
    COUNT(*) AS Transactions,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM superstore
GROUP BY Discount
ORDER BY Discount;


-- 5. Monthly revenue trend
SELECT
    strftime('%Y-%m', "Order Date") AS Month,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM superstore
GROUP BY Month
ORDER BY Month;


-- 6. Top 10 customers by revenue
SELECT
    "Customer Name",
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM superstore
GROUP BY "Customer Name"
ORDER BY Revenue DESC
LIMIT 10;
