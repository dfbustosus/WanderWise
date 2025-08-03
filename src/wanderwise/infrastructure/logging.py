# src/wanderwise/infrastructure/logging.py

import logging
import sys
from typing import Optional


def configure_logging(log_level: Optional[str] = None) -> None:
    """
    Configure the application's logging system.
    
    This function sets up logging with a consistent format across the application.
    In a production environment, this would be extended to include log rotation,
    structured logging (e.g., JSON format), and integration with monitoring services.
    
    Args:
        log_level: The logging level to use. If None, INFO is used.
    """
    # Determine the log level
    level = getattr(logging, log_level.upper()) if log_level else logging.INFO
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to the root logger
    root_logger.addHandler(console_handler)
    
    # Set specific levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # Log the configuration
    logging.info(f"Logging configured with level: {logging.getLevelName(level)}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    This is a convenience function to get a logger with consistent configuration.
    
    Args:
        name: The name of the logger, typically __name__ of the calling module.
        
    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)
