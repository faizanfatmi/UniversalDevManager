"""Header bar — app title + OS badge + admin badge."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

from udm.gui.theme import BG_HEADER, FG_HEADER
from udm.gui.widgets import PillBadge
from udm.platform import os_label, is_admin


class HeaderBar(QWidget):
    """Top header bar with title and status badges."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BG_HEADER}; border: none;")
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 0, 28, 0)

        title = QLabel("UNIVERSAL DEV CONSOLE")
        title.setStyleSheet(f"""
            color: {FG_HEADER};
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 1.5px;
            background: transparent;
        """)
        layout.addWidget(title)

        layout.addStretch()

        os_text = f"🖥  {os_label().upper()}"
        os_badge = PillBadge(os_text, "default")
        layout.addWidget(os_badge)

        layout.addSpacing(8)

        if is_admin():
            admin_badge = PillBadge("🔓  ADMIN MODE", "green")
        else:
            admin_badge = PillBadge("🔒  USER MODE", "amber")
        layout.addWidget(admin_badge)
