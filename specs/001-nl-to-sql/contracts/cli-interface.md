# CLI Interface Contract

**Feature**: 001-nl-to-sql  
**Version**: 1.0.0  
**Type**: Command-Line Interface

## Overview

Simple command-line interface for translating natural language to SQL. Research spike implementation - minimal features only.

## Command Signature

```bash
python src/cli.py "<natural_language_query>"
```

## Input

### Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | query | string | Yes | Natural language query in English |

### Constraints
- Query must be non-empty string
- Query should relate to the predefined schema (customers, orders, products)
- Maximum recommended length: 200 characters (model-dependent)

### Examples

```bash
python src/cli.py "show all customers"
python src/cli.py "count orders from yesterday"
python src/cli.py "list products with price under 100"
```

## Output

### Success Case

**Format**: Plain text SQL statement

**Example**:
```
SELECT * FROM customers;
```

**Exit Code**: 0

---

### Error Case

**Format**: Plain text error message

**Example**:
```
Error: Unable to translate query. The model did not respond.
```

**Exit Code**: 1

---

## Behavior

### Happy Path

1. User provides natural language query as command-line argument
2. System loads predefined schema
3. System constructs prompt with schema context + query
4. System sends prompt to Phi4 via Ollama
5. System extracts SQL from model response
6. System prints SQL to stdout
7. Exit code 0

### Error Paths

**Empty Query**:
- Output: `Error: Query cannot be empty`
- Exit code: 1

**Model Not Available**:
- Output: `Error: Phi4 model not found. Run 'ollama pull phi4' first.`
- Exit code: 1

**Model Timeout**:
- Output: `Error: Model did not respond within 10 seconds`
- Exit code: 1

**Invalid Model Response**:
- Output: `Error: Unable to extract SQL from model response`
- Exit code: 1

## Performance

- **Target**: 95% of queries respond within 5 seconds (per spec)
- **Acceptable**: First query may take longer (cold start)
- **Timeout**: 10 seconds (fail fast for research spike)

## Future Enhancements (Not in Scope)

The following are explicitly NOT part of this research spike:

- Interactive mode
- Query history
- SQL validation against actual database
- Multiple output formats (JSON, CSV)
- Configuration files
- Verbose/debug modes
- Custom schema input

These may be considered in future iterations if spike is successful.
