import logging
import sys

def setup_logging():
    """Configure centralized logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with the given name."""
    return logging.getLogger(name)
