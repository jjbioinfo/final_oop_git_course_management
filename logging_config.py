"""Configure console output and a size-limited log file for the CLI."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path(__file__).with_name("logs") / "course_management.log"
logger = logging.getLogger(__name__)


def configure_logging(log_file: Path | None = None) -> None:
    """Keep console logging available even if the log file cannot be opened."""
    # Configure the console first so a file-permission error can still be reported.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
        force=True,
    )
    try:
        destination = LOG_FILE if log_file is None else Path(log_file)
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Rotate after roughly 1 MB and retain three backups instead of growing forever.
        handler = RotatingFileHandler(
            destination, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(logging.getLogger().handlers[0].formatter)
        logging.getLogger().addHandler(handler)
    except OSError:
        logger.warning("Log file unavailable; continuing with console logging.")
