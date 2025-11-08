# Natural Language to SQL Translation

Research spike using Microsoft Phi4 model running locally via Ollama to translate English queries to SQL.

## Overview

This proof-of-concept demonstrates natural language to SQL translation using:
- **Phi4 model**: Runs locally via Ollama
- **Predefined schema**: E-commerce database (customers, orders, products)
- **Python 3.11+**: Minimal dependencies

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed
- 8GB+ RAM

### Setup

1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Pull Phi4 model:
```bash
ollama pull phi4
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Verify setup:
```bash
ollama list  # Should show phi4
python -c "import ollama; print('Ready')"
```

### Usage

Translate natural language to SQL:

```bash
python src/cli.py "show all customers"
```

Example queries:
```bash
python src/cli.py "list all products"
python src/cli.py "count total orders"
python src/cli.py "show customers with their order count"
```

## Benchmarking
The benchamrk will run 40 queries and record the statistics and timings into ./logs/benchmark_report_<timestanmp>.md
```bash
 ./scripts/run_benchmark.sh 
```


## Predefined Schema

The system uses a fixed e-commerce schema:

- **customers**: id, name, email, created_at
- **orders**: id, customer_id, product_name, quantity, order_date, total_price
- **products**: id, name, price, stock_quantity

## Testing

Run minimal test suite:

```bash
pytest tests/
```

Expected: 3 tests pass (model connection, basic translation, schema context)

## Project Structure

```
src/
├── schema.py           # Predefined schema
├── prompt_builder.py   # Prompt construction
├── translator.py       # Ollama client wrapper
└── cli.py              # Command-line interface

tests/
├── test_model_connection.py
├── test_basic_translation.py
└── test_schema_context.py
```

## Performance

- Target: <5 seconds for 95% of queries
- First query may take 3-5 seconds (cold start)
- Memory: 4-8GB during inference

## Limitations

This is a research spike with:
- Single predefined schema only
- Basic error handling
- Minimal test coverage
- No SQL execution validation

See `specs/001-nl-to-sql/` for full documentation.
