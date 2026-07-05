from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from the_prof.app.launcher import AppContext
from the_prof.app.theme import DARK_STYLESHEET
from the_prof.app.ui.main_window import MainWindow


def create_app(root: Path | None = None) -> tuple[QApplication, MainWindow]:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("The Prof")
    app.setStyleSheet(DARK_STYLESHEET)
    root_path = root or Path(__file__).resolve().parents[2]
    context = AppContext(root_path)
    window = MainWindow(context)
    return app, window


def main() -> int:
    app, window = create_app()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
