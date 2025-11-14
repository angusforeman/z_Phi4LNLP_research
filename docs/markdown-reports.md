# Markdown Benchmark Reports

## Overview

Every benchmark run automatically generates **two output files**:

1. **JSON** (`benchmark_results_TIMESTAMP.json`) - Machine-readable detailed data
2. **Markdown** (`benchmark_report_TIMESTAMP.md`) - Human-readable formatted report

## What's in the Markdown Report?

Each timestamped markdown report includes:

### 📊 Summary Section
- Total queries executed
- Success/failure counts and percentages
- Total execution time

### ⏱️ Timing Statistics
- Average time (all queries)
- Average time (successful only)
- Median response time
- Min and max times
- Standard deviation (consistency metric)

### 📈 Performance Percentiles
- P50 (median) - typical performance
- P90 - 90% of queries faster than this
- P95 - performance under load

### 🔍 Query Complexity Analysis
- Breakdown by query length (short/medium/long)
- Average time for each complexity level
- Query count per category

### 🚀 Top 5 Fastest Queries
- Response times
- Query text
- Generated SQL (with syntax highlighting)

### 🐌 Top 5 Slowest Queries
- Response times
- Query text
- Generated SQL (with syntax highlighting)

### ❌ Failed Queries (if any)
- Error messages
- Duration before failure

### 📋 Complete Results Table
- All 40 queries in a sortable table
- Query text, SQL preview, duration, status

## Usage

### Automatic Generation

Reports are created automatically when you run benchmarks:

```bash
./scripts/run_benchmark.sh
# Outputs:
# - logs/benchmark_results_20251108_164817.json
# - logs/benchmark_report_20251108_164817.md  ← NEW!
```

### Manual Generation from Existing JSON

Convert any existing JSON benchmark result to markdown:

```bash
cd /home/angusf/_source/z_Phi4LNLP_research
PYTHONPATH=src ./venv/bin/python scripts/json_to_markdown.py \
  logs/benchmark_results_20251108_164817.json

# Output: logs/benchmark_report_20251108_164817.md
```

### Viewing Reports

```bash
# In terminal
cat logs/benchmark_report_TIMESTAMP.md

# In VS Code
code logs/benchmark_report_TIMESTAMP.md

# In browser (via markdown preview extension)
# Or any markdown viewer
```

## Comparing Multiple Reports

Keep timestamped reports to track performance over time:

```bash
# List all reports
ls -lt logs/benchmark_report_*.md

# Compare two reports visually
diff logs/benchmark_report_20251108_120000.md \
     logs/benchmark_report_20251108_150000.md

# Or open both in your editor and view side-by-side
```

## Benefits

### ✅ Quick Visual Review
- Scan results at a glance
- No need to parse JSON
- Tables and formatting make trends obvious

### ✅ Easy Sharing
- Send to team members
- Include in documentation
- Attach to pull requests

### ✅ Version Control Friendly
- Text-based format
- Easy to diff between versions
- Can commit to git for historical tracking

### ✅ Multiple Reports for Comparison
- Each run gets a unique timestamp
- No overwriting previous results
- Build up a performance history

## Example Report Structure

```markdown
# Benchmark Report

**Generated:** 2025-11-08T16:48:17.913484
**Model:** phi4

## Summary
| Metric | Value |
|--------|-------|
| Total Queries | 40 |
| Successful | 40 (100.0%) |
| Total Time | 951.51s |

## Timing Statistics
| Metric | Time (seconds) |
|--------|----------------|
| Average (all queries) | 23.788s |
| Median | 19.825s |
...
```

## Use Cases

### 1. Performance Tracking
Keep reports over time to monitor improvements or regressions:
```
logs/benchmark_report_20251101_*.md  # Baseline
logs/benchmark_report_20251108_*.md  # After optimization
logs/benchmark_report_20251115_*.md  # After model update
```

### 2. Model Comparison
Test different models and compare results:
```
phi4_report.md
llama_report.md
mistral_report.md
```

### 3. Regression Testing
Run before/after changes to ensure no performance loss.

### 4. Documentation
Include reports in project documentation to show performance characteristics.

## File Naming Convention

Format: `benchmark_report_YYYYMMDD_HHMMSS.md`

Example: `benchmark_report_20251108_164817.md`
- Date: November 8, 2025
- Time: 16:48:17 (4:48:17 PM)

This ensures:
- Chronological sorting
- No name conflicts
- Easy identification

## Tips

1. **Keep multiple reports** - Don't delete old ones, track trends
2. **Add to .gitignore** - Or commit selected reports as baselines
3. **Use descriptive filenames** - Rename important runs:
   ```bash
   mv logs/benchmark_report_20251108_164817.md \
      logs/benchmark_report_baseline_phi4.md
   ```
4. **Review regularly** - Check P95 times and failed queries

---

**Related Files:**
- `src/benchmark.py` - Main benchmark script
- `scripts/json_to_markdown.py` - JSON to markdown converter
- `docs/benchmarking.md` - Complete benchmarking guide
