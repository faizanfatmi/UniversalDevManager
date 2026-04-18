"""Scrollable tool list table with checkboxes, version, and category badges."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from udm.gui.theme import (
    BADGE_BG,
    BG_CARD,
    BG_ROW,
    BG_ROW_HOVER,
    BG_ROW_SELECTED,
    BORDER,
    COLUMN_HEADER_FG,
    FG,
    FG_DIM,
    FG_MUTED,
    GREEN,
)
from udm.gui.widgets import PillBadge


class ToolRow(QFrame):
    """Single tool row with checkbox, name, description, version, category."""

    toggled = Signal(str, bool)

    def __init__(self, tool: dict, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.key = tool.get("key", tool["name"])
        self._selected = False

        self.setStyleSheet(f"""
            ToolRow {{
                background-color: {BG_ROW};
                border: none;
                border-bottom: 1px solid {BORDER};
            }}
        """)
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

        self.checkbox = QCheckBox()
        self.checkbox.setFixedWidth(36)
        self.checkbox.stateChanged.connect(self._on_check)
        layout.addWidget(self.checkbox)

        name_col = QVBoxLayout()
        name_col.setSpacing(2)
        name_col.setContentsMargins(0, 8, 0, 8)

        self.name_label = QLabel(tool.get("name", ""))
        self.name_label.setStyleSheet(f"""
            color: {FG};
            font-size: 13px;
            font-weight: 600;
            background: transparent;
        """)
        name_col.addWidget(self.name_label)

        self.desc_label = QLabel(tool.get("description", ""))
        self.desc_label.setStyleSheet(f"""
            color: {FG_MUTED};
            font-size: 11px;
            background: transparent;
        """)
        name_col.addWidget(self.desc_label)

        name_widget = QWidget()
        name_widget.setLayout(name_col)
        name_widget.setStyleSheet("background: transparent;")
        name_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        layout.addWidget(name_widget, stretch=1)

        version = (
            tool.get("detect_cmd", "").split("--version")[0].strip()
            if "--version" in tool.get("detect_cmd", "")
            else ""
        )
        version_text = "—"
        if version:
            version_text = version.split()[-1] if version.split() else "—"

        self.version_label = QLabel(version_text)
        self.version_label.setFixedWidth(120)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet(f"""
            color: {GREEN};
            font-family: "JetBrains Mono", "Consolas", monospace;
            font-size: 12px;
            background: transparent;
        """)
        layout.addWidget(self.version_label)

        layout.addSpacing(16)

        cat_text = tool.get("category", "Other").upper()
        self.cat_badge = PillBadge(cat_text, "default")
        self.cat_badge.setFixedWidth(120)
        layout.addWidget(self.cat_badge)

    def _on_check(self, state):
        self._selected = state == Qt.CheckState.Checked.value
        self._update_visual()
        self.toggled.emit(self.key, self._selected)

    def _update_visual(self):
        bg = BG_ROW_SELECTED if self._selected else BG_ROW
        self.setStyleSheet(f"""
            ToolRow {{
                background-color: {bg};
                border: none;
                border-bottom: 1px solid {BORDER};
            }}
        """)

    def is_checked(self) -> bool:
        return self.checkbox.isChecked()

    def set_checked(self, checked: bool):
        self.checkbox.setChecked(checked)

    def matches_filter(self, query: str, category: str) -> bool:
        if category != "All" and self.tool.get("category", "") != category:
            return False
        if query:
            name = self.tool.get("name", "").lower()
            desc = self.tool.get("description", "").lower()
            key = self.key.lower()
            if query not in name and query not in desc and query not in key:
                return False
        return True

    def enterEvent(self, event):
        if not self._selected:
            self.setStyleSheet(f"""
                ToolRow {{
                    background-color: {BG_ROW_HOVER};
                    border: none;
                    border-bottom: 1px solid {BORDER};
                }}
            """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._update_visual()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.checkbox.setChecked(not self.checkbox.isChecked())
        super().mousePressEvent(event)


class ColumnHeader(QWidget):
    """Column header row with select-all checkbox."""

    select_all_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet(
            f"background-color: {BG_CARD}; border-bottom: 1px solid {BORDER};"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

        self.select_all_cb = QCheckBox()
        self.select_all_cb.setFixedWidth(36)
        self.select_all_cb.stateChanged.connect(
            lambda state: self.select_all_changed.emit(
                state == Qt.CheckState.Checked.value
            )
        )
        layout.addWidget(self.select_all_cb)

        header_style = f"color: {COLUMN_HEADER_FG}; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; background: transparent;"

        name_header = QLabel("PACKAGE NAME & DESCRIPTION")
        name_header.setStyleSheet(header_style)
        layout.addWidget(name_header, stretch=1)

        version_header = QLabel("VERSION")
        version_header.setFixedWidth(120)
        version_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_header.setStyleSheet(header_style)
        layout.addWidget(version_header)

        layout.addSpacing(16)

        cat_header = QLabel("CATEGORY")
        cat_header.setFixedWidth(120)
        cat_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cat_header.setStyleSheet(header_style)
        layout.addWidget(cat_header)


class ToolTable(QWidget):
    """Scrollable list of tool rows with column headers."""

    selection_changed = Signal(int)

    def __init__(self, tools: list[dict], parent=None):
        super().__init__(parent)
        self._rows: list[ToolRow] = []

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(28, 0, 28, 0)
        outer_layout.setSpacing(0)

        self.column_header = ColumnHeader()
        self.column_header.select_all_changed.connect(self._on_select_all)
        outer_layout.addWidget(self.column_header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {BG_CARD};
            }}
        """)

        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(0)

        self._populate(tools)

        self.list_layout.addStretch()
        self.scroll_area.setWidget(self.list_widget)
        outer_layout.addWidget(self.scroll_area)

    def _populate(self, tools: list[dict]):
        for tool in tools:
            row = ToolRow(tool)
            row.toggled.connect(self._on_row_toggled)
            self._rows.append(row)
            self.list_layout.addWidget(row)

    def _on_row_toggled(self, key: str, checked: bool):
        count = sum(1 for r in self._rows if r.is_checked())
        self.selection_changed.emit(count)

    def _on_select_all(self, checked: bool):
        for row in self._rows:
            if row.isVisible():
                row.set_checked(checked)

    def apply_filter(self, query: str, category: str):
        for row in self._rows:
            visible = row.matches_filter(query, category)
            row.setVisible(visible)

    def selected_tools(self) -> list[dict]:
        return [r.tool for r in self._rows if r.is_checked()]

    def selected_count(self) -> int:
        return sum(1 for r in self._rows if r.is_checked())

    def clear_selection(self):
        self.column_header.select_all_cb.setChecked(False)
        for row in self._rows:
            row.set_checked(False)

    def rebuild(self, tools: list[dict]):
        for row in self._rows:
            self.list_layout.removeWidget(row)
            row.deleteLater()
        self._rows.clear()

        # Remove the stretch item
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._populate(tools)
        self.list_layout.addStretch()
        self.selection_changed.emit(0)
