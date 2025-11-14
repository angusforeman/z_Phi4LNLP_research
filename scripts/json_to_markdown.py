#!/usr/bin/env python3
"""Generate markdown report from existing benchmark JSON results."""

import sys
import json
from pathlib import Path

sys.path.insert(0, 'src')
from benchmark import BenchmarkResult, save_markdown_report


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/json_to_markdown.py <benchmark_results.json>")
        sys.exit(1)
    
    json_file = Path(sys.argv[1])
    
    if not json_file.exists():
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Convert to BenchmarkResult objects
    results = []
    for r in data['results']:
        result = BenchmarkResult(
            query=r['query'],
            sql=r['sql'],
            success=r['success'],
            duration=r['duration_seconds'],
            error=r.get('error')
        )
        result.timestamp = r['timestamp']
        results.append(result)
    
    # Generate markdown report
    stats = {
        'metadata': data['metadata'],
        'statistics': data['statistics']
    }
    
    # Create matching filename
    base_name = json_file.stem.replace('benchmark_results_', 'benchmark_report_')
    md_filename = f"{base_name}.md"
    
    md_file = save_markdown_report(results, stats, md_filename)
    
    print(f"✓ Markdown report generated: {md_file}")


if __name__ == "__main__":
    main()
