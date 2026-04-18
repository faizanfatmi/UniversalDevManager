"""PATH manipulation utilities."""

import glob
import os
from pathlib import Path

from udm.logger import logger
from udm.platform.detect import is_linux, is_mac, is_windows


def resolve_env_path(p: str) -> str:
    """Expand environment variables and resolve glob patterns."""
    expanded = os.path.expandvars(p)
    expanded = os.path.expanduser(expanded)
    if "*" in expanded:
        matches = glob.glob(expanded)
        if matches:
            return os.path.normpath(sorted(matches)[-1])
    return os.path.normpath(expanded)


def _windows_get_user_path() -> str:
    """Read the current user PATH from the registry."""
    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ
        ) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return value
    except FileNotFoundError:
        return ""


def _windows_set_user_path(new_path: str) -> bool:
    """Write *new_path* to the user PATH in the registry and broadcast."""
    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        import ctypes

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            5000,
            None,
        )
        logger.info("Windows user PATH updated and change broadcasted.")
        return True
    except Exception as e:
        logger.error(f"Failed to set Windows PATH: {e}")
        return False


def add_to_path(directory: str) -> bool:
    """Add *directory* to the user PATH if it is not already present."""
    directory = resolve_env_path(directory)

    if is_windows():
        current = _windows_get_user_path()
        entries = [e.strip() for e in current.split(";") if e.strip()]
        normalized = [os.path.normpath(e) for e in entries]
        if directory in normalized:
            logger.info(f"PATH already contains {directory}")
            return True
        if not os.path.isdir(directory):
            logger.warning(f"Directory does not exist (yet): {directory}")
        entries.append(directory)
        return _windows_set_user_path(";".join(entries))

    elif is_linux():
        rc_file = Path.home() / ".bashrc"
        export_line = f'\nexport PATH="$PATH:{directory}"\n'
        try:
            content = rc_file.read_text(encoding="utf-8") if rc_file.exists() else ""
            if directory in content:
                logger.info(f"PATH already contains {directory}")
                return True
            with open(rc_file, "a", encoding="utf-8") as f:
                f.write(export_line)
            logger.info(f"Appended {directory} to ~/.bashrc")
            return True
        except Exception as e:
            logger.error(f"Failed to update ~/.bashrc: {e}")
            return False

    elif is_mac():
        rc_file = Path.home() / ".zshrc"
        export_line = f'\nexport PATH="$PATH:{directory}"\n'
        try:
            content = rc_file.read_text(encoding="utf-8") if rc_file.exists() else ""
            if directory in content:
                logger.info(f"PATH already contains {directory}")
                return True
            with open(rc_file, "a", encoding="utf-8") as f:
                f.write(export_line)
            logger.info(f"Appended {directory} to ~/.zshrc")
            return True
        except Exception as e:
            logger.error(f"Failed to update ~/.zshrc: {e}")
            return False

    return False
