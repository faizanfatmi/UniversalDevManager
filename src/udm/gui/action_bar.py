"""Bottom action bar — Clear Selection + Install Selected buttons."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QWidget

from udm.gui.theme import BG_WINDOW
from udm.gui.widgets import ActionButton


class ActionBar(QWidget):
    """Bottom buttons bar with clear and install actions."""

    clear_clicked = Signal()
    install_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BG_WINDOW};")
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 8, 28, 12)

        self.clear_btn = ActionButton("🗑  CLEAR SELECTION", "danger")
        self.clear_btn.clicked.connect(self.clear_clicked.emit)
        layout.addWidget(self.clear_btn)

        layout.addStretch()

        self.install_btn = ActionButton("⬇  INSTALL SELECTED", "primary")
        self.install_btn.setEnabled(False)
        self.install_btn.clicked.connect(self.install_clicked.emit)
        layout.addWidget(self.install_btn)

    def update_state(self, selected_count: int):
        self.install_btn.setEnabled(selected_count > 0)
        if selected_count > 0:
            self.install_btn.setText(f"⬇  INSTALL SELECTED ({selected_count})")
        else:
            self.install_btn.setText("⬇  INSTALL SELECTED")
