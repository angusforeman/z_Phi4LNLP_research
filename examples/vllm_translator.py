"""
vLLM Implementation for NL-to-SQL Translation

This implementation uses vLLM for maximum throughput and lowest latency.
Best suited for production deployments with high request volumes.

Expected performance: 5-10x faster than Ollama
"""

import time
from dataclasses import dataclass
from typing import Optional, List

try:
    from vllm import LLM, SamplingParams
except ImportError:
    print("Please install: pip install vllm")
    print("Note: vLLM requires CUDA-capable GPU")
    exit(1)


@dataclass
class TranslationResponse:
    """Response from translation attempt."""
    sql_query: str
    success: bool
    error_message: Optional[str] = None
    response_time: float = 0.0


class VLLMTranslator:
    """
    Translates natural language to SQL using vLLM.
    
    Features:
    - PagedAttention for efficient memory usage
    - Continuous batching for high throughput
    - Optimized CUDA kernels
    - Multi-GPU support
    
    Best for:
    - Production deployments
    - High request volumes
    - Concurrent queries
    - Maximum performance
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/phi-2",  # phi-4 when available
        tensor_parallel_size: int = 1,
        dtype: str = "float16",
        quantization: Optional[str] = None,  # "awq", "gptq", or None
        max_model_len: int = 4096,
        gpu_memory_utilization: float = 0.9
    ):
        """
        Initialize vLLM translator.
        
        Args:
            model_name: HuggingFace model identifier
            tensor_parallel_size: Number of GPUs for tensor parallelism
            dtype: Data type ('float16', 'bfloat16', 'float32')
            quantization: Quantization method ('awq', 'gptq', None)
            max_model_len: Maximum context length
            gpu_memory_utilization: Fraction of GPU memory to use (0.0-1.0)
        """
        print(f"Initializing vLLM with model: {model_name}")
        print(f"GPUs: {tensor_parallel_size}")
        print(f"Dtype: {dtype}")
        print(f"Quantization: {quantization or 'None'}")
        print(f"Max context: {max_model_len}")
        print(f"GPU memory: {gpu_memory_utilization * 100}%")
        
        self.llm = LLM(
            model=model_name,
            tensor_parallel_size=tensor_parallel_size,
            dtype=dtype,
            quantization=quantization,
            max_model_len=max_model_len,
            gpu_memory_utilization=gpu_memory_utilization,
            trust_remote_code=True,
            enforce_eager=False,  # Use CUDA graphs for speed
            disable_log_stats=True  # Reduce overhead
        )
        
        # Default sampling parameters for SQL generation
        self.default_sampling = SamplingParams(
            temperature=0.1,
            max_tokens=512,
            top_p=0.95,
            stop=["\n\n", "</s>", "Natural language query:"],
            skip_special_tokens=True
        )
        
        self.model_name = model_name
        print("✓ vLLM initialized successfully")
    
    def translate(
        self,
        prompt: str,
        sampling_params: Optional[SamplingParams] = None
    ) -> TranslationResponse:
        """
        Translate natural language to SQL.
        
        Args:
            prompt: Complete prompt including schema and query
            sampling_params: Custom sampling parameters (optional)
            
        Returns:
            TranslationResponse with SQL or error
        """
        start_time = time.time()
        
        try:
            params = sampling_params or self.default_sampling
            
            # Generate
            outputs = self.llm.generate([prompt], params)
            
            response_time = time.time() - start_time
            
            # Extract generated text
            sql_query = outputs[0].outputs[0].text.strip()
            
            # Basic cleanup
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()
            
            return TranslationResponse(
                sql_query=sql_query,
                success=True,
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return TranslationResponse(
                sql_query="",
                success=False,
                error_message=f"Translation failed: {str(e)}",
                response_time=response_time
            )
    
    def translate_batch(
        self,
        prompts: List[str],
        sampling_params: Optional[SamplingParams] = None
    ) -> List[TranslationResponse]:
        """
        Translate multiple queries in a batch (more efficient).
        
        This is where vLLM shines - it automatically batches and optimizes
        concurrent requests for maximum throughput.
        
        Args:
            prompts: List of prompts to translate
            sampling_params: Custom sampling parameters (optional)
            
        Returns:
            List of TranslationResponse objects
        """
        start_time = time.time()
        
        try:
            params = sampling_params or self.default_sampling
            
            # Generate all at once (vLLM handles batching)
            outputs = self.llm.generate(prompts, params)
            
            total_time = time.time() - start_time
            avg_time = total_time / len(prompts)
            
            # Convert to responses
            results = []
            for output in outputs:
                sql_query = output.outputs[0].text.strip()
                
                # Cleanup
                if sql_query.startswith("```sql"):
                    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                elif sql_query.startswith("```"):
                    sql_query = sql_query.replace("```", "").strip()
                
                results.append(TranslationResponse(
                    sql_query=sql_query,
                    success=True,
                    response_time=avg_time
                ))
            
            return results
            
        except Exception as e:
            # Return error for all queries
            return [
                TranslationResponse(
                    sql_query="",
                    success=False,
                    error_message=f"Batch translation failed: {str(e)}",
                    response_time=0.0
                )
                for _ in prompts
            ]
    
    def get_model_info(self) -> dict:
        """Get information about the vLLM engine."""
        return {
            "model": self.model_name,
            "num_gpus": self.llm.llm_engine.parallel_config.tensor_parallel_size,
        }


def main():
    """Example usage."""
    print("=" * 60)
    print("vLLM Translator Example")
    print("=" * 60)
    
    # Initialize translator
    translator = VLLMTranslator(
        model_name="microsoft/phi-2",
        tensor_parallel_size=1,  # Single GPU
        dtype="float16",
        gpu_memory_utilization=0.9
    )
    
    # Example schema
    schema = """-- Database Schema
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  product_name VARCHAR(200),
  total_price DECIMAL(10,2)
);"""
    
    # Single query example
    print("\n" + "=" * 60)
    print("Single Query Example")
    print("=" * 60)
    
    natural_query = "show all customers"
    prompt = f"""You are a SQL expert. Given the following database schema, convert the natural language query to a valid SQL statement.

{schema}

Natural language query: {natural_query}

Generate ONLY the SQL query without any explanation.

SQL:"""
    
    result = translator.translate(prompt)
    
    if result.success:
        print(f"✓ Success ({result.response_time:.3f}s)")
        print(f"SQL: {result.sql_query}")
    else:
        print(f"✗ Failed: {result.error_message}")
    
    # Batch query example
    print("\n" + "=" * 60)
    print("Batch Query Example (vLLM's Strength)")
    print("=" * 60)
    
    queries = [
        "show all customers",
        "count total orders",
        "list all products",
        "show customers with their orders"
    ]
    
    prompts = [
        f"""You are a SQL expert. Convert this to SQL:

{schema}

Query: {q}

SQL:""" for q in queries
    ]
    
    print(f"Translating {len(queries)} queries in batch...")
    start = time.time()
    results = translator.translate_batch(prompts)
    total_time = time.time() - start
    
    print(f"\nBatch completed in {total_time:.3f}s")
    print(f"Average per query: {total_time/len(queries):.3f}s")
    print(f"Throughput: {len(queries)/total_time:.2f} queries/sec")
    print("\nResults:")
    for i, (query, result) in enumerate(zip(queries, results), 1):
        if result.success:
            print(f"{i}. {query}")
            print(f"   → {result.sql_query}")
        else:
            print(f"{i}. {query} - FAILED")


if __name__ == "__main__":
    main()
