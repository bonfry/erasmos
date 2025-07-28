"""Core configuration module for the Erasmos project.

This module centralizes configuration variables, such as directory paths,
to avoid hardcoding them throughout the application. It ensures that
temporary and output directories are available when the application starts.
"""

from pathlib import Path

# Project's base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Directories for temporary and output files
TMP_DIR = BASE_DIR / "tmp"
OUTPUT_DIR = BASE_DIR / "output"

def ensure_dirs():
    """Ensures that the output and temporary directories exist.

    This function should be called at application startup to create
    the necessary directories if they don't already exist.
    """
    TMP_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)