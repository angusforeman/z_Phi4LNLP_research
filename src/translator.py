"""Core translation logic using Ollama and Phi4 model."""

import time
from dataclasses import dataclass
from typing import Optional

import ollama
from logger import logger


@dataclass
class TranslationResponse:
    """Response from translation attempt."""
    sql_query: str
    success: bool
    error_message: Optional[str] = None
    response_time: float = 0.0


class Translator:
    """Translates natural language to SQL using Phi4 via Ollama."""
    
    def __init__(self, model_name: str = "phi4", timeout: int = 10):
        """
        Initialize translator.
        
        Args:
            model_name: Name of Ollama model to use
            timeout: Maximum seconds to wait for response
        """
        self.model_name = model_name
        self.timeout = timeout
    
    def translate(self, prompt: str) -> TranslationResponse:
        """
        Translate natural language to SQL using the model.
        
        Args:
            prompt: Complete prompt including schema and query
            
        Returns:
            TranslationResponse with SQL or error
        """
        logger.info(f"Starting translation with model: {self.model_name}")
        start_time = time.time()
        
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,  # Low temperature for consistent SQL
                    "num_predict": 512,  # Max tokens for SQL query
                }
            )
            
            response_time = time.time() - start_time
            logger.info(f"Phi4 model call completed in {response_time:.3f} seconds")
            
            if not response or 'response' not in response:
                logger.warning("Model returned empty response")
                return TranslationResponse(
                    sql_query="",
                    success=False,
                    error_message="Model returned empty response",
                    response_time=response_time
                )
            
            sql_query = response['response'].strip()
            
            # Basic cleanup - remove markdown if present
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()
            
            logger.info(f"Translation successful. Generated SQL query with {len(sql_query)} characters")
            return TranslationResponse(
                sql_query=sql_query,
                success=True,
                response_time=response_time
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Translation failed after {response_time:.3f} seconds: {str(e)}")
            return TranslationResponse(
                sql_query="",
                success=False,
                error_message=f"Translation failed: {str(e)}",
                response_time=response_time
            )
    
    def check_model_available(self) -> bool:
        """
        Check if the model is available in Ollama.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            models = ollama.list()
            if 'models' in models:
                model_names = [m['name'] for m in models['models']]
                return any(self.model_name in name for name in model_names)
            return False
        except Exception:
            return False
