"""Quick test of llama.cpp performance with multiple queries."""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from llama_cpp_translator import LlamaCppTranslator

def main():
    MODEL_PATH = os.path.expanduser("~/.ollama/models/phi-2.Q4_K_M.gguf")
    
    print("Initializing llama.cpp translator...")
    translator = LlamaCppTranslator(
        model_path=MODEL_PATH,
        n_gpu_layers=-1,
        verbose=False
    )
    
    schema = """-- Database Schema
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  product_name VARCHAR(200),
  quantity INTEGER,
  order_date DATE NOT NULL,
  total_price DECIMAL(10,2)
);

-- Relationships
-- orders.customer_id -> customers.id"""
    
    test_queries = [
        "show all customers",
        "count total orders",
        "list customers who placed orders",
        "show orders from last 30 days",
        "find the top 5 customers by total spending"
    ]
    
    print(f"\nTesting {len(test_queries)} queries...")
    print("=" * 70)
    
    times = []
    for i, query in enumerate(test_queries, 1):
        prompt = f"""You are a SQL expert. Given the following database schema, convert the natural language query to a valid SQL statement.

{schema}

Natural language query: {query}

Generate ONLY the SQL query without any explanation or markdown formatting. Return just the SQL statement.

SQL:"""
        
        print(f"\n{i}. {query}")
        result = translator.translate(prompt)
        
        if result.success:
            print(f"   ✓ {result.response_time:.2f}s")
            print(f"   SQL: {result.sql_query}")
            times.append(result.response_time)
        else:
            print(f"   ✗ Failed: {result.error_message}")
    
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    if times:
        avg = sum(times) / len(times)
        print(f"Average time: {avg:.2f}s")
        print(f"Min time:     {min(times):.2f}s")
        print(f"Max time:     {max(times):.2f}s")
        print(f"\nOllama baseline: 23.8s")
        print(f"llama.cpp:       {avg:.2f}s")
        print(f"Speedup:         {23.8/avg:.1f}x faster! 🚀")

if __name__ == "__main__":
    main()
