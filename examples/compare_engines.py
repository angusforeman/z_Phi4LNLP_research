"""
Compare performance across different inference engines.

This script runs the same queries on multiple inference engines
to provide a direct performance comparison.
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict

# Attempt to import all engines
ENGINES_AVAILABLE = {}

try:
    from llama_cpp_translator import LlamaCppTranslator
    ENGINES_AVAILABLE['llama.cpp'] = True
except ImportError:
    ENGINES_AVAILABLE['llama.cpp'] = False
    print("⚠ llama.cpp not available")

try:
    from transformers_translator import TransformersTranslator
    ENGINES_AVAILABLE['transformers'] = True
except ImportError:
    ENGINES_AVAILABLE['transformers'] = False
    print("⚠ transformers not available")

try:
    from vllm_translator import VLLMTranslator
    ENGINES_AVAILABLE['vllm'] = True
except ImportError:
    ENGINES_AVAILABLE['vllm'] = False
    print("⚠ vLLM not available")

# Always try Ollama (baseline)
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from translator import NLtoSQLTranslator
    ENGINES_AVAILABLE['ollama'] = True
except ImportError:
    ENGINES_AVAILABLE['ollama'] = False
    print("⚠ Ollama not available")


@dataclass
class ComparisonResult:
    """Results from comparing engines."""
    engine: str
    query: str
    sql: str
    response_time: float
    success: bool
    error: str = ""


TEST_QUERIES = [
    "show all customers",
    "count total orders",
    "list customers who placed orders",
    "show orders from last 30 days",
    "find customers with no orders",
]


def run_comparison(
    test_queries: List[str] = TEST_QUERIES,
    warmup_runs: int = 2
) -> Dict[str, List[ComparisonResult]]:
    """
    Run comparison across all available engines.
    
    Args:
        test_queries: List of natural language queries to test
        warmup_runs: Number of warmup runs per engine
        
    Returns:
        Dictionary mapping engine name to results list
    """
    schema = """-- Database Schema
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  product_name VARCHAR(200),
  quantity INTEGER,
  order_date DATE NOT NULL,
  total_price DECIMAL(10,2)
);

