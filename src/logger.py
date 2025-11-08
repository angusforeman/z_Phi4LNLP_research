"""Logging configuration for the NL-to-SQL translator."""

import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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
    
    # Set log level
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Create formatter
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
