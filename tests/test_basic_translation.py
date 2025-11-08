"""Test basic natural language to SQL translation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from schema import ECOMMERCE_SCHEMA
from prompt_builder import build_prompt
from translator import Translator


def test_simple_query_translation():
    """Test translation of a simple query."""
    translator = Translator(model_name="phi4")
    
    natural_language_query = "show all customers"
    prompt = build_prompt(natural_language_query, ECOMMERCE_SCHEMA)
    
    response = translator.translate(prompt)
    
    assert response.success, f"Translation failed: {response.error_message}"
    assert response.sql_query, "SQL query is empty"
    assert "customers" in response.sql_query.lower(), "SQL should reference customers table"
    assert "select" in response.sql_query.lower(), "SQL should be a SELECT query"
    assert response.response_time < 10, f"Response took too long: {response.response_time}s"


def test_count_query_translation():
    """Test translation of a count query."""
    translator = Translator(model_name="phi4")
    
    natural_language_query = "count all orders"
    prompt = build_prompt(natural_language_query, ECOMMERCE_SCHEMA)
    
    response = translator.translate(prompt)
    
    assert response.success, f"Translation failed: {response.error_message}"
    assert response.sql_query, "SQL query is empty"
    assert "orders" in response.sql_query.lower(), "SQL should reference orders table"
    assert "count" in response.sql_query.lower(), "SQL should use COUNT function"
