# Benchmark Report

**Generated:** 2025-11-08T17:44:04.229306
**Model:** phi4

## Summary

| Metric | Value |
|--------|-------|
| Total Queries | 40 |
| Successful | 40 (100.0%) |
| Failed | 0 |
| Total Time | 949.73s |

## Timing Statistics

| Metric | Time (seconds) |
|--------|----------------|
| Average (all queries) | 23.743s |
| Average (successful) | 23.743s |
| Median | 19.020s |
| Min | 14.022s |
| Max | 86.485s |
| Std Deviation | 13.221s |

## Performance Percentiles

| Percentile | Time (seconds) |
|------------|----------------|
| P50 (median) | 19.028s |
| P90 | 34.579s |
| P95 | 54.823s |

## Query Complexity Analysis

| Complexity | Count | Avg Time |
|------------|-------|----------|
| Short (<30 chars) | 18 | 21.019s |
| Medium (30-50 chars) | 21 | 25.562s |
| Long (>50 chars) | 1 | 34.579s |

## Fastest Queries

1. **14.022s** - display all orders
   ```sql
   SELECT * FROM orders;
   ```

2. **14.749s** - show me the products
   ```sql
   SELECT * FROM products;
   ```

3. **14.864s** - get all customer names
   ```sql
   SELECT name FROM customers;
   ```

4. **14.879s** - get customers ordered by creation date
   ```sql
   SELECT * FROM customers ORDER BY created_at;
   ```

5. **15.072s** - count all customers
   ```sql
   SELECT COUNT(*) FROM customers;
   ```

## Slowest Queries

1. **86.485s** - show all customers
   ```sql
   SELECT * FROM customers;
   ```

2. **54.823s** - number of products per price range
   ```sql
   SELECT 
    CASE 
        WHEN p.price BETWEEN 0 AND 99.99 THEN '0-99.99'
        WHEN p.price BETWEEN 100 AND 199.99 THEN '100-199.99'
        WHEN p.price BETWEEN 200 AND 299.99 THEN '200-299.99'
        ELSE '300+' 
    END AS price_range,
    COUNT(p.id) AS product_count
FROM 
    products p
GROUP BY 
    price_range;
   ```

3. **39.595s** - list all orders with customer information
   ```sql
   SELECT o.id AS order_id, c.name AS customer_name, c.email AS customer_email, o.product_name, o.quantity, o.order_date, o.total_price 
FROM orders o
JOIN customers c ON o.customer_id = c.id;
   ```

4. **34.579s** - find the most expensive order with customer details
   ```sql
   SELECT c.id, c.name, c.email, o.id AS order_id, o.product_name, o.quantity, o.total_price, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id
ORDER BY o.total_price DESC
LIMIT 1;
   ```

5. **33.863s** - display orders along with customer names
   ```sql
   SELECT o.id AS order_id, c.name AS customer_name, o.product_name, o.quantity, o.order_date, o.total_price 
FROM orders o 
JOIN customers c ON o.customer_id = c.id;
   ```

## All Results

