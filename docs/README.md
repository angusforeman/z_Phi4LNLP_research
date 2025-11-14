# Documentation Index

## Getting Started
- [README](../README.md) - Project overview and quick start
- [Overview](./overview.md) - Detailed project overview

## Benchmarking & Testing
- [Benchmark Quick Start](./benchmark-quickstart.md) - Quick reference for running benchmarks
- [Benchmarking Guide](./benchmarking.md) - Comprehensive benchmarking documentation
- [Markdown Reports](./markdown-reports.md) - Guide to benchmark markdown reports
- [Benchmark Summary](./benchmark-summary.md) - Overview of benchmarking features

## Performance Optimization
- 🔥 [Performance Quick Reference](./performance_quick_reference.md) - **START HERE** - Quick wins for 46x speedup
- 📊 [Performance Considerations](./performance_considerations.md) - Detailed performance analysis and optimization strategies

## Project Specifications
Located in `specs/001-nl-to-sql/`:
- [Plan](../specs/001-nl-to-sql/plan.md) - Project plan
- [Specification](../specs/001-nl-to-sql/spec.md) - Technical specification
- [Data Model](../specs/001-nl-to-sql/data-model.md) - Database schema
- [Tasks](../specs/001-nl-to-sql/tasks.md) - Task breakdown
- [Quickstart](../specs/001-nl-to-sql/quickstart.md) - Quick setup guide
- [Research](../specs/001-nl-to-sql/research.md) - Research notes

## Key Findings

### Current Performance
- **Average query time:** 23.8 seconds
- **P95 latency:** 60.9 seconds
- **Status:** Too slow for production use ❌

### Recommended Improvements
1. **Groq API Integration** - 46x speedup (23s → 0.5s)
2. **Query Caching** - Additional 1.4x improvement
3. **Model Keep-Alive** - Eliminate cold starts

**Combined Impact:** 0.3-0.5s average response time ✅

### Benchmark Results
- **40 test queries** covering all SQL operations
- **100% success rate** with Phi4
- **Detailed metrics:** P50, P90, P95, complexity analysis
- **Output formats:** JSON + Markdown reports

## Quick Links

| Need to... | Go to... |
|------------|----------|
| Run a benchmark | [Benchmark Quick Start](./benchmark-quickstart.md) |
| Improve performance | [Performance Quick Reference](./performance_quick_reference.md) |
| Understand current metrics | [Benchmark Report](../logs/benchmark_report_20251108_164817.md) |
| Learn about markdown reports | [Markdown Reports Guide](./markdown-reports.md) |
| See detailed optimization plan | [Performance Considerations](./performance_considerations.md) |

## Document Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| Performance Quick Reference | ✅ Current | Nov 8, 2025 |
| Performance Considerations | ✅ Current | Nov 8, 2025 |
| Benchmark Quick Start | ✅ Current | Nov 8, 2025 |
| Benchmarking Guide | ✅ Current | Nov 8, 2025 |
| Markdown Reports | ✅ Current | Nov 8, 2025 |

---

*For questions or updates to this documentation, please contact the project team.*
