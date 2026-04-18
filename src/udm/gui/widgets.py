"""Custom Qt widgets — PillBadge, GradientButton, CategoryChip."""

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath
from PySide6.QtWidgets import QLabel, QPushButton, QGraphicsDropShadowEffect

from udm.gui.theme import (
    ACCENT_GRADIENT_END,
    ACCENT_GRADIENT_START,
    ACCENT_GLOW,
    ACCENT_PRIMARY,
    AMBER,
    BADGE_ACCENT_BG,
    BADGE_ACCENT_FG,
    BADGE_AMBER_BG,
    BADGE_AMBER_FG,
    BADGE_BG,
    BADGE_GREEN_BG,
    BADGE_GREEN_FG,
    BG_INPUT,
    BORDER,
    BORDER_LIGHT,
    FG,
    FG_DIM,
    FG_MUTED,
    GREEN,
    GREEN_DARK,
    GREEN_DIM,
    RED,
    RED_DIM,
    SIDEBAR_ITEM_ACTIVE,
    SIDEBAR_ITEM_HOVER,
)


class PillBadge(QLabel):
    """Rounded pill-style badge label."""

    VARIANTS = {
        "default": (BADGE_BG, FG_DIM),
        "green": (BADGE_GREEN_BG, BADGE_GREEN_FG),
        "amber": (BADGE_AMBER_BG, BADGE_AMBER_FG),
        "red": (RED_DIM, RED),
        "accent": (BADGE_ACCENT_BG, BADGE_ACCENT_FG),
    }

    def __init__(self, text: str, variant: str = "default", parent=None):
        super().__init__(text, parent)
        bg, fg = self.VARIANTS.get(variant, self.VARIANTS["default"])
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class ActionButton(QPushButton):
    """Styled action button with hover animation and optional gradient."""

    def __init__(self, text: str, variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._variant = variant
        self._apply_style(hovered=False)

    def _apply_style(self, hovered=False):
        if self._variant == "primary":
            if hovered:
                bg = ACCENT_PRIMARY
                fg = "#ffffff"
                border = ACCENT_PRIMARY
            else:
                bg = ACCENT_PRIMARY
                fg = "#ffffff"
                border = ACCENT_PRIMARY
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {ACCENT_GRADIENT_START}, stop:1 {ACCENT_GRADIENT_END});
                    color: {fg};
                    border: none;
                    border-radius: 10px;
                    padding: 12px 28px;
                    font-size: 13px;
                    font-weight: 700;
                    letter-spacing: 0.8px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #7c6cf7, stop:1 #10c4e8);
                }}
                QPushButton:disabled {{
                    background-color: {BG_INPUT};
                    color: {FG_MUTED};
                    border: 1px solid {BORDER};
                }}
            """)
            return

        if self._variant == "danger":
            if hovered:
                bg = RED
                fg = "#ffffff"
                border = RED
            else:
                bg = "transparent"
                fg = RED
                border = f"rgba(255, 82, 82, 0.4)"
        else:  # secondary
            bg = BG_INPUT if not hovered else "#272c3e"
            fg = FG
            border = BORDER

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: 1.5px solid {border};
                border-radius: 10px;
                padding: 11px 24px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.8px;
            }}
            QPushButton:disabled {{
                background-color: {BG_INPUT};
                color: {FG_MUTED};
                border-color: {BORDER};
            }}
        """)

    def enterEvent(self, event):
        if self.isEnabled():
            self._apply_style(hovered=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style(hovered=False)
        super().leaveEvent(event)


class SidebarButton(QPushButton):
    """Sidebar navigation button with icon and active state."""

    def __init__(self, text: str, icon_char: str = "", parent=None):
        display = f"{icon_char}  {text}" if icon_char else text
        super().__init__(display, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._active = False
        self._icon_char = icon_char
        self._text = text
        self._apply_style()

    def set_active(self, active: bool):
        self._active = active
        self._apply_style()

    def _apply_style(self):
        if self._active:
            bg = SIDEBAR_ITEM_ACTIVE
            fg = ACCENT_PRIMARY
            border_left = f"3px solid {ACCENT_PRIMARY}"
            font_weight = "700"
        else:
            bg = "transparent"
            fg = FG_DIM
            border_left = "3px solid transparent"
            font_weight = "500"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border: none;
                border-left: {border_left};
                border-radius: 0px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: {font_weight};
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {SIDEBAR_ITEM_HOVER};
                color: {FG};
            }}
        """)

    def enterEvent(self, event):
        if not self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {SIDEBAR_ITEM_HOVER};
                    color: {FG};
                    border: none;
                    border-left: 3px solid transparent;
                    border-radius: 0px;
                    padding: 12px 20px;
                    font-size: 13px;
                    font-weight: 500;
                    text-align: left;
                }}
            """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style()
        super().leaveEvent(event)