| # | Query | SQL | Duration | Status |
|---|-------|-----|----------|--------|
| 1 | show all customers | `SELECT * FROM customers;` | 86.485s | ✓ |
| 2 | list all products | `SELECT * FROM products;` | 15.388s | ✓ |
| 3 | display all orders | `SELECT * FROM orders;` | 14.022s | ✓ |
| 4 | get all customer names | `SELECT name FROM customers;` | 14.864s | ✓ |
| 5 | show me the products | `SELECT * FROM products;` | 14.749s | ✓ |
| 6 | count all customers | `SELECT COUNT(*) FROM customers;` | 15.072s | ✓ |
| 7 | how many orders are there | `SELECT COUNT(*) FROM orders;` | 16.275s | ✓ |
| 8 | count total products | `SELECT SUM(quantity) AS total_products F...` | 16.639s | ✓ |
| 9 | how many customers do we have | `SELECT COUNT(*) FROM customers;` | 15.415s | ✓ |
| 10 | total number of orders | `SELECT COUNT(*) AS total_number_of_order...` | 18.567s | ✓ |
| 11 | show customers with email containing gma... | `SELECT * FROM customers WHERE email LIKE...` | 18.620s | ✓ |
| 12 | find products with price greater than 10... | `SELECT * FROM products WHERE price > 100...` | 18.833s | ✓ |
| 13 | get orders from customer id 5 | `SELECT * FROM orders WHERE customer_id =...` | 19.012s | ✓ |
| 14 | list products that are out of stock | `SELECT name 
FROM products 
WHERE stock_...` | 19.857s | ✓ |
| 15 | show orders with quantity more than 10 | `SELECT * FROM orders WHERE quantity > 10...` | 18.790s | ✓ |
| 16 | list customers sorted by name | `SELECT * FROM customers ORDER BY name;` | 16.028s | ✓ |
| 17 | show products ordered by price descendin... | `SELECT name, price 
FROM products 
ORDER...` | 17.763s | ✓ |
| 18 | display orders sorted by date | `SELECT * FROM orders ORDER BY order_date...` | 15.487s | ✓ |
| 19 | get customers ordered by creation date | `SELECT * FROM customers ORDER BY created...` | 14.879s | ✓ |
| 20 | show products from cheapest to most expe... | `SELECT name, price 
FROM products 
ORDER...` | 17.689s | ✓ |
| 21 | what is the average product price | `SELECT AVG(price) AS average_product_pri...` | 20.565s | ✓ |
| 22 | sum of all order prices | `SELECT SUM(total_price) AS total_order_p...` | 19.028s | ✓ |
| 23 | find the maximum price in products | `SELECT MAX(price) FROM products;` | 15.079s | ✓ |
| 24 | minimum quantity in orders | `SELECT MIN(quantity) AS min_quantity FRO...` | 15.488s | ✓ |
| 25 | total revenue from all orders | `SELECT SUM(total_price) AS total_revenue...` | 19.435s | ✓ |
| 26 | show customer names with their orders | `SELECT c.name AS customer_name, o.produc...` | 33.252s | ✓ |
| 27 | list all orders with customer informatio... | `SELECT o.id AS order_id, c.name AS custo...` | 39.595s | ✓ |
| 28 | get customer email addresses for each or... | `SELECT c.email 
FROM customers c
JOIN or...` | 25.398s | ✓ |
| 29 | show which customers placed orders | `SELECT DISTINCT c.name, c.email 
FROM cu...` | 21.841s | ✓ |
| 30 | display orders along with customer names | `SELECT o.id AS order_id, c.name AS custo...` | 33.863s | ✓ |
| 31 | count orders per customer | `SELECT c.name, COUNT(o.id) AS order_coun...` | 24.863s | ✓ |
| 32 | total quantity ordered by each customer | `SELECT c.name, SUM(o.quantity) AS total_...` | 24.754s | ✓ |
| 33 | average order price per customer | `SELECT c.name, AVG(o.total_price) AS ave...` | 25.802s | ✓ |
| 34 | number of products per price range | `SELECT 
    CASE 
        WHEN p.price B...` | 54.823s | ✓ |
| 35 | sum of order totals grouped by customer | `SELECT c.name, SUM(o.total_price) AS tot...` | 24.917s | ✓ |
| 36 | find customers who ordered more than 5 i... | `SELECT DISTINCT c.id, c.name, c.email 
F...` | 26.285s | ✓ |
| 37 | show top 10 customers by total spending | `SELECT c.id, c.name, SUM(o.total_price) ...` | 32.881s | ✓ |
| 38 | list products never ordered | `SELECT p.name 
FROM products p
LEFT JOIN...` | 21.521s | ✓ |
| 39 | get customers who placed orders in the l... | `SELECT DISTINCT c.id, c.name, c.email 
F...` | 31.324s | ✓ |
| 40 | find the most expensive order with custo... | `SELECT c.id, c.name, c.email, o.id AS or...` | 34.579s | ✓ |

---

*Report generated by benchmark.py on 2025-11-08 at 17:44:04*