"""Logging configuration."""

import logging
import sys
from pathlib import Path


def _log_file_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path.home() / ".universal_dev_manager.log"
    return Path(__file__).resolve().parent.parent.parent / "installer.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(_log_file_path(), encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("UniversalDevManager")
