"""Logging configuration for the Course Management System."""

import logging
from pathlib import Path

LOG_FILE = Path(__file__).with_name("logs") / "course_management.log"


def configure_logging() -> None:
    """Log DEBUG and higher messages to the terminal and a file."""
    LOG_FILE.parent.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
        force=True,
    )
    logging.getLogger(__name__).debug(f"Logging configured: file={LOG_FILE}")
