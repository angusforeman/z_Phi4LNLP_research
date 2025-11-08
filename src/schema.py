"""Predefined database schema for e-commerce system."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ColumnDefinition:
    """Represents a database column."""
    name: str
    type: str
    is_primary_key: bool = False
    is_nullable: bool = True


@dataclass
class TableDefinition:
    """Represents a database table."""
    name: str
    columns: List[ColumnDefinition]
    description: Optional[str] = None


@dataclass
class Relationship:
    """Represents a foreign key relationship."""
    from_table: str
    from_column: str
    to_table: str
    to_column: str


@dataclass
class SchemaDefinition:
    """Represents the complete database schema."""
    tables: List[TableDefinition]
    relationships: List[Relationship]
    
    def to_sql_ddl(self) -> str:
        """Serialize schema to SQL DDL format for model context."""
        lines = ["-- Database Schema\n"]
        
        for table in self.tables:
            lines.append(f"CREATE TABLE {table.name} (")
            
            column_lines = []
            for col in table.columns:
                col_def = f"  {col.name} {col.type}"
                if col.is_primary_key:
                    col_def += " PRIMARY KEY"
                if not col.is_nullable and not col.is_primary_key:
                    col_def += " NOT NULL"
                column_lines.append(col_def)
            
            lines.append(",\n".join(column_lines))
            lines.append(");\n")
        
        if self.relationships:
            lines.append("\n-- Relationships")
            for rel in self.relationships:
                lines.append(
                    f"-- {rel.from_table}.{rel.from_column} -> "
                    f"{rel.to_table}.{rel.to_column}"
                )
        
        return "\n".join(lines)


# Predefined e-commerce schema
ECOMMERCE_SCHEMA = SchemaDefinition(
    tables=[
        TableDefinition(
            name="customers",
            columns=[
                ColumnDefinition("id", "INTEGER", is_primary_key=True),
                ColumnDefinition("name", "VARCHAR(100)", is_nullable=False),
                ColumnDefinition("email", "VARCHAR(255)", is_nullable=False),
                ColumnDefinition("created_at", "TIMESTAMP", is_nullable=False),
            ],
            description="Customer information"
        ),
        TableDefinition(
            name="orders",
            columns=[
                ColumnDefinition("id", "INTEGER", is_primary_key=True),
                ColumnDefinition("customer_id", "INTEGER", is_nullable=False),
                ColumnDefinition("product_name", "VARCHAR(200)"),
                ColumnDefinition("quantity", "INTEGER"),
                ColumnDefinition("order_date", "DATE", is_nullable=False),
                ColumnDefinition("total_price", "DECIMAL(10,2)"),
            ],
            description="Order information"
        ),
        TableDefinition(
            name="products",
            columns=[
                ColumnDefinition("id", "INTEGER", is_primary_key=True),
                ColumnDefinition("name", "VARCHAR(200)", is_nullable=False),
                ColumnDefinition("price", "DECIMAL(10,2)", is_nullable=False),
                ColumnDefinition("stock_quantity", "INTEGER"),
            ],
            description="Product catalog"
        ),
    ],
    relationships=[
        Relationship("orders", "customer_id", "customers", "id"),
    ]
)
