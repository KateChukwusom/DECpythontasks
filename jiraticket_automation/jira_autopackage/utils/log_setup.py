import logging
import os

def get_logger(module_name: str, level=logging.INFO):
    """
    Returns a logger for a specific module.

    Args:
        module_name (str): Name of the module (used for filename and logger name)
        level: Logging level (default DEBUG)

    Returns:
        logging.Logger: Configured logger for the module
    """
    logger = logging.getLogger(module_name)

    # Prevent adding multiple handlers if logger is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # File handler (one log file per module)
    log_file = os.path.join("logs", f"{module_name}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Log message format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

# Add handlers to the logger
    logger.addHandler(file_handler)


    return logger

