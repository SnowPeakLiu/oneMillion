"""
Logging utility module for the trading system.

Provides consistent logging configuration across all modules.

Example:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Operation successful")
"""

import logging
from typing import Optional

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a logger instance with consistent formatting.
    
    Args:
        name: Name of the logger, typically __name__
        level: Optional logging level, defaults to INFO
        
    Returns:
        Configured logger instance
        
    Example:
        logger = get_logger(__name__)
        logger.info("Processing trade")
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level or logging.INFO)
    return logger 