-- Relationships
-- orders.customer_id -> customers.id"""
    
    results = {}
    
    # Initialize engines
    engines = {}
    
    print("=" * 70)
    print("Initializing Inference Engines")
    print("=" * 70)
    
    if ENGINES_AVAILABLE['ollama']:
        try:
            print("\n[Ollama]")
            engines['ollama'] = NLtoSQLTranslator()
            print("✓ Ollama initialized")
        except Exception as e:
            print(f"✗ Ollama failed: {e}")
    
    if ENGINES_AVAILABLE['llama.cpp']:
        try:
            print("\n[llama.cpp]")
            model_path = input("Enter path to GGUF model file: ")
            engines['llama.cpp'] = LlamaCppTranslator(
                model_path=model_path,
                n_gpu_layers=-1
            )
            print("✓ llama.cpp initialized")
        except Exception as e:
            print(f"✗ llama.cpp failed: {e}")
    
    if ENGINES_AVAILABLE['transformers']:
        try:
            print("\n[Transformers]")
            engines['transformers'] = TransformersTranslator(
                model_name="microsoft/phi-2",
                use_4bit=True
            )
            print("✓ Transformers initialized")
        except Exception as e:
            print(f"✗ Transformers failed: {e}")
    
    if ENGINES_AVAILABLE['vllm']:
        try:
            print("\n[vLLM]")
            engines['vllm'] = VLLMTranslator(
                model_name="microsoft/phi-2",
                tensor_parallel_size=1
            )
            print("✓ vLLM initialized")
        except Exception as e:
            print(f"✗ vLLM failed: {e}")
    
    if not engines:
        print("\n✗ No engines available for comparison")
        return results
    
    # Warmup runs
    print("\n" + "=" * 70)
    print(f"Running {warmup_runs} warmup queries per engine...")
    print("=" * 70)
    
    warmup_query = "show all customers"
    
    for engine_name, engine in engines.items():
        print(f"\nWarming up {engine_name}...", end=" ")
        for i in range(warmup_runs):
            try:
                if engine_name == 'ollama':
                    prompt = f"{schema}\n\nNatural language query: {warmup_query}\n\nSQL:"
                    engine.translate(prompt)
                else:
                    prompt = f"Convert to SQL:\n{schema}\n\nQuery: {warmup_query}\n\nSQL:"
                    engine.translate(prompt)
                print(f"{i+1}...", end=" ")
            except Exception as e:
                print(f"✗")
                break
        print("✓")
    
    # Run comparisons
    print("\n" + "=" * 70)
    print(f"Running Comparison on {len(test_queries)} Queries")
    print("=" * 70)
    
    for engine_name, engine in engines.items():
        print(f"\n[{engine_name}]")
        results[engine_name] = []
        
        for i, query in enumerate(test_queries, 1):
            print(f"  {i}/{len(test_queries)}: {query[:50]}...", end=" ")
            
            try:
                # Build prompt
                if engine_name == 'ollama':
                    prompt = f"{schema}\n\nNatural language query: {query}\n\nSQL:"
                    response = engine.translate(prompt)
                    sql = response if isinstance(response, str) else response.sql_query
                    success = True
                    response_time = 0.0  # Ollama doesn't return timing in same format
                else:
                    prompt = f"Convert to SQL:\n{schema}\n\nQuery: {query}\n\nSQL:"
                    response = engine.translate(prompt)
                    sql = response.sql_query
                    success = response.success
                    response_time = response.response_time
                
                results[engine_name].append(ComparisonResult(
                    engine=engine_name,
                    query=query,
                    sql=sql,
                    response_time=response_time,
                    success=success
                ))
                
                print(f"✓ ({response_time:.2f}s)")
                
            except Exception as e:
                results[engine_name].append(ComparisonResult(
                    engine=engine_name,
                    query=query,
                    sql="",
                    response_time=0.0,
                    success=False,
                    error=str(e)
                ))
                print(f"✗ {e}")
    
    return results


def print_summary(results: Dict[str, List[ComparisonResult]]):
    """Print comparison summary."""
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    
    for engine_name, engine_results in results.items():
        if not engine_results:
            continue
        
        times = [r.response_time for r in engine_results if r.success]
        successes = sum(1 for r in engine_results if r.success)
        total = len(engine_results)
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n[{engine_name}]")
            print(f"  Success Rate: {successes}/{total} ({successes/total*100:.1f}%)")
            print(f"  Average Time: {avg_time:.3f}s")
            print(f"  Min Time:     {min_time:.3f}s")
            print(f"  Max Time:     {max_time:.3f}s")
        else:
            print(f"\n[{engine_name}]")
            print(f"  ✗ All queries failed")
    
    # Calculate speedup vs Ollama
    if 'ollama' in results and results['ollama']:
        ollama_times = [r.response_time for r in results['ollama'] if r.success]
        if ollama_times:
            ollama_avg = sum(ollama_times) / len(ollama_times)
            
            print("\n" + "-" * 70)
            print("SPEEDUP vs Ollama:")
            print("-" * 70)
            
            for engine_name in results:
                if engine_name == 'ollama':
                    continue
                times = [r.response_time for r in results[engine_name] if r.success]
                if times:
                    engine_avg = sum(times) / len(times)
                    speedup = ollama_avg / engine_avg
                    print(f"  {engine_name:15s}: {speedup:5.2f}x faster")


def save_results(results: Dict[str, List[ComparisonResult]], output_dir: Path):
    """Save detailed results to files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_file = output_dir / f"engine_comparison_{timestamp}.json"
    json_data = {
        engine: [asdict(r) for r in engine_results]
        for engine, engine_results in results.items()
    }
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"\n✓ Saved results to: {json_file}")
    
    # Save markdown report
    md_file = output_dir / f"engine_comparison_{timestamp}.md"
    with open(md_file, 'w') as f:
        f.write("# Inference Engine Comparison\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary table
        f.write("## Summary\n\n")
        f.write("| Engine | Success Rate | Avg Time | Min Time | Max Time |\n")
        f.write("|--------|--------------|----------|----------|----------|\n")
        
        for engine_name, engine_results in results.items():
            times = [r.response_time for r in engine_results if r.success]
            successes = sum(1 for r in engine_results if r.success)
            total = len(engine_results)
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                f.write(f"| {engine_name} | {successes}/{total} | {avg_time:.3f}s | {min_time:.3f}s | {max_time:.3f}s |\n")
        
        # Detailed results
        f.write("\n## Detailed Results\n\n")
        for engine_name, engine_results in results.items():
            f.write(f"### {engine_name}\n\n")
            for result in engine_results:
                f.write(f"**Query:** {result.query}\n\n")
                if result.success:
                    f.write(f"- **SQL:** `{result.sql}`\n")
                    f.write(f"- **Time:** {result.response_time:.3f}s\n")
                else:
                    f.write(f"- **Status:** Failed\n")
                    f.write(f"- **Error:** {result.error}\n")
                f.write("\n")
    
    print(f"✓ Saved report to: {md_file}")


def main():
    """Run engine comparison."""
    print("=" * 70)
    print("INFERENCE ENGINE COMPARISON")
    print("=" * 70)
    print("\nAvailable engines:")
    for engine, available in ENGINES_AVAILABLE.items():
        status = "✓" if available else "✗"
        print(f"  {status} {engine}")
    
    if not any(ENGINES_AVAILABLE.values()):
        print("\n✗ No inference engines available")
        print("\nInstall at least one:")
        print("  pip install llama-cpp-python")
        print("  pip install transformers torch accelerate")
        print("  pip install vllm")
        return
    
    # Run comparison
    results = run_comparison()
    
    if results:
        # Print summary
        print_summary(results)
        
        # Save results
        output_dir = Path(__file__).parent.parent / "logs"
        save_results(results, output_dir)


if __name__ == "__main__":
    main()
