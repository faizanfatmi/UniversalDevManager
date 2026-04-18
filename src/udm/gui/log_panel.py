"""Collapsible system log panel with terminal styling."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from udm.gui.theme import (
    ACCENT_PRIMARY,
    AMBER,
    BG_CARD,
    BG_LOG,
    BORDER,
    FG_DIM,
    FG_MUTED,
    GREEN,
    PURPLE,
    RED,
)


class LogPanel(QWidget):
    """Collapsible terminal-style log output panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._collapsed = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 8, 24, 0)
        layout.setSpacing(0)

        # Header bar
        header = QWidget()
        header.setStyleSheet(f"""
            background-color: {BG_CARD};
            border: 1px solid {BORDER};
            border-bottom: none;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        header.setFixedHeight(38)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 8, 0)

        # Terminal dots decoration
        dots_layout = QHBoxLayout()
        dots_layout.setSpacing(6)
        for color in ["#ff5f57", "#ffbd2e", "#28c840"]:
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"""
                background-color: {color};
                border-radius: 5px;
            """)
            dots_layout.addWidget(dot)
        header_layout.addLayout(dots_layout)

        header_layout.addSpacing(12)

        title = QLabel("TERMINAL OUTPUT")
        title.setStyleSheet(f"""
            color: {FG_MUTED};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            background: transparent;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        toggle_btn = QPushButton("▲")
        toggle_btn.setFixedSize(28, 28)
        toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {FG_MUTED};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{ color: {FG_DIM}; }}
        """)
        toggle_btn.clicked.connect(self._toggle_collapse)
        self._toggle_btn = toggle_btn
        header_layout.addWidget(toggle_btn)

        layout.addWidget(header)

        # Log text area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedHeight(130)
        self.text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {BG_LOG};
                border: 1px solid {BORDER};
                border-top: none;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                font-family: "JetBrains Mono", "Cascadia Code", "Consolas", monospace;
                font-size: 12px;
                padding: 12px;
                color: {FG_DIM};
            }}
        """)
        layout.addWidget(self.text_edit)
        self._text_widget = self.text_edit

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        self._text_widget.setVisible(not self._collapsed)
        self._toggle_btn.setText("▼" if self._collapsed else "▲")

    def append_log(self, msg: str):
        color = FG_DIM
        ml = msg.lower()
        if "✓" in msg or "success" in ml or "installed" in ml:
            color = GREEN
        elif "✗" in msg or "fail" in ml or "error" in ml:
            color = RED
        elif "⚠" in msg or "warning" in ml or "skip" in ml:
            color = AMBER
        elif "═" in msg:
            color = ACCENT_PRIMARY

        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        fmt = cursor.charFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(msg + "\n")

        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    def clear_log(self):
        self.text_edit.clear()
