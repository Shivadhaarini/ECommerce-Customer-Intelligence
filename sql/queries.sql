-- 1. Total number of customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- 3. Order status distribution
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 4. Delivered-order revenue
SELECT ROUND(SUM(order_amount), 2) AS delivered_revenue
FROM orders
WHERE status = 'Delivered';

-- 5. Monthly order volume
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;
-- 6. Monthly delivered-order revenue
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(order_amount), 2) AS delivered_revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY month
ORDER BY month;
-- 7. Revenue by product category
SELECT
    p.category,
    ROUND(SUM(o.order_amount), 2) AS delivered_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY delivered_revenue DESC;
-- 8. Top 10 customers by delivered-order spending
SELECT
    c.customer_id,
    c.name,
    c.region,
    ROUND(SUM(o.order_amount), 2) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_id, c.name, c.region
ORDER BY total_spending DESC
LIMIT 10;
-- 9. Delivered-order revenue by region
SELECT
    c.region,
    ROUND(SUM(o.order_amount), 2) AS delivered_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.region
ORDER BY delivered_revenue DESC;
-- 10. Customers who have never placed an order
SELECT
    c.customer_id,
    c.name,
    c.region
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;
-- 11. Average delivered-order value by region
SELECT
    c.region,
    ROUND(AVG(o.order_amount), 2) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.region
ORDER BY average_order_value DESC;
-- 12. Top 10 products by delivered revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(o.order_amount), 2) AS delivered_revenue
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY delivered_revenue DESC
LIMIT 10;
-- 13. Order count and value by status
SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(order_amount), 2) AS total_order_value
FROM orders
GROUP BY status
ORDER BY order_count DESC;
-- 14. Total items sold by product category
SELECT
    p.category,
    SUM(o.quantity) AS total_items_sold
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY total_items_sold DESC;