"""OS detection utilities."""

import platform


def detect_os() -> str:
    """Return 'Windows', 'Linux', or 'Darwin' (macOS)."""
    return platform.system()


def is_windows() -> bool:
    return detect_os() == "Windows"


def is_linux() -> bool:
    return detect_os() == "Linux"


def is_mac() -> bool:
    return detect_os() == "Darwin"


def os_label() -> str:
    """Return a human-friendly OS name."""
    mapping = {"Windows": "Windows", "Linux": "Linux", "Darwin": "macOS"}
    return mapping.get(detect_os(), detect_os())
