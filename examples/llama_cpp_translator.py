"""
llama.cpp Implementation for NL-to-SQL Translation

This implementation uses llama-cpp-python for direct inference
without the Ollama wrapper overhead.

Expected performance: 2-3x faster than Ollama
"""

import time
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

try:
    from llama_cpp import Llama
except ImportError:
    print("Please install: pip install llama-cpp-python")
    exit(1)


@dataclass
class TranslationResponse:
    """Response from translation attempt."""
    sql_query: str
    success: bool
    error_message: Optional[str] = None
    response_time: float = 0.0


class LlamaCppTranslator:
    """
    Translates natural language to SQL using llama.cpp directly.
    
    Advantages over Ollama:
    - 2-3x faster inference
    - Lower memory footprint
    - Direct GPU acceleration
    - Better control over generation parameters
    """
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 4096,
        n_gpu_layers: int = -1,
        n_batch: int = 512,
        verbose: bool = False
    ):
        """
        Initialize llama.cpp translator.
        
        Args:
            model_path: Path to GGUF model file
            n_ctx: Context window size
            n_gpu_layers: Number of layers to offload to GPU (-1 = all)
            n_batch: Batch size for prompt processing
            verbose: Enable verbose logging
        """
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        print(f"Loading model: {model_path}")
        print(f"GPU layers: {n_gpu_layers} (-1 = all)")
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_batch=n_batch,
            n_gpu_layers=n_gpu_layers,
            verbose=verbose,
            n_threads=os.cpu_count() or 4,  # Use all CPU cores
            use_mmap=True,                   # Memory-map model file
            use_mlock=False,                 # Don't lock memory
        )
        
        self.model_path = model_path
        print("✓ Model loaded successfully")
    
    def translate(self, prompt: str, max_tokens: int = 512) -> TranslationResponse:
        """
        Translate natural language to SQL.
        
        Args:
            prompt: Complete prompt including schema and query
            max_tokens: Maximum tokens to generate
            
        Returns:
            TranslationResponse with SQL or error
        """
        start_time = time.time()
        
        try:
            # Generate response
            response = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=0.1,
                top_p=0.95,
                repeat_penalty=1.1,
                stop=["</s>", "\n\n", "Natural language query:"],
                echo=False
            )
            
            response_time = time.time() - start_time
            
            # Extract generated text
            sql_query = response['choices'][0]['text'].strip()
            
            # Basic cleanup - remove markdown if present
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
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "model_path": self.model_path,
            "context_size": self.llm.n_ctx(),
            "vocab_size": self.llm.n_vocab(),
        }


def main():
    """Example usage."""
    # Example model path - adjust to your setup
    # Try Phi-4 first, then fall back to Phi-2
    MODEL_PATH = os.path.expanduser("~/.ollama/models/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf")
    if not Path(MODEL_PATH).exists():
        MODEL_PATH = os.path.expanduser("~/.ollama/models/phi-2.Q4_K_M.gguf")
    if not Path(MODEL_PATH).exists():
        MODEL_PATH = os.path.expanduser("~/.ollama/models/phi4-q4_k_m.gguf")
    
    # Or download a model:
    # wget https://huggingface.co/.../phi-4-q4_k_m.gguf
    
    if not Path(MODEL_PATH).exists():
        print(f"Model not found at: {MODEL_PATH}")
        print("\nTo use llama.cpp:")
        print("1. Download a GGUF model file")
        print("2. Update MODEL_PATH in this script")
        print("3. Run again")
        return
    
    # Initialize translator
    translator = LlamaCppTranslator(
        model_path=MODEL_PATH,
        n_gpu_layers=-1,  # Use GPU if available
    )
    
    # Example schema and query
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
    
    natural_query = "show all customers"
    
    prompt = f"""You are a SQL expert. Given the following database schema, convert the natural language query to a valid SQL statement.

{schema}

Natural language query: {natural_query}

Generate ONLY the SQL query without any explanation or markdown formatting. Return just the SQL statement.

SQL:"""
    
    # Translate
    print(f"\nQuery: {natural_query}")
    print("Translating...")
    
    result = translator.translate(prompt)
    
    if result.success:
        print(f"✓ Success ({result.response_time:.3f}s)")
        print(f"SQL: {result.sql_query}")
    else:
        print(f"✗ Failed ({result.response_time:.3f}s)")
        print(f"Error: {result.error_message}")


if __name__ == "__main__":
    main()
