# Data Model: Natural Language to SQL Translation

**Feature**: 001-nl-to-sql  
**Created**: 2025-11-07  
**Purpose**: Define data structures for schema representation and translation workflow

## Overview

This feature uses a predefined database schema to provide context for the Phi4 model when translating natural language to SQL. The data model focuses on representing the schema structure and managing the translation request/response flow.

## Entities

### 1. SchemaDefinition

Represents the predefined database schema that provides context for SQL generation.

**Attributes**:
- `tables`: Collection of table definitions
- `relationships`: Optional foreign key relationships between tables

**Purpose**: Embedded in the system at development time, serialized into prompt context for the model

**Example**:
```python
schema = SchemaDefinition(
    tables=[
        TableDefinition(name="customers", columns=[...]),
        TableDefinition(name="orders", columns=[...])
    ],
    relationships=[
        Relationship(from_table="orders", from_column="customer_id", 
                    to_table="customers", to_column="id")
    ]
)
```

---

### 2. TableDefinition

Represents a single database table within the schema.

**Attributes**:
- `name`: Table name (string)
- `columns`: List of column definitions
- `description`: Optional human-readable description

**Purpose**: Describes each table in the schema for model context

**Example**:
```python
table = TableDefinition(
    name="customers",
    columns=[
        ColumnDefinition(name="id", type="INTEGER", is_primary_key=True),
        ColumnDefinition(name="name", type="VARCHAR(100)"),
        ColumnDefinition(name="email", type="VARCHAR(255)")
    ],
    description="Customer information"
)
```

---

### 3. ColumnDefinition

Represents a single column within a table.

**Attributes**:
- `name`: Column name (string)
- `type`: SQL data type (string, e.g., "INTEGER", "VARCHAR(100)")
- `is_primary_key`: Boolean indicating if this is a primary key
- `is_nullable`: Boolean indicating if NULL values allowed (default: True)

**Purpose**: Provides detailed column information for accurate SQL generation

**Example**:
```python
column = ColumnDefinition(
    name="created_at",
    type="TIMESTAMP",
    is_primary_key=False,
    is_nullable=False
)
```

---

### 4. Relationship

Represents a foreign key relationship between tables.

**Attributes**:
- `from_table`: Source table name
- `from_column`: Source column name
- `to_table`: Target table name
- `to_column`: Target column name

**Purpose**: Helps model understand table relationships for JOIN operations

**Example**:
```python
rel = Relationship(
    from_table="orders",
    from_column="customer_id",
    to_table="customers",
    to_column="id"
)
```

---

### 5. TranslationRequest

Represents a user's request to translate natural language to SQL.

**Attributes**:
- `natural_language_query`: The English query string from user
- `schema_context`: The serialized schema to include in prompt
- `timestamp`: When request was made (for logging)

**Purpose**: Packages the user query with schema context for model

**Example**:
```python
request = TranslationRequest(
    natural_language_query="show all customers who ordered yesterday",
    schema_context=schema.to_prompt_text(),
    timestamp=datetime.now()
)
```

---

### 6. TranslationResponse

Represents the result from Phi4 model.

**Attributes**:
- `sql_query`: The generated SQL statement (string)
- `success`: Boolean indicating if translation succeeded
- `error_message`: Optional error description if translation failed
- `response_time`: Time taken to generate response (seconds)

**Purpose**: Contains the translated SQL or error information

**Example**:
```python
response = TranslationResponse(
    sql_query="SELECT * FROM customers WHERE created_at > DATE('now', '-1 day')",
    success=True,
    error_message=None,
    response_time=2.3
)
```

---

## Schema Serialization

The schema must be serialized into text format suitable for inclusion in the Phi4 prompt.

**Format**: SQL-like DDL (Data Definition Language) for clarity

**Example Output**:
```sql
-- Database Schema
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
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

This text is injected into the prompt template to provide context.

## Validation Rules

### Schema Validation
- All table names must be unique
- Column names within a table must be unique
- Each table should have at least one column
- Relationships must reference existing tables and columns

### Query Validation
- Natural language query must be non-empty
- Generated SQL must be non-empty if success=True
- Error message must be provided if success=False

### Response Validation
- Response time must be positive number
- SQL syntax should be checked (basic validation) before returning to user

## State Transitions

For research spike, no complex state management needed. Simple request-response flow:

```
User Input → TranslationRequest → Phi4 Model → TranslationResponse → User Output
```

No persistence, no state storage, no sessions.

## Implementation Notes

### Minimal Approach (per constitution)
- Schema defined as Python dataclasses or simple classes
- No ORM, no database, no complex validation beyond basic checks
- Schema hardcoded in `schema.py` file
- Serialization is simple string formatting, no fancy templating libraries

### Example Predefined Schema
For the research spike, use a simple e-commerce schema:
- `customers` table (id, name, email, created_at)
- `orders` table (id, customer_id, product_name, quantity, order_date, total_price)
- `products` table (id, name, price, stock_quantity)

This provides enough complexity to test JOINs and aggregations without overwhelming the spike.
