"""Application entry point."""

import sys

from udm.logger import logger
from udm.platform import is_windows, is_admin, request_admin


def main():
    logger.info("═══ Universal Dev Console started ═══")

    if is_windows() and not is_admin():
        if "--elevate" in sys.argv:
            logger.info("Requesting UAC elevation…")
            try:
                request_admin()
            except Exception:
                logger.warning("UAC elevation failed — continuing without admin.")
        else:
            logger.warning(
                "Running without admin privileges. "
                "Some installations may need admin. "
                "Relaunch with --elevate for full access."
            )

    from PySide6.QtWidgets import QApplication
    from udm.gui import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
