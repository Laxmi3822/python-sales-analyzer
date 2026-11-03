-- 1. Display all sales records

SELECT * FROM sales;


-- 2. Find total revenue

SELECT SUM(quantity * price)
FROM sales;


-- 3. Find the highest revenue product

SELECT
    product,
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 1;


-- 4. Find total units sold

SELECT SUM(quantity)
FROM sales;


-- 5. Display product-wise revenue

SELECT
    product,
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product;