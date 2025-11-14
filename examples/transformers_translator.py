"""
Hugging Face Transformers Implementation for NL-to-SQL Translation

This implementation uses the Transformers library with various optimizations
including FlashAttention, 4-bit quantization, and torch.compile.

Expected performance: 1.5-2.5x faster than Ollama (depending on optimizations)
"""

import time
import os
from dataclasses import dataclass
from typing import Optional
import torch

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
except ImportError:
    print("Please install: pip install transformers torch accelerate bitsandbytes")
    exit(1)


@dataclass
class TranslationResponse:
    """Response from translation attempt."""
    sql_query: str
    success: bool
    error_message: Optional[str] = None
    response_time: float = 0.0


class TransformersTranslator:
    """
    Translates natural language to SQL using Hugging Face Transformers.
    
    Features:
    - Multiple optimization options
    - 4-bit quantization support
    - FlashAttention v2
    - PyTorch 2.0 compilation
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/phi-2",  # phi-4 not yet on HF
        use_4bit: bool = True,
        use_flash_attention: bool = False,
        compile_model: bool = False,
        device: str = "auto"
    ):
        """
        Initialize Transformers translator.
        
        Args:
            model_name: HuggingFace model identifier
            use_4bit: Enable 4-bit quantization (saves memory)
            use_flash_attention: Use FlashAttention v2 (faster, requires compatible GPU)
            compile_model: Use torch.compile (PyTorch 2.0+, faster after warmup)
            device: Device to use ('auto', 'cuda', 'cpu')
        """
        print(f"Loading model: {model_name}")
        print(f"4-bit quantization: {use_4bit}")
        print(f"FlashAttention: {use_flash_attention}")
        print(f"Torch compile: {compile_model}")
        
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Device: {self.device}")
        
        # Configure quantization if enabled
        quantization_config = None
        if use_4bit and self.device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            print("✓ 4-bit quantization configured")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        model_kwargs = {
            "trust_remote_code": True,
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
        }
        
        if quantization_config:
            model_kwargs["quantization_config"] = quantization_config
            model_kwargs["device_map"] = "auto"
        
        if use_flash_attention and self.device == "cuda":
            try:
                model_kwargs["attn_implementation"] = "flash_attention_2"
                print("✓ FlashAttention v2 enabled")
            except Exception as e:
                print(f"⚠ FlashAttention not available: {e}")
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            **model_kwargs
        )
        
        # Move to device if not using device_map
        if "device_map" not in model_kwargs and self.device == "cuda":
            self.model = self.model.to(self.device)
        
        # Compile model if requested
        if compile_model and hasattr(torch, 'compile'):
            try:
                print("Compiling model (will be slow on first run)...")
                self.model = torch.compile(self.model, mode="reduce-overhead")
                print("✓ Model compiled")
            except Exception as e:
                print(f"⚠ Compilation failed: {e}")
        
        self.model.eval()
        print("✓ Model loaded successfully")
    
    def translate(self, prompt: str, max_new_tokens: int = 512) -> TranslationResponse:
        """
        Translate natural language to SQL.
        
        Args:
            prompt: Complete prompt including schema and query
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            TranslationResponse with SQL or error
        """
        start_time = time.time()
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=4096
            )
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=0.1,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode output (skip input tokens)
            sql_query = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            ).strip()
            
            response_time = time.time() - start_time
            
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
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "device": str(self.device),
            "dtype": str(self.model.dtype),
            "memory_footprint": f"{self.model.get_memory_footprint() / 1e9:.2f} GB",
        }


def main():
    """Example usage with different configurations."""
    
    # Configuration 1: Fast (4-bit quantization)
    print("=" * 60)
    print("Configuration 1: Fast (4-bit quantized)")
    print("=" * 60)
    translator_fast = TransformersTranslator(
        model_name="microsoft/phi-2",
        use_4bit=True,
        use_flash_attention=False,
        compile_model=False
    )
    
    # Example prompt
    schema = """-- Database Schema
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL
);"""
    
    natural_query = "show all customers"
    
    prompt = f"""You are a SQL expert. Given the following database schema, convert the natural language query to a valid SQL statement.

{schema}

Natural language query: {natural_query}

Generate ONLY the SQL query without any explanation.

SQL:"""
    
    # Test
    print(f"\nQuery: {natural_query}")
    result = translator_fast.translate(prompt)
    
    if result.success:
        print(f"✓ Success ({result.response_time:.3f}s)")
        print(f"SQL: {result.sql_query}")
    else:
        print(f"✗ Failed: {result.error_message}")
    
    print("\n" + "=" * 60)
    print("Model Info:")
    print(translator_fast.get_model_info())


if __name__ == "__main__":
    main()
