"""Test schema context is properly included in prompts."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from schema import ECOMMERCE_SCHEMA
from prompt_builder import build_prompt


def test_schema_in_prompt():
    """Verify schema DDL is included in prompt."""
    query = "show all products"
    prompt = build_prompt(query, ECOMMERCE_SCHEMA)
    
    # Check schema elements are present
    assert "CREATE TABLE customers" in prompt
    assert "CREATE TABLE orders" in prompt
    assert "CREATE TABLE products" in prompt
    
    # Check key columns
    assert "id" in prompt
    assert "name" in prompt
    assert "email" in prompt
    assert "customer_id" in prompt
    
    # Check query is included
    assert query in prompt


def test_schema_serialization():
    """Test schema serializes to valid DDL format."""
    ddl = ECOMMERCE_SCHEMA.to_sql_ddl()
    
    assert "CREATE TABLE" in ddl
    assert "customers" in ddl
    assert "orders" in ddl
    assert "products" in ddl
    assert "INTEGER" in ddl
    assert "VARCHAR" in ddl
    assert "PRIMARY KEY" in ddl
