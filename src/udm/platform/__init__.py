"""Platform-specific utilities."""

from udm.platform.detect import detect_os, is_windows, is_linux, is_mac, os_label
from udm.platform.admin import is_admin, request_admin
from udm.platform.path import add_to_path, resolve_env_path
from udm.platform.command import run_command, command_exists

__all__ = [
    "detect_os", "is_windows", "is_linux", "is_mac", "os_label",
    "is_admin", "request_admin",
    "add_to_path", "resolve_env_path",
    "run_command", "command_exists",
]
