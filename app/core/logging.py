"""
Logging configuration for the application.

Sets up the root logger once at startup via setup_logging(),
which is called from main.py before the app initializes.
"""

import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
