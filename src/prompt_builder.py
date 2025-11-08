"""Build prompts with schema context for the Phi4 model."""

from schema import SchemaDefinition


def build_prompt(natural_language_query: str, schema: SchemaDefinition) -> str:
    """
    Construct a prompt that includes schema context and the user's query.
    
    Args:
        natural_language_query: The English query from the user
        schema: The database schema definition
        
    Returns:
        Complete prompt string for the model
    """
    schema_ddl = schema.to_sql_ddl()
    
    prompt = f"""You are a SQL expert. Given the following database schema, convert the natural language query to a valid SQL statement.

{schema_ddl}

Natural language query: {natural_language_query}

Generate ONLY the SQL query without any explanation or markdown formatting. Return just the SQL statement.

SQL:"""
    
    return prompt
