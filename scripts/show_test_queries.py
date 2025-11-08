#!/usr/bin/env python3
"""Display the benchmark test queries."""

# Test queries list - duplicated to avoid import issues
TEST_QUERIES = [
    # Simple SELECT queries
    "show all customers",
    "list all products",
    "display all orders",
    "get all customer names",
    "show me the products",
    
    # COUNT queries
    "count all customers",
    "how many orders are there",
    "count total products",
    "how many customers do we have",
    "total number of orders",
    
    # Filtering with WHERE
    "show customers with email containing gmail",
    "find products with price greater than 100",
    "get orders from customer id 5",
    "list products that are out of stock",
    "show orders with quantity more than 10",
    
    # Ordering and sorting
    "list customers sorted by name",
    "show products ordered by price descending",
    "display orders sorted by date",
    "get customers ordered by creation date",
    "show products from cheapest to most expensive",
    
    # Aggregate functions
    "what is the average product price",
    "sum of all order prices",
    "find the maximum price in products",
    "minimum quantity in orders",
    "total revenue from all orders",
    
    # JOINs
    "show customer names with their orders",
    "list all orders with customer information",
    "get customer email addresses for each order",
    "show which customers placed orders",
    "display orders along with customer names",
    
    # GROUP BY
    "count orders per customer",
    "total quantity ordered by each customer",
    "average order price per customer",
    "number of products per price range",
    "sum of order totals grouped by customer",
    
    # Complex queries
    "find customers who ordered more than 5 items",
    "show top 10 customers by total spending",
    "list products never ordered",
    "get customers who placed orders in the last month",
    "find the most expensive order with customer details",
]


def main():
    print(f"\n{'='*80}")
    print(f"BENCHMARK TEST QUERIES ({len(TEST_QUERIES)} total)")
    print(f"{'='*80}\n")
    
    categories = [
        ("Simple SELECT", 0, 5),
        ("COUNT Queries", 5, 10),
        ("Filtering with WHERE", 10, 15),
        ("Ordering and Sorting", 15, 20),
        ("Aggregate Functions", 20, 25),
        ("JOINs", 25, 30),
        ("GROUP BY", 30, 35),
        ("Complex Queries", 35, 40),
    ]
    
    for category, start, end in categories:
        print(f"{category}:")
        for i, query in enumerate(TEST_QUERIES[start:end], start + 1):
            print(f"  {i:2d}. {query}")
        print()
    
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
