"""Status bar — progress bar + system status label."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

from udm.gui.theme import BG_STATUS, FG_MUTED, BORDER
from udm.gui.widgets import PillBadge
from udm.constants import APP_VERSION


class StatusBar(QWidget):
    """Bottom status bar with progress indicator."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setStyleSheet(f"""
            background-color: {BG_STATUS};
            border-top: 1px solid {BORDER};
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(12)

        self.status_label = QLabel("SYSTEM OUTPUT LOG")
        self.status_label.setStyleSheet(f"""
            color: {FG_MUTED};
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            background: transparent;
        """)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        layout.addWidget(self.progress_bar, stretch=1)

        layout.addSpacing(16)

        version_badge = PillBadge(f"V{APP_VERSION}-STABLE", "default")
        layout.addWidget(version_badge)

    def set_progress(self, value: int):
        self.progress_bar.setValue(value)

    def set_status_text(self, text: str):
        self.status_label.setText(text)
