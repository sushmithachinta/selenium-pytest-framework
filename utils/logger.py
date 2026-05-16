import logging
import os
from typing import Dict

# Thread-safe singleton logger cache
_LOGGERS: Dict[str, logging.Logger] = {}
_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger instance with centralized configuration.
    
    Args:
        name: Logger module name (__name__)
        
    Returns:
        Configured logging.Logger instance
    """
    if name not in _LOGGERS:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers on root logger
        if logger.handlers:
            return logger
            
        os.makedirs("reports", exist_ok=True)

        # Console handler — INFO level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

        # File handler — DEBUG level for detailed logs
        file_handler = logging.FileHandler("reports/test_run.log", mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        _LOGGERS[name] = logger
    
    return _LOGGERS[name]
