"""Dark console theme — color palette and global QSS stylesheet."""

# Background hierarchy
BG_WINDOW = "#1a1d23"
BG_HEADER = "#22252d"
BG_CARD = "#252830"
BG_INPUT = "#2a2d36"
BG_ROW = "#252830"
BG_ROW_HOVER = "#2e323c"
BG_ROW_SELECTED = "#2a3040"
BG_LOG = "#1e2028"
BG_STATUS = "#1e2028"

# Foreground
FG = "#e0e2e8"
FG_DIM = "#8b8f9a"
FG_MUTED = "#5c5f6a"
FG_HEADER = "#f0f1f4"

# Accents
GREEN = "#4ade80"
GREEN_DIM = "#1a3a2a"
GREEN_DARK = "#16a34a"
RED = "#f87171"
RED_DIM = "#3f1a1a"
AMBER = "#fbbf24"
CYAN = "#22d3ee"
PURPLE = "#a78bfa"

# Borders
BORDER = "#32363f"
BORDER_LIGHT = "#3a3f4a"

# Badges
BADGE_BG = "#32363f"
BADGE_GREEN_BG = "#1a3a2a"
BADGE_GREEN_FG = "#4ade80"
BADGE_AMBER_BG = "#3a3020"
BADGE_AMBER_FG = "#fbbf24"

# Progress
PROGRESS_BG = "#2a2d36"
PROGRESS_FG = "#4ade80"

# Scrollbar
SCROLLBAR_BG = "#252830"
SCROLLBAR_FG = "#3a3f4a"

# Column header
COLUMN_HEADER_FG = "#6b7080"


def build_stylesheet() -> str:
    """Return the global QSS stylesheet for the application."""
    return f"""
        QMainWindow, QWidget {{
            background-color: {BG_WINDOW};
            color: {FG};
            font-family: "Segoe UI", "SF Pro Display", "Helvetica Neue", sans-serif;
            font-size: 13px;
        }}

        QLineEdit {{
            background-color: {BG_INPUT};
            color: {FG};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 14px;
            selection-background-color: {GREEN_DARK};
        }}
        QLineEdit:focus {{
            border-color: {GREEN};
        }}

        QComboBox {{
            background-color: {BG_INPUT};
            color: {FG};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            min-width: 80px;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {FG_DIM};
            margin-right: 8px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {BG_CARD};
            color: {FG};
            border: 1px solid {BORDER};
            selection-background-color: {GREEN_DIM};
            selection-color: {GREEN};
            outline: none;
        }}

        QScrollBar:vertical {{
            background: {SCROLLBAR_BG};
            width: 10px;
            border: none;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background: {SCROLLBAR_FG};
            border-radius: 5px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {FG_MUTED};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}

        QProgressBar {{
            background-color: {PROGRESS_BG};
            border: none;
            border-radius: 4px;
            text-align: center;
            color: transparent;
            max-height: 8px;
        }}
        QProgressBar::chunk {{
            background-color: {PROGRESS_FG};
            border-radius: 4px;
        }}

        QCheckBox {{
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {BORDER_LIGHT};
            border-radius: 4px;
            background-color: transparent;
        }}
        QCheckBox::indicator:checked {{
            background-color: {GREEN};
            border-color: {GREEN};
            image: none;
        }}
        QCheckBox::indicator:hover {{
            border-color: {GREEN};
        }}

        QTextEdit {{
            background-color: {BG_LOG};
            color: {FG_DIM};
            border: none;
            font-family: "JetBrains Mono", "Cascadia Code", "Consolas", monospace;
            font-size: 12px;
            padding: 12px;
            selection-background-color: {GREEN_DIM};
        }}

        QMessageBox {{
            background-color: {BG_CARD};
        }}
        QMessageBox QLabel {{
            color: {FG};
        }}
        QMessageBox QPushButton {{
            background-color: {BG_INPUT};
            color: {FG};
            border: 1px solid {BORDER};
            border-radius: 4px;
            padding: 6px 20px;
            min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: {BG_ROW_HOVER};
        }}
    """
