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

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Optional name for the logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger 