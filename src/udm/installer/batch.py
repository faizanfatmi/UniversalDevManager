"""Batch installation orchestrator."""

from udm.installer.callbacks import notify, log
from udm.installer.engine import detect_tool, install_tool, setup_path


def install_selected(tools: list[dict], on_complete=None) -> dict[str, str]:
    """Install all tools sequentially with progress callbacks."""
    results: dict[str, str] = {}
    total = len(tools)

    log("═══════════════════════════════════════════════════════")
    log(f"  Starting installation of {total} tool(s)…")
    log("═══════════════════════════════════════════════════════")

    for idx, tool in enumerate(tools, start=1):
        key = tool.get("key", tool["name"])
        name = tool.get("name", key)
        pct = int((idx - 1) / total * 100)

        notify(name, "Checking…", pct)
        log(f"\n── {name} ({idx}/{total}) ─────────────────────")

        if detect_tool(tool):
            log(f"  ✓ {name} is already installed. Skipping.")
            results[key] = "already_installed"
            notify(name, "Already installed  ✓", int(idx / total * 100))
            continue

        notify(name, "Installing…", pct)
        log(f"  Installing {name}…")
        try:
            success = install_tool(tool)
        except Exception as e:
            log(f"  ✗ Exception during install: {e}")
            success = False

        if not success:
            log(f"  ✗ Failed to install {name}.")
            results[key] = "failed"
            notify(name, "Failed  ✗", int(idx / total * 100))
            continue

        if tool.get("path_required", False):
            notify(name, "Configuring PATH…", pct)
            log(f"  Configuring PATH for {name}…")
            try:
                setup_path(tool)
            except Exception as e:
                log(f"  ⚠ PATH error: {e}")

        log(f"  ✓ {name} installed successfully.")
        results[key] = "installed"
        notify(name, "Installed  ✓", int(idx / total * 100))

    notify("Done", "All tasks complete", 100)
    log("\n═══════════════════════════════════════════════════════")
    log("  Installation batch complete.")
    log("═══════════════════════════════════════════════════════\n")

    if on_complete:
        on_complete(results)

    return results
