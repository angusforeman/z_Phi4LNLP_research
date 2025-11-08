# Benchmarking and Performance Testing

This directory contains tools for testing and analyzing the performance of the NL-to-SQL translator.

## Running Benchmarks

### Basic Benchmark

Run the benchmark suite with 40 pre-defined test queries:

```bash
./venv/bin/python src/benchmark.py
```

This will:
- Execute 40 diverse English language queries
- Measure response time for each query
- Display real-time progress
- Save detailed results to `logs/benchmark_results_TIMESTAMP.json`
- Print a summary of results

### Sample Output

```
======================================================================
Starting benchmark with 40 queries using model: phi4
======================================================================

[1/40] Testing: show all customers
  ✓ Success (4.234s)
  SQL: SELECT * FROM customers;

[2/40] Testing: list all products
  ✓ Success (3.891s)
  SQL: SELECT * FROM products;
...

======================================================================
BENCHMARK SUMMARY
======================================================================
Total queries:          40
Successful:             38 (95.0%)
Failed:                 2 (5.0%)

Timing Statistics:
Total time:             182.456s
Average time (all):     4.561s
Average time (success): 4.458s
Min time:               3.124s
Max time:               9.234s
======================================================================

Results saved to: logs/benchmark_results_20241108_161234.json
Markdown report: logs/benchmark_report_20241108_161234.md
```

## Analyzing Results

### Analyze a Single Run

```bash
./venv/bin/python src/analyze_benchmark.py logs/benchmark_results_20241108_161234.json
```

This provides:
- Overall success rate
- Detailed timing statistics (mean, median, std dev)
- Performance percentiles (P50, P90, P95)
- Query complexity analysis
- Fastest and slowest queries
- Failed query details

### Compare Two Runs

```bash
./venv/bin/python src/analyze_benchmark.py logs/run1.json logs/run2.json
```

This compares:
- Success rates
- Average response times
- Performance improvements/regressions

## Test Query Categories

The 40 test queries cover:

1. **Simple SELECT** (5 queries)
   - Basic table retrievals
   - Column selection

2. **COUNT Operations** (5 queries)
   - Counting records
   - Total calculations

3. **Filtering with WHERE** (5 queries)
   - Conditional queries
   - Comparison operators

4. **Ordering and Sorting** (5 queries)
   - ASC/DESC ordering
   - Multiple sort criteria

5. **Aggregate Functions** (5 queries)
   - SUM, AVG, MAX, MIN
   - Statistical operations

6. **JOINs** (5 queries)
   - Customer-order relationships
   - Multi-table queries

7. **GROUP BY** (5 queries)
   - Grouped aggregations
   - Per-customer statistics

8. **Complex Queries** (5 queries)
   - Nested conditions
   - Advanced filtering
   - Top-N queries

## Logging Configuration

### Standard Logging

For human-readable logs (default):

```bash
# .env
LOG_OUTPUT=console  # or 'file' for logs/nl_to_sql.log
LOG_LEVEL=INFO
LOG_FORMAT=text
```

### JSON Logging for Analysis

For structured, machine-readable logs:

```bash
# .env
LOG_OUTPUT=file
LOG_LEVEL=INFO
LOG_FORMAT=json
```

JSON logs include:
- `timestamp`: ISO 8601 timestamp
- `level`: Log level
- `message`: Log message
- `duration_seconds`: Query execution time
- `sql_length`: Generated SQL length
- `model`: Model name used

### Example JSON Log Entry

```json
{
  "timestamp": "2024-11-08T16:14:54.123456",
  "level": "INFO",
  "logger": "nl_to_sql",
  "message": "Phi4 model call completed in 4.606 seconds",
  "duration_seconds": 4.606,
  "model": "phi4"
}
```

## Performance Metrics

Key metrics tracked:

- **Response Time**: Time from query submission to SQL generation
- **Success Rate**: Percentage of queries successfully translated
- **Query Complexity**: Analysis based on query length and structure
- **Percentiles**: P50, P90, P95 response times

## Customizing Tests

Edit `src/benchmark.py` to modify the `TEST_QUERIES` list:

```python
TEST_QUERIES = [
    "your custom query here",
    "another test query",
    # ... add more queries
]
```

## Output Files

All results are saved in the `logs/` directory:

- `benchmark_results_TIMESTAMP.json` - Detailed benchmark data (machine-readable)
- `benchmark_report_TIMESTAMP.md` - Formatted markdown report (human-readable)
- `nl_to_sql.log` - Application logs (when LOG_OUTPUT=file)

### Markdown Reports

Each benchmark run automatically generates a timestamped markdown report containing:
- Summary statistics and success rates
- Timing analysis with percentiles (P50, P90, P95)
- Query complexity breakdown
- Top 5 fastest and slowest queries with SQL
- Complete results table
- Failed query details (if any)

These reports can be easily viewed, compared, and tracked over time.

### Benchmark JSON Structure

```json
{
  "metadata": {
    "timestamp": "ISO 8601 timestamp",
    "total_queries": 40,
    "successful": 38,
    "failed": 2,
    "success_rate": 95.0
  },
  "statistics": {
    "total_time_seconds": 182.456,
    "average_time_seconds": 4.561,
    "average_success_time_seconds": 4.458,
    "min_time_seconds": 3.124,
    "max_time_seconds": 9.234
  },
  "results": [
    {
      "timestamp": "ISO 8601",
      "query": "show all customers",
      "sql": "SELECT * FROM customers;",
      "success": true,
      "duration_seconds": 4.234,
      "error": null
    }
    // ... more results
  ]
}
```

## Tips

- Run benchmarks multiple times to account for variability
- Use JSON logging for automated analysis
- Compare results before/after model changes
- Monitor P95 times for worst-case performance
- Check failed queries for common patterns
