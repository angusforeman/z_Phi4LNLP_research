# Quickstart Guide: Natural Language to SQL

**Feature**: 001-nl-to-sql  
**Updated**: 2025-11-07

## Prerequisites

- Linux/WSL environment
- Python 3.11 or higher
- At least 8GB available RAM
- Internet connection (for initial setup only)

## Setup Instructions

### 1. Install Ollama

Download and install Ollama binary:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify installation:

```bash
ollama --version
```

Expected output: `ollama version 0.x.x` or similar

---

### 2. Pull Phi4 Model

Download the Phi4 model to Ollama:

```bash
ollama pull phi4
```

This will download several GB of data. Wait for completion.

Verify the model is available:

```bash
ollama list
```

You should see `phi4` in the list.

---

### 3. Test Model Response

Verify Phi4 responds correctly:

```bash
ollama run phi4 "Say hello"
```

Expected: The model should generate a response (not an error).

Press `Ctrl+D` or type `/bye` to exit the interactive mode.

---

### 4. Install Python Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

This installs:
- `ollama-python`: API client for Ollama
- `pytest`: Testing framework

---

### 5. Verify Python Client

Test the Ollama Python client:

```bash
python -c "import ollama; print('Ollama client installed:', ollama.__version__)"
```

Expected output: `Ollama client installed: 0.x.x`

---

## Running the Tool

### Basic Usage

Translate a natural language query to SQL:

```bash
python src/cli.py "show all customers"
```

Expected output:
```sql
SELECT * FROM customers;
```

---

### Example Queries

Try these example queries against the predefined schema:

```bash
# Simple queries
python src/cli.py "list all products"
python src/cli.py "show customer names and emails"

# Filtering
python src/cli.py "find orders from yesterday"
python src/cli.py "show products with price less than 50"

# Aggregation
python src/cli.py "count total orders"
python src/cli.py "what is the average order total"

# Joins
python src/cli.py "show customer names with their order count"
python src/cli.py "list orders with customer email addresses"
```

---

## Predefined Schema

The tool uses this predefined e-commerce schema:

```sql
-- Customers
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

-- Orders
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  product_name VARCHAR(200),
  quantity INTEGER,
  order_date DATE NOT NULL,
  total_price DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Products
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock_quantity INTEGER
);
```

---

## Running Tests

Execute the minimal test suite:

```bash
pytest tests/
```

Expected: 3 tests pass (model connection, basic translation, schema context)

---

## Troubleshooting

### Model Not Found

**Error**: `Error: model 'phi4' not found`

**Solution**: Run `ollama pull phi4` and wait for download to complete

---

### Ollama Service Not Running

**Error**: Connection refused or timeout

**Solution**: 
```bash
# Check if Ollama is running
ollama list

# If not, restart the service (it should auto-start on install)
# On systemd systems:
sudo systemctl restart ollama
```

---

### Slow Response Times

**Issue**: Queries take longer than 5 seconds

**Expected Behavior**: First query after model load may take 3-5 seconds (cold start). Subsequent queries should be faster (1-3 seconds).

**If consistently slow**:
- Check available RAM (model needs ~4-8GB)
- Close other memory-intensive applications
- Note: This is acceptable for research spike, document actual performance

---

### Invalid SQL Generated

**Issue**: Generated SQL has syntax errors

**Expected Behavior**: For research spike, ~80% accuracy on simple queries is acceptable (per spec SC-001)

**Action**: Document the query and generated SQL as a known limitation. Research spikes are for validation, not production quality.

---

## Performance Expectations

Based on research (see `research.md`):

- **Cold start**: 2-5 seconds (first query)
- **Warm queries**: 1-3 seconds
- **Memory usage**: 4-8GB RAM
- **CPU usage**: May spike to 100% during inference (normal)

---

## Next Steps

After verifying setup:

1. Try translating various natural language queries
2. Observe which query types work well vs. poorly
3. Document findings for future iterations
4. If concept is validated, consider next steps from spec (complex queries, error handling)

---

## Cleanup

To remove the Phi4 model and free up disk space:

```bash
ollama rm phi4
```

To uninstall Ollama:

```bash
# On Linux
sudo rm $(which ollama)
sudo rm -rf /usr/share/ollama
```
