from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from the_prof.app.launcher import AppContext
from the_prof.app.theme import DARK_STYLESHEET
from the_prof.app.ui.main_window import MainWindow


def _discover_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parents[1], here.parents[2]]:
        if (candidate / "README.md").exists() and (candidate / "app").exists():
            return candidate
        if (candidate / "README.md").exists() and (candidate / "the_prof" / "app").exists():
            return candidate
    return here.parents[1]


def create_app(root: Path | None = None) -> tuple[QApplication, MainWindow]:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("The Prof")
    app.setStyleSheet(DARK_STYLESHEET)
    root_path = root or _discover_repo_root()
    context = AppContext(root_path)
    window = MainWindow(context)
    return app, window


def main() -> int:
    app, window = create_app()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
