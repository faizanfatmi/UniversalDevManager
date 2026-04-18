"""Progress and log callback management."""

from udm.logger import logger

_progress_cb = None
_log_cb = None


def set_progress_callback(cb):
    global _progress_cb
    _progress_cb = cb


def set_log_callback(cb):
    global _log_cb
    _log_cb = cb


def notify(tool: str, status: str, pct: int):
    if _progress_cb:
        _progress_cb(tool, status, pct)


def log(msg: str):
    logger.info(msg)
    if _log_cb:
        _log_cb(msg)
