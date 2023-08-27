"""Top-level package for PollScraper."""

__author__ = """Adam Jaspan"""
__email__ = 'adam.jaspan@googlemail.com'
__version__ = '0.1.0'

import logging
from root import ROOT_DIR

# Default logging level for the package
package_log_level = logging.DEBUG

# Configure the root logger for the package
logging.basicConfig(
    level=package_log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create a logger instance for the package
logger = logging.getLogger(__name__)

# Create a FileHandler and set its level and format
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs/pollscraper.log")
file_handler.setLevel(package_log_level)
formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
file_handler.setFormatter(formatter)

# Add the FileHandler to the package logger
logger.addHandler(file_handler)

# from . import cli, pollscraper, datamodel


# Function to update the logging level for the entire package
def update_log_level(level):
    global package_log_level
    package_log_level = level
    logger.setLevel(package_log_level)
    file_handler.setLevel(package_log_level)
