"""Main application window — assembles all GUI sections."""

import sys
import threading

from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget

from udm.config import get_categories, load_tools
from udm.constants import (
    MIN_HEIGHT,
    MIN_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)
from udm.gui.action_bar import ActionBar
from udm.gui.header import HeaderBar
from udm.gui.log_panel import LogPanel
from udm.gui.search_bar import SearchBar
from udm.gui.status_bar import StatusBar
from udm.gui.theme import build_stylesheet
from udm.gui.tool_table import ToolTable
from udm.installer import install_selected, set_log_callback, set_progress_callback
from udm.logger import logger
from udm.network import check_internet


class WorkerSignals(QObject):
    """Signals for cross-thread communication."""

    progress = Signal(str, str, int)
    log_message = Signal(str)
    finished = Signal(dict)


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)
        self.setStyleSheet(build_stylesheet())

        self._installing = False
        self._signals = WorkerSignals()
        self._signals.progress.connect(self._on_progress)
        self._signals.log_message.connect(self._on_log)
        self._signals.finished.connect(self._on_install_finished)

        self._all_tools = load_tools()
        self._categories = get_categories(self._all_tools)

        self._build_ui()
        self._connect_signals()
        self._setup_callbacks()
        self._center_on_screen()

    def _center_on_screen(self):
        screen = self.screen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = HeaderBar()
        layout.addWidget(self.header)

        self.search_bar = SearchBar(self._categories)
        layout.addWidget(self.search_bar)

        self.tool_table = ToolTable(self._all_tools)
        layout.addWidget(self.tool_table, stretch=1)

        self.log_panel = LogPanel()
        layout.addWidget(self.log_panel)

        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)

        self.action_bar = ActionBar()
        layout.addWidget(self.action_bar)

    def _connect_signals(self):
        self.search_bar.filter_changed.connect(self._apply_filter)
        self.search_bar.refresh_requested.connect(self._on_refresh)
        self.tool_table.selection_changed.connect(self._on_selection_changed)
        self.action_bar.clear_clicked.connect(self._on_clear)
        self.action_bar.install_clicked.connect(self._on_install)

    def _setup_callbacks(self):
        set_progress_callback(
            lambda tool, status, pct: self._signals.progress.emit(tool, status, pct)
        )
        set_log_callback(lambda msg: self._signals.log_message.emit(msg))

    def _apply_filter(self):
        query = self.search_bar.search_text()
        category = self.search_bar.selected_category()
        self.tool_table.apply_filter(query, category)

    def _on_selection_changed(self, count: int):
        self.action_bar.update_state(count)

    def _on_clear(self):
        self.tool_table.clear_selection()

    def _on_refresh(self):
        self._all_tools = load_tools()
        self._categories = get_categories(self._all_tools)
        self.search_bar.set_categories(self._categories)
        self.tool_table.rebuild(self._all_tools)
        self._apply_filter()
        self.log_panel.append_log("↻  Tool list refreshed from tools.json")

    def _on_install(self):
        tools = self.tool_table.selected_tools()
        if not tools:
            QMessageBox.warning(
                self, "Nothing selected", "Select at least one tool first."
            )
            return
        if self._installing:
            QMessageBox.information(self, "Busy", "An installation is already running.")
            return

        self.log_panel.append_log("Checking internet connection…")
        if not check_internet():
            QMessageBox.critical(
                self, "No Internet", "Please connect to the internet and try again."
            )
            self.log_panel.append_log("✗ No internet — aborted.")
            return

        self._installing = True
        self.status_bar.set_progress(0)
        self.status_bar.set_status_text("Starting installation…")

        names = ", ".join(t["name"] for t in tools)
        self.log_panel.append_log(f"Selected: {names}")

        def worker():
            try:
                results = install_selected(tools)
            except Exception as ex:
                logger.exception("Unhandled error during installation")
                results = {}
            finally:
                self._installing = False
                self._signals.finished.emit(results)

        threading.Thread(target=worker, daemon=True).start()

    @Slot(str, str, int)
    def _on_progress(self, tool: str, status: str, pct: int):
        self.status_bar.set_progress(pct)
        self.status_bar.set_status_text(f"{tool}  ·  {status}")

    @Slot(str)
    def _on_log(self, msg: str):
        self.log_panel.append_log(msg)

    @Slot(dict)
    def _on_install_finished(self, results: dict):
        self.status_bar.set_progress(100)

        installed = sum(1 for v in results.values() if v == "installed")
        skipped = sum(1 for v in results.values() if v == "already_installed")
        failed = sum(1 for v in results.values() if v == "failed")

        summary = (
            f"Installation Complete\n\n"
            f"   Newly installed:   {installed}\n"
            f"   Already present:   {skipped}\n"
            f"   Failed:            {failed}\n"
        )

        if failed:
            self.status_bar.set_status_text("Completed with errors")
            failed_names = [k for k, v in results.items() if v == "failed"]
            summary += f"\nFailed: {', '.join(failed_names)}"
            QMessageBox.warning(self, "Completed with errors", summary)
        else:
            self.status_bar.set_status_text("All done — happy coding! 🎉")
            QMessageBox.information(self, "Success ✓", summary)

    def closeEvent(self, event):
        if self._installing:
            reply = QMessageBox.question(
                self,
                "Confirm",
                "Installation in progress. Force exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        event.accept()
