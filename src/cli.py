"""Command-line interface for natural language to SQL translation."""

import sys
from schema import ECOMMERCE_SCHEMA
from prompt_builder import build_prompt
from translator import Translator
from logger import logger


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Error: Query cannot be empty", file=sys.stderr)
        print("\nUsage: python src/cli.py \"<natural language query>\"", file=sys.stderr)
        print("\nExample: python src/cli.py \"show all customers\"", file=sys.stderr)
        sys.exit(1)
    
    natural_language_query = sys.argv[1]
    
    if not natural_language_query.strip():
        print("Error: Query cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    logger.info(f"Processing query: {natural_language_query}")
    
    # Initialize translator
    translator = Translator(model_name="phi4", timeout=10)
    
    # Check if model is available
    if not translator.check_model_available():
        logger.error("Phi4 model not found")
        print("Error: Phi4 model not found. Run 'ollama pull phi4' first.", file=sys.stderr)
        sys.exit(1)
    
    # Build prompt with schema context
    prompt = build_prompt(natural_language_query, ECOMMERCE_SCHEMA)
    
    # Translate to SQL
    response = translator.translate(prompt)
    
    if response.success:
        logger.info(f"Query processed successfully in {response.response_time:.3f} seconds")
        print(response.sql_query)
        sys.exit(0)
    else:
        error_msg = response.error_message or "Unable to translate query"
        logger.error(f"Query processing failed: {error_msg}")
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
