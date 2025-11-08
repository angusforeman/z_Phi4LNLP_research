# Benchmark Report

**Generated:** 2025-11-08T17:15:38.503730
**Model:** phi4

## Summary

| Metric | Value |
|--------|-------|
| Total Queries | 40 |
| Successful | 40 (100.0%) |
| Failed | 0 |
| Total Time | 978.34s |

## Timing Statistics

| Metric | Time (seconds) |
|--------|----------------|
| Average (all queries) | 24.458s |
| Average (successful) | 24.458s |
| Median | 18.754s |
| Min | 12.127s |
| Max | 77.434s |
| Std Deviation | 13.635s |

## Performance Percentiles

| Percentile | Time (seconds) |
|------------|----------------|
| P50 (median) | 18.771s |
| P90 | 49.167s |
| P95 | 55.483s |

## Query Complexity Analysis

| Complexity | Count | Avg Time |
|------------|-------|----------|
| Short (<30 chars) | 18 | 20.822s |
| Medium (30-50 chars) | 21 | 26.388s |
| Long (>50 chars) | 1 | 49.395s |

## Fastest Queries

1. **12.127s** - list all products
   ```sql
   SELECT * FROM products;
   ```

2. **13.386s** - display all orders
   ```sql
   SELECT * FROM orders;
   ```

3. **13.574s** - show me the products
   ```sql
   SELECT * FROM products;
   ```

4. **14.090s** - get all customer names
   ```sql
   SELECT name FROM customers;
   ```

5. **15.090s** - count all customers
   ```sql
   SELECT COUNT(*) FROM customers;
   ```

## Slowest Queries

1. **77.434s** - show all customers
   ```sql
   SELECT * FROM customers;
   ```

2. **55.483s** - number of products per price range
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

3. **49.395s** - find the most expensive order with customer details
   ```sql
   SELECT c.id, c.name, c.email, o.id AS order_id, o.product_name, o.quantity, o.total_price, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id
ORDER BY o.total_price DESC
LIMIT 1;
   ```

4. **49.167s** - list all orders with customer information
   ```sql
   SELECT 
    o.id AS order_id,
    c.id AS customer_id,
    c.name AS customer_name,
    c.email AS customer_email,
    o.product_name,
    o.quantity,
    o.order_date,
    o.total_price
FROM 
    orders o
JOIN 
    customers c ON o.customer_id = c.id;
   ```

5. **41.709s** - show top 10 customers by total spending
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
| 1 | show all customers | `SELECT * FROM customers;` | 77.434s | ✓ |
| 2 | list all products | `SELECT * FROM products;` | 12.127s | ✓ |
| 3 | display all orders | `SELECT * FROM orders;` | 13.386s | ✓ |
| 4 | get all customer names | `SELECT name FROM customers;` | 14.090s | ✓ |
| 5 | show me the products | `SELECT * FROM products;` | 13.574s | ✓ |
| 6 | count all customers | `SELECT COUNT(*) FROM customers;` | 15.090s | ✓ |
| 7 | how many orders are there | `SELECT COUNT(*) FROM orders;` | 15.130s | ✓ |
| 8 | count total products | `SELECT SUM(quantity) AS total_products F...` | 16.452s | ✓ |
| 9 | how many customers do we have | `SELECT COUNT(*) FROM customers;` | 15.366s | ✓ |
| 10 | total number of orders | `SELECT COUNT(*) AS total_number_of_order...` | 16.666s | ✓ |
| 11 | show customers with email containing gma... | `SELECT * FROM customers WHERE email LIKE...` | 18.813s | ✓ |
| 12 | find products with price greater than 10... | `SELECT * FROM products WHERE price > 100...` | 17.661s | ✓ |
| 13 | get orders from customer id 5 | `SELECT * FROM orders WHERE customer_id =...` | 18.771s | ✓ |
| 14 | list products that are out of stock | `SELECT name 
FROM products 
WHERE stock_...` | 18.671s | ✓ |
| 15 | show orders with quantity more than 10 | `SELECT * FROM orders WHERE quantity > 10...` | 16.528s | ✓ |
| 16 | list customers sorted by name | `SELECT * FROM customers ORDER BY name;` | 16.583s | ✓ |
| 17 | show products ordered by price descendin... | `SELECT name, price 
FROM products 
ORDER...` | 16.881s | ✓ |
| 18 | display orders sorted by date | `SELECT * FROM orders ORDER BY order_date...` | 18.738s | ✓ |
| 19 | get customers ordered by creation date | `SELECT * FROM customers ORDER BY created...` | 16.191s | ✓ |
| 20 | show products from cheapest to most expe... | `SELECT name, price 
FROM products 
ORDER...` | 17.732s | ✓ |
| 21 | what is the average product price | `SELECT AVG(price) AS average_product_pri...` | 17.558s | ✓ |
| 22 | sum of all order prices | `SELECT SUM(total_price) AS total_order_p...` | 16.851s | ✓ |
| 23 | find the maximum price in products | `SELECT MAX(price) FROM products;` | 15.944s | ✓ |
| 24 | minimum quantity in orders | `SELECT MIN(quantity) AS min_quantity FRO...` | 26.153s | ✓ |
| 25 | total revenue from all orders | `SELECT SUM(total_price) AS total_revenue...` | 20.957s | ✓ |
| 26 | show customer names with their orders | `SELECT c.name AS customer_name, o.produc...` | 40.349s | ✓ |
| 27 | list all orders with customer informatio... | `SELECT 
    o.id AS order_id,
    c.id A...` | 49.167s | ✓ |
| 28 | get customer email addresses for each or... | `SELECT c.email 
FROM customers c 
JOIN o...` | 19.908s | ✓ |
| 29 | show which customers placed orders | `SELECT DISTINCT c.name, c.email 
FROM cu...` | 22.700s | ✓ |
| 30 | display orders along with customer names | `SELECT o.id AS order_id, c.name AS custo...` | 32.006s | ✓ |
| 31 | count orders per customer | `SELECT c.name, COUNT(o.id) AS order_coun...` | 23.736s | ✓ |
| 32 | total quantity ordered by each customer | `SELECT c.name, SUM(o.quantity) AS total_...` | 26.109s | ✓ |
| 33 | average order price per customer | `SELECT c.name, AVG(o.total_price) AS ave...` | 25.445s | ✓ |
| 34 | number of products per price range | `SELECT 
    CASE 
        WHEN p.price B...` | 55.483s | ✓ |
| 35 | sum of order totals grouped by customer | `SELECT c.name, SUM(o.total_price) AS tot...` | 26.839s | ✓ |
| 36 | find customers who ordered more than 5 i... | `SELECT DISTINCT c.id, c.name, c.email 
F...` | 26.616s | ✓ |
| 37 | show top 10 customers by total spending | `SELECT c.id, c.name, SUM(o.total_price) ...` | 41.709s | ✓ |
| 38 | list products never ordered | `SELECT p.name 
FROM products p
LEFT JOIN...` | 23.689s | ✓ |
| 39 | get customers who placed orders in the l... | `SELECT DISTINCT c.id, c.name, c.email 
F...` | 31.837s | ✓ |
| 40 | find the most expensive order with custo... | `SELECT c.id, c.name, c.email, o.id AS or...` | 49.395s | ✓ |

---

*Report generated by benchmark.py on 2025-11-08 at 17:15:38*