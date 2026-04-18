"""Custom Qt widgets — PillBadge, AnimatedButton."""

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QPushButton

from udm.gui.theme import (
    AMBER,
    BADGE_AMBER_BG,
    BADGE_AMBER_FG,
    BADGE_BG,
    BADGE_GREEN_BG,
    BADGE_GREEN_FG,
    BG_INPUT,
    BORDER,
    FG,
    FG_DIM,
    GREEN,
    GREEN_DARK,
    GREEN_DIM,
    RED,
    RED_DIM,
)


class PillBadge(QLabel):
    """Rounded pill-style badge label."""

    VARIANTS = {
        "default": (BADGE_BG, FG_DIM),
        "green": (BADGE_GREEN_BG, BADGE_GREEN_FG),
        "amber": (BADGE_AMBER_BG, BADGE_AMBER_FG),
        "red": (RED_DIM, RED),
    }

    def __init__(self, text: str, variant: str = "default", parent=None):
        super().__init__(text, parent)
        bg, fg = self.VARIANTS.get(variant, self.VARIANTS["default"])
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class ActionButton(QPushButton):
    """Styled action button with hover animation."""

    def __init__(self, text: str, variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._variant = variant
        self._apply_style(hovered=False)

    def _apply_style(self, hovered=False):
        if self._variant == "primary":
            bg = GREEN_DARK if not hovered else GREEN
            fg = "#ffffff"
            border = GREEN_DARK if not hovered else GREEN
        elif self._variant == "danger":
            if hovered:
                bg = RED
                fg = "#ffffff"
                border = RED
            else:
                bg = "transparent"
                fg = RED
                border = RED
        else:
            bg = BG_INPUT if not hovered else "#3a3f4a"
            fg = FG
            border = BORDER

        disabled_style = f"""
            QPushButton:disabled {{
                background-color: {BG_INPUT};
                color: {FG_DIM};
                border-color: {BORDER};
                cursor: default;
            }}
        """

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 2px solid {border};
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.8px;
            }}
            {disabled_style}
        """)

    def enterEvent(self, event):
        if self.isEnabled():
            self._apply_style(hovered=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style(hovered=False)
        super().leaveEvent(event)
