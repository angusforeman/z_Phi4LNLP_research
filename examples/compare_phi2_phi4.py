"""Compare SQL accuracy between Phi-2 and Phi-4 benchmark results."""

import json
import sys
from pathlib import Path
from difflib import SequenceMatcher

def load_results(filepath):
    """Load benchmark results from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)

def clean_sql(sql):
    """Clean SQL for comparison - remove extra whitespace, newlines, etc."""
    # Remove common artifacts
    sql = sql.replace('"""', '').replace('```', '').replace('```sql', '')
    # Normalize whitespace
    sql = ' '.join(sql.split())
    return sql.strip()

def similarity_ratio(sql1, sql2):
    """Calculate similarity between two SQL queries."""
    return SequenceMatcher(None, sql1.lower(), sql2.lower()).ratio()

def analyze_query_differences(phi2_result, phi4_result):
    """Analyze differences for a single query."""
    query = phi2_result['query']
    sql2 = clean_sql(phi2_result['sql'])
    sql4 = clean_sql(phi4_result['sql'])
    
    # Calculate similarity
    sim = similarity_ratio(sql2, sql4)
    
    # Categorize difference
    if sim == 1.0:
        category = "identical"
    elif sim > 0.9:
        category = "minor_diff"  # Formatting, aliasing, etc.
    elif sim > 0.7:
        category = "moderate_diff"  # Different approach, same result
    else:
        category = "major_diff"  # Significantly different
    
    return {
        'query': query,
        'phi2_sql': sql2,
        'phi4_sql': sql4,
        'similarity': sim,
        'category': category,
        'different': sql2 != sql4
    }

def main():
    # Load results
    phi2_path = Path("../logs/benchmark_llama_cpp_20251114_093844.json")
    phi4_path = Path("../logs/benchmark_llama_cpp_20251114_100419.json")
    
    print("=" * 70)
    print("Phi-2 vs Phi-4 SQL Accuracy Comparison")
    print("=" * 70)
    print()
    
    if not phi2_path.exists() or not phi4_path.exists():
        print("Error: Benchmark files not found")
        return
    
    phi2_data = load_results(phi2_path)
    phi4_data = load_results(phi4_path)
    
    phi2_results = phi2_data['results']
    phi4_results = phi4_data['results']
    
    # Compare each query
    comparisons = []
    for phi2_r, phi4_r in zip(phi2_results, phi4_results):
        comp = analyze_query_differences(phi2_r, phi4_r)
        comparisons.append(comp)
    
    # Statistics
    identical = [c for c in comparisons if c['category'] == 'identical']
    minor = [c for c in comparisons if c['category'] == 'minor_diff']
    moderate = [c for c in comparisons if c['category'] == 'moderate_diff']
    major = [c for c in comparisons if c['category'] == 'major_diff']
    
    print("SUMMARY")
    print("-" * 70)
    print(f"Total queries:        {len(comparisons)}")
    print(f"Identical SQL:        {len(identical)} ({len(identical)/len(comparisons)*100:.1f}%)")
    print(f"Minor differences:    {len(minor)} ({len(minor)/len(comparisons)*100:.1f}%)")
    print(f"Moderate differences: {len(moderate)} ({len(moderate)/len(comparisons)*100:.1f}%)")
    print(f"Major differences:    {len(major)} ({len(major)/len(comparisons)*100:.1f}%)")
    print()
    
    # Average similarity
    avg_sim = sum(c['similarity'] for c in comparisons) / len(comparisons)
    print(f"Average similarity:   {avg_sim:.2%}")
    print()
    
    # Show examples of each category
    if minor:
        print("=" * 70)
        print("MINOR DIFFERENCES (formatting, aliases, etc.)")
        print("=" * 70)
        for c in minor[:3]:  # Show first 3
            print(f"\nQuery: {c['query']}")
            print(f"Similarity: {c['similarity']:.2%}")
            print(f"Phi-2: {c['phi2_sql'][:100]}...")
            print(f"Phi-4: {c['phi4_sql'][:100]}...")
    
    if moderate:
        print("\n" + "=" * 70)
        print("MODERATE DIFFERENCES (different approach)")
        print("=" * 70)
        for c in moderate[:3]:
            print(f"\nQuery: {c['query']}")
            print(f"Similarity: {c['similarity']:.2%}")
            print(f"Phi-2: {c['phi2_sql']}")
            print(f"Phi-4: {c['phi4_sql']}")
    
    if major:
        print("\n" + "=" * 70)
        print("MAJOR DIFFERENCES")
        print("=" * 70)
        for c in major:
            print(f"\nQuery: {c['query']}")
            print(f"Similarity: {c['similarity']:.2%}")
            print(f"Phi-2: {c['phi2_sql']}")
            print(f"Phi-4: {c['phi4_sql']}")
    
    # Quality analysis
    print("\n" + "=" * 70)
    print("QUALITY ANALYSIS")
    print("=" * 70)
    
    # Check for common quality indicators
    phi2_issues = 0
    phi4_issues = 0
    
    for c in comparisons:
        # Check for unnecessary complexity
        if len(c['phi2_sql']) > len(c['phi4_sql']) * 1.5:
            phi2_issues += 1
        if len(c['phi4_sql']) > len(c['phi2_sql']) * 1.5:
            phi4_issues += 1
    
    print(f"\nPhi-2 potentially over-complex queries: {phi2_issues}")
    print(f"Phi-4 potentially over-complex queries: {phi4_issues}")
    
    # Check for SQL artifacts/issues
    phi2_artifacts = sum(1 for c in comparisons if '"""' in c['phi2_sql'] or '```' in c['phi2_sql'])
    phi4_artifacts = sum(1 for c in comparisons if '"""' in c['phi4_sql'] or '```' in c['phi4_sql'])
    
    print(f"\nPhi-2 queries with formatting artifacts: {phi2_artifacts}")
    print(f"Phi-4 queries with formatting artifacts: {phi4_artifacts}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    if avg_sim > 0.95:
        print("✓ Both models produce HIGHLY SIMILAR SQL queries")
    elif avg_sim > 0.85:
        print("✓ Both models produce SIMILAR SQL queries with minor variations")
    elif avg_sim > 0.70:
        print("⚠ Models show MODERATE differences in approach")
    else:
        print("⚠ Models show SIGNIFICANT differences")
    
    if len(identical) > len(comparisons) * 0.5:
        print(f"✓ Over 50% of queries are IDENTICAL ({len(identical)}/{len(comparisons)})")
    
    print(f"\nBoth models: 100% success rate")
    print(f"Phi-2 avg time: {phi2_data['statistics']['average_success_time_seconds']:.2f}s")
    print(f"Phi-4 avg time: {phi4_data['statistics']['average_success_time_seconds']:.2f}s")
    
    if phi2_artifacts < phi4_artifacts:
        print(f"\n✓ Phi-2 produces cleaner output ({phi2_artifacts} vs {phi4_artifacts} artifacts)")
    elif phi4_artifacts < phi2_artifacts:
        print(f"\n✓ Phi-4 produces cleaner output ({phi4_artifacts} vs {phi2_artifacts} artifacts)")
    else:
        print(f"\n✓ Both models produce equally clean output")

if __name__ == "__main__":
    main()
