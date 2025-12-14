import logging
import sys

def setup_logging(log_file="app_logs.log", level=logging.INFO):
    """
    Configures logging for the application.
    Logs are printed to console and written to a file.
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
