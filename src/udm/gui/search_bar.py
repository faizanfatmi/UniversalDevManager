"""Search bar — floating search input with tool count badge."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from udm.gui.theme import (
    ACCENT_PRIMARY,
    BG_CARD,
    BG_INPUT,
    BORDER,
    FG,
    FG_DIM,
    FG_MUTED,
)
from udm.gui.widgets import ActionButton


class SearchBar(QWidget):
    """Search input and refresh button (category moved to sidebar)."""

    filter_changed = Signal()
    refresh_requested = Signal()

    def __init__(self, categories: list[str], parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 8)
        layout.setSpacing(12)

        # Search input with custom styling
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search packages...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(lambda _: self.filter_changed.emit())
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_INPUT};
                color: {FG};
                border: 1px solid {BORDER};
                border-radius: 12px;
                padding: 12px 18px;
                font-size: 14px;
                selection-background-color: {ACCENT_PRIMARY};
            }}
            QLineEdit:focus {{
                border-color: {ACCENT_PRIMARY};
                background-color: #1a1f30;
            }}
        """)
        layout.addWidget(self.search_input, stretch=1)

        # Refresh button
        refresh_btn = ActionButton("↻  Refresh", "secondary")
        refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(refresh_btn)

    def search_text(self) -> str:
        return self.search_input.text().strip().lower()

    def selected_category(self) -> str:
        """Category now comes from sidebar; this returns 'All' for compat."""
        return getattr(self, "_current_category", "All")

    def set_category(self, category: str):
        """Set current category from sidebar."""
        self._current_category = category
        self.filter_changed.emit()

    def set_categories(self, categories: list[str]):
        """Compatibility method — categories are now in sidebar."""
        pass
