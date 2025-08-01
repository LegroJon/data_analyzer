"""
Configuration module for the data analyzer package.

Contains default settings, pattern configurations, and file path constants.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"

# Default settings
DEFAULT_ENCODING = "utf-8"
DEFAULT_CSV_DELIMITER = ","
DEFAULT_OUTPUT_FORMAT = "original"

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# File patterns
SUPPORTED_INPUT_EXTENSIONS = [".txt", ".text"]
OUTPUT_EXTENSION = ".csv"

# Pattern validation settings
MAX_PATTERN_LENGTH = 1000
MAX_FILE_SIZE_MB = 100

def ensure_directories():
    """Ensure all required directories exist."""
    directories = [DATA_DIR, INPUT_DIR, OUTPUT_DIR, CONFIG_DIR, DOCS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_output_path(filename: str) -> Path:
    """Get full output path for a filename."""
    ensure_directories()
    return OUTPUT_DIR / filename

def get_input_path(filename: str) -> Path:
    """Get full input path for a filename."""
    ensure_directories()
    return INPUT_DIR / filename
