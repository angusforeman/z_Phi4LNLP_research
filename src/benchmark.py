"""Benchmark script to test LLM performance with various English language queries."""

import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from schema import ECOMMERCE_SCHEMA
from prompt_builder import build_prompt
from translator import Translator


# 40 diverse test queries covering various SQL operations
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


class BenchmarkResult:
    """Results from a single benchmark test."""
    
    def __init__(self, query: str, sql: str, success: bool, 
                 duration: float, error: str = None):
        self.query = query
        self.sql = sql
        self.success = success
        self.duration = duration
        self.error = error
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "query": self.query,
            "sql": self.sql,
            "success": self.success,
            "duration_seconds": round(self.duration, 3),
            "error": self.error
        }


def run_benchmark(queries: List[str], model_name: str = "phi4") -> List[BenchmarkResult]:
    """
    Run benchmark tests on a list of queries.
    
    Args:
        queries: List of natural language queries to test
        model_name: Name of the Ollama model to use
        
    Returns:
        List of BenchmarkResult objects
    """
    translator = Translator(model_name=model_name, timeout=30)
    
    # Check model availability
    if not translator.check_model_available():
        print(f"Error: {model_name} model not found. Run 'ollama pull {model_name}' first.", 
              file=sys.stderr)
        sys.exit(1)
    
    results = []
    total = len(queries)
    
    print(f"\n{'='*70}")
    print(f"Starting benchmark with {total} queries using model: {model_name}")
    print(f"{'='*70}\n")
    
    for idx, query in enumerate(queries, 1):
        print(f"[{idx}/{total}] Testing: {query[:60]}{'...' if len(query) > 60 else ''}")
        
        # Build prompt and translate
        prompt = build_prompt(query, ECOMMERCE_SCHEMA)
        response = translator.translate(prompt)
        
        # Create result
        result = BenchmarkResult(
            query=query,
            sql=response.sql_query if response.success else "",
            success=response.success,
            duration=response.response_time,
            error=response.error_message if not response.success else None
        )
        
        results.append(result)
        
        # Print result
        if response.success:
            print(f"  ✓ Success ({response.response_time:.3f}s)")
            print(f"  SQL: {response.sql_query[:100]}{'...' if len(response.sql_query) > 100 else ''}")
        else:
            print(f"  ✗ Failed ({response.response_time:.3f}s): {response.error_message}")
        print()
        
        # Small delay to avoid overwhelming the model
        time.sleep(0.5)
    
    return results


