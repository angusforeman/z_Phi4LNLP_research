"""Logging configuration for the NL-to-SQL translator."""

import logging
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs for analysis."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields if they exist
        if hasattr(record, 'duration'):
            log_data['duration_seconds'] = round(record.duration, 3)
        if hasattr(record, 'query'):
            log_data['query'] = record.query
        if hasattr(record, 'sql_length'):
            log_data['sql_length'] = record.sql_length
        if hasattr(record, 'model'):
            log_data['model'] = record.model
        
        return json.dumps(log_data)


def setup_logger(name: str = "nl_to_sql") -> logging.Logger:
    """
    Set up and configure the logger based on environment variables.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Get configuration from environment
    log_output = os.getenv("LOG_OUTPUT", "console").lower()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = os.getenv("LOG_FORMAT", "text").lower()  # text or json
    
    # Set log level
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Create formatter based on format type
    if log_format == "json":
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Configure handler based on LOG_OUTPUT
    if log_output == "file":
        # Create logs directory if it doesn't exist
        log_dir = Path("./logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        log_file = log_dir / "nl_to_sql.log"
        handler = logging.FileHandler(log_file)
    else:
        # Console handler (stderr to avoid mixing with SQL output)
        handler = logging.StreamHandler(sys.stderr)
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


# Create default logger instance
logger = setup_logger()
