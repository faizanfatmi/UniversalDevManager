"""Search bar — search input + category dropdown + refresh button."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QWidget

from udm.gui.theme import BG_WINDOW
from udm.gui.widgets import ActionButton


class SearchBar(QWidget):
    """Search input, category filter, and refresh button."""

    filter_changed = Signal()
    refresh_requested = Signal()

    def __init__(self, categories: list[str], parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BG_WINDOW};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 8)
        layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search registry…")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(lambda _: self.filter_changed.emit())
        layout.addWidget(self.search_input, stretch=1)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["All"] + categories)
        self.category_combo.setMinimumWidth(120)
        self.category_combo.currentTextChanged.connect(
            lambda _: self.filter_changed.emit()
        )
        layout.addWidget(self.category_combo)

        refresh_btn = ActionButton("↻  REFRESH", "secondary")
        refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(refresh_btn)

    def search_text(self) -> str:
        return self.search_input.text().strip().lower()

    def selected_category(self) -> str:
        return self.category_combo.currentText()

    def set_categories(self, categories: list[str]):
        current = self.category_combo.currentText()
        self.category_combo.blockSignals(True)
        self.category_combo.clear()
        self.category_combo.addItems(["All"] + categories)
        idx = self.category_combo.findText(current)
        if idx >= 0:
            self.category_combo.setCurrentIndex(idx)
        self.category_combo.blockSignals(False)
