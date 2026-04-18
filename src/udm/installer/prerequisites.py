"""Platform prerequisites — Homebrew and apt-get update."""

from udm.platform import is_mac, is_linux, command_exists, run_command
from udm.installer.callbacks import log


def ensure_homebrew():
    """On macOS, install Homebrew if it is not present."""
    if is_mac() and not command_exists("brew"):
        log("  Homebrew not found — installing…")
        cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        rc, out, err = run_command(cmd, timeout=300)
        if rc != 0:
            log(f"  ⚠ Homebrew install failed: {err[:200]}")
        else:
            log("  ✓ Homebrew installed.")


def ensure_apt_updated():
    """Run `sudo apt-get update` once per session on Linux."""
    if not hasattr(ensure_apt_updated, "_done"):
        log("  Updating apt package index…")
        run_command("sudo apt-get update -y", timeout=120)
        ensure_apt_updated._done = True
