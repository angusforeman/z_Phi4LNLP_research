"""Analyze benchmark results from JSON files."""

import json
import sys
from pathlib import Path
from typing import Dict, List
import statistics


def load_results(file_path: str) -> Dict:
    """Load benchmark results from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def analyze_results(data: Dict):
    """Analyze and display benchmark results."""
    metadata = data['metadata']
    stats = data['statistics']
    results = data['results']
    
    print(f"\n{'='*80}")
    print(f"BENCHMARK ANALYSIS")
    print(f"{'='*80}")
    print(f"Timestamp: {metadata['timestamp']}")
    print(f"\nOverall Results:")
    print(f"  Total Queries:    {metadata['total_queries']}")
    print(f"  Successful:       {metadata['successful']} ({metadata['success_rate']}%)")
    print(f"  Failed:           {metadata['failed']}")
    
    print(f"\nTiming Statistics:")
    print(f"  Total Time:       {stats['total_time_seconds']:.3f}s")
    print(f"  Average Time:     {stats['average_time_seconds']:.3f}s")
    print(f"  Avg Success Time: {stats['average_success_time_seconds']:.3f}s")
    print(f"  Min Time:         {stats['min_time_seconds']:.3f}s")
    print(f"  Max Time:         {stats['max_time_seconds']:.3f}s")
    
    # Calculate additional statistics
    successful = [r for r in results if r['success']]
    if successful:
        durations = [r['duration_seconds'] for r in successful]
        median = statistics.median(durations)
        stdev = statistics.stdev(durations) if len(durations) > 1 else 0
        
        print(f"  Median Time:      {median:.3f}s")
        print(f"  Std Deviation:    {stdev:.3f}s")
    
    # Query complexity analysis (rough estimate based on length)
    print(f"\nQuery Complexity Analysis:")
    short = [r for r in results if len(r['query']) < 30]
    medium = [r for r in results if 30 <= len(r['query']) < 50]
    long_queries = [r for r in results if len(r['query']) >= 50]
    
    if short:
        avg_short = sum(r['duration_seconds'] for r in short if r['success']) / len([r for r in short if r['success']])
        print(f"  Short queries (<30 chars):   {len(short)} queries, avg {avg_short:.3f}s")
    if medium:
        avg_med = sum(r['duration_seconds'] for r in medium if r['success']) / len([r for r in medium if r['success']])
        print(f"  Medium queries (30-50):      {len(medium)} queries, avg {avg_med:.3f}s")
    if long_queries:
        success_long = [r for r in long_queries if r['success']]
        if success_long:
            avg_long = sum(r['duration_seconds'] for r in success_long) / len(success_long)
            print(f"  Long queries (>50 chars):    {len(long_queries)} queries, avg {avg_long:.3f}s")
    
    # Performance percentiles
    if successful:
        durations_sorted = sorted([r['duration_seconds'] for r in successful])
        p50 = durations_sorted[len(durations_sorted) // 2]
        p90 = durations_sorted[int(len(durations_sorted) * 0.9)]
        p95 = durations_sorted[int(len(durations_sorted) * 0.95)]
        
        print(f"\nPerformance Percentiles:")
        print(f"  P50 (median):     {p50:.3f}s")
        print(f"  P90:              {p90:.3f}s")
        print(f"  P95:              {p95:.3f}s")
    
    # Show slowest and fastest queries
    if successful:
        print(f"\nFastest Queries:")
        fastest = sorted(successful, key=lambda x: x['duration_seconds'])[:3]
        for i, r in enumerate(fastest, 1):
            print(f"  {i}. {r['duration_seconds']:.3f}s - {r['query'][:60]}")
        
        print(f"\nSlowest Queries:")
        slowest = sorted(successful, key=lambda x: x['duration_seconds'], reverse=True)[:3]
        for i, r in enumerate(slowest, 1):
            print(f"  {i}. {r['duration_seconds']:.3f}s - {r['query'][:60]}")
    
    # Show failed queries
    failed = [r for r in results if not r['success']]
    if failed:
        print(f"\nFailed Queries ({len(failed)}):")
        for r in failed:
            print(f"  - {r['query']}")
            print(f"    Error: {r['error']}")
    
    print(f"{'='*80}\n")


def compare_results(file1: str, file2: str):
    """Compare two benchmark results."""
    data1 = load_results(file1)
    data2 = load_results(file2)
    
    print(f"\n{'='*80}")
    print(f"BENCHMARK COMPARISON")
    print(f"{'='*80}")
    
    print(f"\nFile 1: {file1}")
    print(f"  Success Rate: {data1['metadata']['success_rate']:.1f}%")
    print(f"  Average Time: {data1['statistics']['average_success_time_seconds']:.3f}s")
    
    print(f"\nFile 2: {file2}")
    print(f"  Success Rate: {data2['metadata']['success_rate']:.1f}%")
    print(f"  Average Time: {data2['statistics']['average_success_time_seconds']:.3f}s")
    
    # Calculate differences
    success_diff = data2['metadata']['success_rate'] - data1['metadata']['success_rate']
    time_diff = data2['statistics']['average_success_time_seconds'] - data1['statistics']['average_success_time_seconds']
    time_pct = (time_diff / data1['statistics']['average_success_time_seconds'] * 100) if data1['statistics']['average_success_time_seconds'] > 0 else 0
    
    print(f"\nDifferences (File 2 vs File 1):")
    print(f"  Success Rate: {success_diff:+.1f}%")
    print(f"  Average Time: {time_diff:+.3f}s ({time_pct:+.1f}%)")
    
    print(f"{'='*80}\n")


def main():
    """Main analysis execution."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python src/analyze_benchmark.py <results_file.json>")
        print("  python src/analyze_benchmark.py <file1.json> <file2.json>  # Compare two runs")
        print("\nExample:")
        print("  python src/analyze_benchmark.py logs/benchmark_results_20241108_161234.json")
        sys.exit(1)
    
    file1 = sys.argv[1]
    
    if not Path(file1).exists():
        print(f"Error: File not found: {file1}")
        sys.exit(1)
    
    if len(sys.argv) == 3:
        # Compare mode
        file2 = sys.argv[2]
        if not Path(file2).exists():
            print(f"Error: File not found: {file2}")
            sys.exit(1)
        
        analyze_results(load_results(file1))
        analyze_results(load_results(file2))
        compare_results(file1, file2)
    else:
        # Single analysis mode
        data = load_results(file1)
        analyze_results(data)


if __name__ == "__main__":
    main()
