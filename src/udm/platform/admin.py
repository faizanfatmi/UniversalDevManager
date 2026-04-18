"""Admin / privilege helpers."""

import os
import sys

from udm.platform.detect import is_windows


def is_admin() -> bool:
    """Return True if the process has elevated privileges."""
    if is_windows():
        try:
            import ctypes

            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0


def request_admin():
    """Relaunch the current script with admin / root privileges."""
    if is_windows():
        import ctypes

        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