def save_results(results: List[BenchmarkResult], output_file: str = None):
    """
    Save benchmark results to JSON file.
    
    Args:
        results: List of BenchmarkResult objects
        output_file: Path to output file (auto-generated if None)
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"benchmark_results_{timestamp}.json"
    
    # Calculate statistics
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    
    total_time = sum(r.duration for r in results)
    avg_time = total_time / len(results) if results else 0
    
    success_times = [r.duration for r in successful]
    avg_success_time = sum(success_times) / len(success_times) if success_times else 0
    
    min_time = min(success_times) if success_times else 0
    max_time = max(success_times) if success_times else 0
    
    # Create output structure
    output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_queries": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": round(len(successful) / len(results) * 100, 2) if results else 0,
        },
        "statistics": {
            "total_time_seconds": round(total_time, 3),
            "average_time_seconds": round(avg_time, 3),
            "average_success_time_seconds": round(avg_success_time, 3),
            "min_time_seconds": round(min_time, 3),
            "max_time_seconds": round(max_time, 3),
        },
        "results": [r.to_dict() for r in results]
    }
    
    # Save to file
    output_path = Path("./logs") / output_file
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Results saved to: {output_path}")
    print(f"{'='*70}\n")
    
    return output_path, output


def save_markdown_report(results: List[BenchmarkResult], stats: Dict, output_file: str = None) -> Path:
    """
    Save benchmark results as a markdown report.
    
    Args:
        results: List of BenchmarkResult objects
        stats: Dictionary with metadata and statistics
        output_file: Path to output file (auto-generated if None)
        
    Returns:
        Path to the created markdown file
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"benchmark_report_{timestamp}.md"
    
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    
    metadata = stats['metadata']
    statistics = stats['statistics']
    
    # Calculate additional statistics
    import statistics as stat_module
    success_times = [r.duration for r in successful]
    median = stat_module.median(success_times) if success_times else 0
    stdev = stat_module.stdev(success_times) if len(success_times) > 1 else 0
    
    # Build markdown content
    lines = []
    lines.append("# Benchmark Report")
    lines.append("")
    lines.append(f"**Generated:** {metadata['timestamp']}")
    lines.append(f"**Model:** phi4")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Queries | {metadata['total_queries']} |")
    lines.append(f"| Successful | {metadata['successful']} ({metadata['success_rate']:.1f}%) |")
    lines.append(f"| Failed | {metadata['failed']} |")
    lines.append(f"| Total Time | {statistics['total_time_seconds']:.2f}s |")
    lines.append("")
    lines.append("## Timing Statistics")
    lines.append("")
    lines.append(f"| Metric | Time (seconds) |")
    lines.append(f"|--------|----------------|")
    lines.append(f"| Average (all queries) | {statistics['average_time_seconds']:.3f}s |")
    lines.append(f"| Average (successful) | {statistics['average_success_time_seconds']:.3f}s |")
    lines.append(f"| Median | {median:.3f}s |")
    lines.append(f"| Min | {statistics['min_time_seconds']:.3f}s |")
    lines.append(f"| Max | {statistics['max_time_seconds']:.3f}s |")
    lines.append(f"| Std Deviation | {stdev:.3f}s |")
    lines.append("")
    
    # Performance percentiles
    if successful:
        durations_sorted = sorted(success_times)
        p50 = durations_sorted[len(durations_sorted) // 2]
        p90 = durations_sorted[int(len(durations_sorted) * 0.9)]
        p95 = durations_sorted[int(len(durations_sorted) * 0.95)]
        
        lines.append("## Performance Percentiles")
        lines.append("")
        lines.append(f"| Percentile | Time (seconds) |")
        lines.append(f"|------------|----------------|")
        lines.append(f"| P50 (median) | {p50:.3f}s |")
        lines.append(f"| P90 | {p90:.3f}s |")
        lines.append(f"| P95 | {p95:.3f}s |")
        lines.append("")
    
    # Query complexity analysis
    short = [r for r in successful if len(r.query) < 30]
    medium = [r for r in successful if 30 <= len(r.query) < 50]
    long_queries = [r for r in successful if len(r.query) >= 50]
    
    if any([short, medium, long_queries]):
        lines.append("## Query Complexity Analysis")
        lines.append("")
        lines.append(f"| Complexity | Count | Avg Time |")
        lines.append(f"|------------|-------|----------|")
        if short:
            avg_short = sum(r.duration for r in short) / len(short)
            lines.append(f"| Short (<30 chars) | {len(short)} | {avg_short:.3f}s |")
        if medium:
            avg_med = sum(r.duration for r in medium) / len(medium)
            lines.append(f"| Medium (30-50 chars) | {len(medium)} | {avg_med:.3f}s |")
        if long_queries:
            avg_long = sum(r.duration for r in long_queries) / len(long_queries)
            lines.append(f"| Long (>50 chars) | {len(long_queries)} | {avg_long:.3f}s |")
        lines.append("")
    
    # Top 5 fastest queries
    if successful:
        lines.append("## Fastest Queries")
        lines.append("")
        fastest = sorted(successful, key=lambda x: x.duration)[:5]
        for i, r in enumerate(fastest, 1):
            lines.append(f"{i}. **{r.duration:.3f}s** - {r.query}")
            lines.append(f"   ```sql")
            lines.append(f"   {r.sql}")
            lines.append(f"   ```")
            lines.append("")
    
    # Top 5 slowest queries
    if successful:
        lines.append("## Slowest Queries")
        lines.append("")
        slowest = sorted(successful, key=lambda x: x.duration, reverse=True)[:5]
        for i, r in enumerate(slowest, 1):
            lines.append(f"{i}. **{r.duration:.3f}s** - {r.query}")
            lines.append(f"   ```sql")
            lines.append(f"   {r.sql}")
            lines.append(f"   ```")
            lines.append("")
    
    # Failed queries
    if failed:
        lines.append("## Failed Queries")
        lines.append("")
        for i, r in enumerate(failed, 1):
            lines.append(f"{i}. **{r.query}**")
            lines.append(f"   - Error: {r.error}")
            lines.append(f"   - Duration: {r.duration:.3f}s")
            lines.append("")
    
    # All results summary
    lines.append("## All Results")
    lines.append("")
    lines.append(f"| # | Query | SQL | Duration | Status |")
    lines.append(f"|---|-------|-----|----------|--------|")
    for i, r in enumerate(results, 1):
        query_preview = r.query[:40] + "..." if len(r.query) > 40 else r.query
        sql_preview = r.sql[:40] + "..." if len(r.sql) > 40 else r.sql
        status = "✓" if r.success else "✗"
        lines.append(f"| {i} | {query_preview} | `{sql_preview}` | {r.duration:.3f}s | {status} |")
    lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append(f"*Report generated by benchmark.py on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*")
    
    # Save to file
    output_path = Path("./logs") / output_file
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("\n".join(lines))
    
    return output_path


def print_summary(results: List[BenchmarkResult]):
    """Print a summary of benchmark results."""
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    
    total_time = sum(r.duration for r in results)
    avg_time = total_time / len(results) if results else 0
    
    success_times = [r.duration for r in successful]
    avg_success_time = sum(success_times) / len(success_times) if success_times else 0
    
    print(f"\n{'='*70}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*70}")
    print(f"Total queries:          {len(results)}")
    print(f"Successful:             {len(successful)} ({len(successful)/len(results)*100:.1f}%)")
    print(f"Failed:                 {len(failed)} ({len(failed)/len(results)*100:.1f}%)")
    print(f"\nTiming Statistics:")
    print(f"Total time:             {total_time:.3f}s")
    print(f"Average time (all):     {avg_time:.3f}s")
    print(f"Average time (success): {avg_success_time:.3f}s")
    if success_times:
        print(f"Min time:               {min(success_times):.3f}s")
        print(f"Max time:               {max(success_times):.3f}s")
    print(f"{'='*70}\n")
    
    if failed:
        print("Failed queries:")
        for r in failed:
            print(f"  - {r.query}")
            print(f"    Error: {r.error}\n")


def main():
    """Main benchmark execution."""
    print(f"Starting benchmark at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run benchmark
    results = run_benchmark(TEST_QUERIES)
    
    # Print summary
    print_summary(results)
    
    # Save results (JSON and Markdown)
    json_file, stats = save_results(results)
    md_file = save_markdown_report(results, stats)
    
    print(f"Benchmark completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"JSON results: {json_file}")
    print(f"Markdown report: {md_file}")


if __name__ == "__main__":
    main()
