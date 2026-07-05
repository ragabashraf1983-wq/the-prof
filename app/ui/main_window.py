from __future__ import annotations

from pathlib import Path

import yaml
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from the_prof.app.launcher import AppContext
from the_prof.app.ui.pages.brain_page import BrainPage
from the_prof.core.models import ProjectIntake
from the_prof.app.ui.pages.dashboard_page import DashboardPage
from the_prof.app.ui.pages.home_page import HomePage
from the_prof.app.ui.pages.help_page import HelpPage
from the_prof.app.ui.pages.new_project_page import NewProjectPage
from the_prof.app.ui.pages.providers_page import ProvidersPage
from the_prof.app.ui.pages.settings_page import SettingsPage
from the_prof.app.ui.pages.skills_page import SkillsPage


class MainWindow(QMainWindow):
    NAV_ITEMS = [
        "Home",
        "New Project",
        "Project Dashboard",
        "Workflow",
        "Agents",
        "Council Debate",
        "Brain",
        "Sources",
        "Drafts",
        "Reviews",
        "Providers",
        "API Registry",
        "Settings",
        "Help",
        "Logs",
        "Agent Skills",
        "Exports",
    ]

    DASHBOARD_TAB_MAP = {
        "Project Dashboard": "Project",
        "Workflow": "Workflow",
        "Agents": "Agents",
        "Council Debate": "Council Debate",
        "Sources": "Sources",
        "Drafts": "Drafts",
        "Reviews": "Reviews",
        "Providers": "Provider Usage",
        "API Registry": "API Registry",
        "Logs": "Logs",
        "Exports": "Exports",
    }

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.current_project_path: Path | None = None
        self.setWindowTitle("The Prof")
        self.resize(1400, 900)
        self._load_logo()
        self._build_ui()
        self.restore_last_session()

    def _load_logo(self) -> None:
        logo_path = self.context.root / "TheProf_logo.png"
        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))

    def _build_ui(self) -> None:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        toolbar = QToolBar("Project")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        self.project_title = QLabel("No project")
        self.project_title.setObjectName("TitleLabel")
        self.stage_label = QLabel("Stage: idle")
        self.stage_label.setObjectName("SubtitleLabel")
        toolbar.addWidget(self.project_title)
        toolbar.addSeparator()
        toolbar.addWidget(self.stage_label)

        root_widget = QWidget()
        self.setCentralWidget(root_widget)
        root_layout = QHBoxLayout(root_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        root_layout.addWidget(splitter)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        logo_path = self.context.root / "TheProf_logo.png"
        sidebar_logo = QLabel("The Prof")
        sidebar_logo.setObjectName("TitleLabel")
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                sidebar_logo.setPixmap(pixmap.scaledToWidth(160, Qt.TransformationMode.SmoothTransformation))
                sidebar_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(sidebar_logo)
        subtitle = QLabel("Autonomous academic research production")
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setWordWrap(True)
        sidebar_layout.addWidget(subtitle)
        self.nav_list = QListWidget()
        for item in self.NAV_ITEMS:
            QListWidgetItem(item, self.nav_list)
        sidebar_layout.addWidget(self.nav_list)
        quick_run = QPushButton("Run Current Project")
        quick_run.clicked.connect(self.run_current_project)
        sidebar_layout.addWidget(quick_run)
        sidebar_layout.addStretch(1)

        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        self.live_log = QTextEdit()
        self.live_log.setReadOnly(True)
        self.live_log.setMinimumHeight(140)
        content_layout.addWidget(self.live_log)

        splitter.addWidget(sidebar)
        splitter.addWidget(content_container)
        splitter.setSizes([240, 1160])

        self.home_page = HomePage(self.context)
        self.new_project_page = NewProjectPage()
        self.new_project_page.create_requested.connect(self.handle_create_project)
        self.dashboard_page = DashboardPage(self.context)
        self.brain_page = BrainPage(self.context)
        self.providers_page = ProvidersPage(self.context)
        self.settings_page = SettingsPage(self.context)
        self.settings_page.settings_saved.connect(self.reload_context)
        self.help_page = HelpPage(self.context)
        self.skills_page = SkillsPage(self.context)

        self.page_map = {
            "Home": self.home_page,
            "New Project": self.new_project_page,
            "Project Dashboard": self.dashboard_page,
            "Workflow": self.dashboard_page,
            "Agents": self.dashboard_page,
            "Council Debate": self.dashboard_page,
            "Brain": self.brain_page,
            "Sources": self.dashboard_page,
            "Drafts": self.dashboard_page,
            "Reviews": self.dashboard_page,
            "Providers": self.providers_page,
            "API Registry": self.dashboard_page,
            "Settings": self.settings_page,
            "Help": self.help_page,
            "Logs": self.dashboard_page,
            "Agent Skills": self.skills_page,
            "Exports": self.dashboard_page,
        }
        for page in [self.home_page, self.new_project_page, self.dashboard_page, self.brain_page, self.providers_page, self.settings_page, self.help_page, self.skills_page]:
            self.stack.addWidget(page)

        self.nav_list.currentTextChanged.connect(self.switch_page)
        self.nav_list.setCurrentRow(0)

    def append_log(self, message: str) -> None:
        self.live_log.append(message)
        self.status_bar.showMessage(message)
        QApplication.processEvents()

    def switch_page(self, name: str) -> None:
        widget = self.page_map.get(name, self.home_page)
        self.stack.setCurrentWidget(widget)
        if widget is self.dashboard_page and name in self.DASHBOARD_TAB_MAP:
            tab_name = self.DASHBOARD_TAB_MAP[name]
            for idx in range(self.dashboard_page.tabs.count()):
                if self.dashboard_page.tabs.tabText(idx) == tab_name:
                    self.dashboard_page.tabs.setCurrentIndex(idx)
                    break

    def handle_create_project(self, intake, run_after_create: bool) -> None:
        try:
            project_path = self.context.workflow_engine.create_project(intake)
        except Exception as exc:
            QMessageBox.critical(self, "Project Creation Failed", str(exc))
            return
        self.current_project_path = project_path
        self.project_title.setText(project_path.name)
        self.stage_label.setText("Stage: initialized")
        self.context.state_store.save_session({"current_project_id": project_path.name, "current_project_path": str(project_path)})
        self.dashboard_page.load_project(project_path)
        self.append_log(f"Created project {project_path.name}")
        self.nav_list.setCurrentRow(self.NAV_ITEMS.index("Project Dashboard"))
        if run_after_create:
            self.run_project(project_path, intake)

    def run_project(self, project_path: Path, intake) -> None:
        try:
            self.stage_label.setText("Stage: running")
            result = self.context.workflow_engine.run(project_path, intake, log=self.append_log)
            self.stage_label.setText(f"Stage: {result.stage}")
            self.dashboard_page.load_project(project_path)
            self.append_log(f"Workflow complete. Final output: {result.final_output_path}")
        except Exception as exc:
            self.append_log(f"Workflow failed: {exc}")
            QMessageBox.critical(self, "Workflow Failed", str(exc))

    def run_current_project(self) -> None:
        if not self.current_project_path:
            QMessageBox.information(self, "No Project", "Create a project first.")
            return
        project_yaml_path = self.current_project_path / "project.yaml"
        if not project_yaml_path.exists():
            QMessageBox.warning(self, "Missing Project File", "The current project has no project.yaml file.")
            return
        data = yaml.safe_load(project_yaml_path.read_text(encoding="utf-8")) or {}
        settings = data.get("settings", {})
        intake = ProjectIntake(**settings)
        self.run_project(self.current_project_path, intake)

    def reload_context(self) -> None:
        self.context = AppContext(self.context.root)
        self.home_page.context = self.context
        self.dashboard_page.context = self.context
        self.brain_page.context = self.context
        self.providers_page.context = self.context
        self.settings_page.context = self.context
        self.help_page.context = self.context
        self.skills_page.context = self.context
        self.skills_page.load_skills()
        self.settings_page.load_settings()
        self.providers_page.refresh()
        self.append_log("Reloaded application context from saved settings.")
        self.home_page.refresh()
        self.dashboard_page.refresh_api_registry()
        self.dashboard_page.refresh_brain_summary()

    def restore_last_session(self) -> None:
        session = self.context.state_store.load_session()
        current_path = session.get("current_project_path", "")
        if current_path and Path(current_path).exists():
            self.current_project_path = Path(current_path)
            self.project_title.setText(self.current_project_path.name)
            self.dashboard_page.load_project(self.current_project_path)
            self.append_log(f"Restored session for project {self.current_project_path.name}")
