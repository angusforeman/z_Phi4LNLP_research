# Quick Start: Benchmarking Guide

## Running a Benchmark

```bash
# Option 1: Direct execution
cd /home/angusf/_source/z_Phi4LNLP_research
PYTHONPATH="$PWD/src" ./venv/bin/python src/benchmark.py

# Option 2: Using the helper script
./scripts/run_benchmark.sh
```

## Analyzing Results

```bash
# Analyze the most recent benchmark
./scripts/analyze_benchmark.sh logs/benchmark_results_TIMESTAMP.json

# Compare two benchmarks
./scripts/analyze_benchmark.sh logs/run1.json logs/run2.json
```

## Key Features

### 40 Test Queries

The benchmark includes queries for:
- Simple SELECT (5 queries)
- COUNT operations (5 queries)  
- WHERE filtering (5 queries)
- ORDER BY sorting (5 queries)
- Aggregates: SUM, AVG, MAX, MIN (5 queries)
- JOINs (5 queries)
- GROUP BY (5 queries)
- Complex queries (5 queries)

### Metrics Tracked

- **Response time** for each query
- **Success/failure** rate
- **SQL generation** accuracy
- **Performance percentiles** (P50, P90, P95)
- **Query complexity** analysis

### Output Formats

1. **Console output**: Real-time progress during benchmark
2. **JSON file**: Detailed results in `logs/benchmark_results_TIMESTAMP.json`
3. **Analysis report**: Statistical breakdown via analyze_benchmark.py

## Logging Options

Edit `.env` to configure logging:

```bash
# Text logs (human-readable)
LOG_OUTPUT=console  # or 'file'
LOG_LEVEL=INFO
LOG_FORMAT=text

# JSON logs (machine-readable for analysis)
LOG_OUTPUT=file
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Example Workflow

```bash
# 1. Run benchmark
./scripts/run_benchmark.sh

# 2. View the markdown report (automatically generated)
cat logs/benchmark_report_TIMESTAMP.md
# or open it in a markdown viewer

# 3. Analyze results in detail (optional)
./scripts/analyze_benchmark.sh logs/benchmark_results_20251108_164817.json

# 4. Make improvements to the system

# 5. Run benchmark again
./scripts/run_benchmark.sh

# 6. Compare markdown reports side-by-side
# Open both reports to compare visually
diff logs/benchmark_report_old.md logs/benchmark_report_new.md

# Or use the analysis tool
./scripts/analyze_benchmark.sh logs/old_results.json logs/new_results.json
```

## Understanding Results

### Success Rate
- **100%**: All queries translated successfully
- **<100%**: Review failed queries for patterns

### Average Time
- Baseline for comparing improvements
- Watch for regressions

### Percentiles
- **P50 (median)**: Typical performance
- **P90**: 90% of queries faster than this
- **P95**: Performance under load

### Standard Deviation
- Low: Consistent performance
- High: Variable performance (investigate outliers)

## Tips

1. **Run multiple times**: First run may be slower (cold start)
2. **Use JSON logs**: Easier to parse and analyze programmatically
3. **Track over time**: Keep results to monitor trends
4. **Focus on P95**: Represents worst-case user experience
5. **Check failed queries**: May indicate model limitations

## Files Generated

- `logs/benchmark_results_TIMESTAMP.json` - Detailed results (JSON)
- `logs/benchmark_report_TIMESTAMP.md` - Formatted report (Markdown)
- `logs/nl_to_sql.log` - Application logs (if LOG_OUTPUT=file)

The markdown reports are perfect for:
- Quick visual review of results
- Comparing multiple test runs side-by-side
- Sharing results with team members
- Tracking performance trends over time
