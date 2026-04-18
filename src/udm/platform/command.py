"""Shell command execution utilities."""

import subprocess

from udm.logger import logger
from udm.platform.detect import is_windows


def run_command(
    cmd: str,
    shell: bool = True,
    timeout: int = 900,
) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    kwargs: dict = dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=shell,
        timeout=timeout,
    )
    if is_windows():
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    try:
        proc = subprocess.run(cmd, **kwargs)
        return (
            proc.returncode,
            proc.stdout.decode(errors="replace"),
            proc.stderr.decode(errors="replace"),
        )
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {cmd}")
        return -1, "", "Command timed out"
    except Exception as e:
        logger.error(f"Command failed: {cmd} — {e}")
        return -1, "", str(e)


def command_exists(cmd: str) -> bool:
    """Check whether *cmd* is available on PATH."""
    try:
        if is_windows():
            result = subprocess.run(
                ["where", cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        else:
            result = subprocess.run(
                ["which", cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        return result.returncode == 0
    except Exception:
        return False
