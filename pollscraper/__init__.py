"""Top-level package for PollScraper."""
try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata


__version__ = metadata.version(__package__)
__author__ = """Adam Jaspan"""
__email__ = 'adam.jaspan@googlemail.com'

import logging
from pathlib import Path
from .root import ROOT_DIR

# Default logging level for the package
package_log_level = logging.DEBUG

logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configure the root logger for the package
logging.basicConfig(
    level=package_log_level,
    format=logging_format,
)

# Create a logger instance for the package
logger = logging.getLogger(__name__)

# Create a FileHandler and set its level and format
logs_dir = Path(f'{ROOT_DIR}/logs/')
logs_dir.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(logs_dir / "pollscraper.log")
file_handler.setLevel(package_log_level)
formatter = logging.Formatter(
        logging_format
    )
file_handler.setFormatter(formatter)

# Add the FileHandler to the package logger
logger.addHandler(file_handler)
