# Benchmark Report

**Generated:** 2025-11-08T16:48:17.913484
**Model:** phi4

## Summary

| Metric | Value |
|--------|-------|
| Total Queries | 40 |
| Successful | 40 (100.0%) |
| Failed | 0 |
| Total Time | 951.51s |

## Timing Statistics

| Metric | Time (seconds) |
|--------|----------------|
| Average (all queries) | 23.788s |
| Average (successful) | 23.788s |
| Median | 19.825s |
| Min | 12.818s |
| Max | 84.473s |
| Std Deviation | 13.810s |

## Performance Percentiles

| Percentile | Time (seconds) |
|------------|----------------|
| P50 (median) | 19.950s |
| P90 | 37.651s |
| P95 | 60.914s |

## Query Complexity Analysis

| Complexity | Count | Avg Time |
|------------|-------|----------|
| Short (<30 chars) | 18 | 20.030s |
| Medium (30-50 chars) | 21 | 26.135s |
| Long (>50 chars) | 1 | 42.145s |

## Fastest Queries

1. **12.818s** - list all products
   ```sql
   SELECT * FROM products;
   ```

2. **13.016s** - get all customer names
   ```sql
   SELECT name FROM customers;
   ```

3. **13.052s** - show me the products
   ```sql
   SELECT * FROM products;
   ```

4. **13.111s** - count all customers
   ```sql
   SELECT COUNT(*) FROM customers;
   ```

5. **13.917s** - display all orders
   ```sql
   SELECT * FROM orders;
   ```

## Slowest Queries

1. **84.473s** - show all customers
   ```sql
   SELECT * FROM customers;
   ```

2. **60.914s** - number of products per price range
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

3. **42.145s** - find the most expensive order with customer details
   ```sql
   SELECT c.id, c.name, c.email, o.id AS order_id, o.product_name, o.quantity, o.total_price, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id
ORDER BY o.total_price DESC
LIMIT 1;
   ```

4. **37.651s** - show products ordered by price descending
   ```sql
   SELECT name, price FROM products ORDER BY price DESC;
   ```

5. **34.078s** - show top 10 customers by total spending
   ```sql
   SELECT c.id, c.name, SUM(o.total_price) AS total_spending
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spending DESC
LIMIT 10;
   ```

## All Results

| # | Query | SQL | Duration | Status |
|---|-------|-----|----------|--------|
| 1 | show all customers | `SELECT * FROM customers;` | 84.473s | ✓ |
| 2 | list all products | `SELECT * FROM products;` | 12.818s | ✓ |
| 3 | display all orders | `SELECT * FROM orders;` | 13.917s | ✓ |
| 4 | get all customer names | `SELECT name FROM customers;` | 13.016s | ✓ |
| 5 | show me the products | `SELECT * FROM products;` | 13.052s | ✓ |
| 6 | count all customers | `SELECT COUNT(*) FROM customers;` | 13.111s | ✓ |
| 7 | how many orders are there | `SELECT COUNT(*) FROM orders;` | 14.123s | ✓ |
| 8 | count total products | `SELECT SUM(quantity) AS total_products F...` | 17.113s | ✓ |
| 9 | how many customers do we have | `SELECT COUNT(*) FROM customers;` | 14.142s | ✓ |
| 10 | total number of orders | `SELECT COUNT(*) AS total_number_of_order...` | 15.608s | ✓ |
| 11 | show customers with email containing gma... | `SELECT * FROM customers WHERE email LIKE...` | 16.780s | ✓ |
| 12 | find products with price greater than 10... | `SELECT * FROM products WHERE price > 100...` | 16.287s | ✓ |
| 13 | get orders from customer id 5 | `SELECT * FROM orders WHERE customer_id =...` | 17.071s | ✓ |
| 14 | list products that are out of stock | `SELECT name 
FROM products 
WHERE stock_...` | 21.847s | ✓ |
| 15 | show orders with quantity more than 10 | `SELECT * FROM orders WHERE quantity > 10...` | 16.958s | ✓ |
| 16 | list customers sorted by name | `SELECT * FROM customers ORDER BY name;` | 17.121s | ✓ |
| 17 | show products ordered by price descendin... | `SELECT name, price FROM products ORDER B...` | 37.651s | ✓ |
| 18 | display orders sorted by date | `SELECT * FROM orders ORDER BY order_date...` | 19.975s | ✓ |
| 19 | get customers ordered by creation date | `SELECT * FROM customers ORDER BY created...` | 21.952s | ✓ |
| 20 | show products from cheapest to most expe... | `SELECT name, price FROM products ORDER B...` | 19.700s | ✓ |
| 21 | what is the average product price | `SELECT AVG(price) AS average_product_pri...` | 16.183s | ✓ |
| 22 | sum of all order prices | `SELECT SUM(total_price) AS total_order_p...` | 17.095s | ✓ |
| 23 | find the maximum price in products | `SELECT MAX(price) FROM products;` | 15.387s | ✓ |
| 24 | minimum quantity in orders | `SELECT MIN(quantity) AS min_quantity FRO...` | 14.727s | ✓ |
| 25 | total revenue from all orders | `SELECT SUM(total_price) AS total_revenue...` | 16.143s | ✓ |
| 26 | show customer names with their orders | `SELECT c.name AS customer_name, o.produc...` | 28.994s | ✓ |
| 27 | list all orders with customer informatio... | `SELECT o.id AS order_id, c.name AS custo...` | 31.869s | ✓ |
| 28 | get customer email addresses for each or... | `SELECT c.email 
FROM orders o 
JOIN cust...` | 19.950s | ✓ |
| 29 | show which customers placed orders | `SELECT DISTINCT c.name, c.email 
FROM cu...` | 21.185s | ✓ |
| 30 | display orders along with customer names | `SELECT o.id AS order_id, c.name AS custo...` | 31.141s | ✓ |
| 31 | count orders per customer | `SELECT c.name, COUNT(o.id) AS order_coun...` | 24.950s | ✓ |
| 32 | total quantity ordered by each customer | `SELECT c.name, SUM(o.quantity) AS total_...` | 26.188s | ✓ |
| 33 | average order price per customer | `SELECT c.name, AVG(o.total_price) AS ave...` | 25.679s | ✓ |
| 34 | number of products per price range | `SELECT 
    CASE 
        WHEN p.price B...` | 60.914s | ✓ |
| 35 | sum of order totals grouped by customer | `SELECT c.name, SUM(o.total_price) AS tot...` | 26.289s | ✓ |
| 36 | find customers who ordered more than 5 i... | `SELECT DISTINCT c.id, c.name, c.email 
F...` | 26.371s | ✓ |
| 37 | show top 10 customers by total spending | `SELECT c.id, c.name, SUM(o.total_price) ...` | 34.078s | ✓ |
| 38 | list products never ordered | `SELECT p.name 
FROM products p
LEFT JOIN...` | 22.086s | ✓ |
| 39 | get customers who placed orders in the l... | `SELECT DISTINCT c.id, c.name, c.email 
F...` | 33.425s | ✓ |
| 40 | find the most expensive order with custo... | `SELECT c.id, c.name, c.email, o.id AS or...` | 42.145s | ✓ |

---

*Report generated by benchmark.py on 2025-11-08 at 16:56:39*