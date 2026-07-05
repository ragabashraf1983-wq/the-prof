from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from the_prof.core.models import ProjectIntake


class NewProjectPage(QWidget):
    """Scrollable project intake form.

    The first broken build used a fixed layout, so the bottom create button could
    disappear on smaller screens.  This page is intentionally wrapped in a
    QScrollArea and keeps the action buttons sticky at the page bottom.
    """

    create_requested = Signal(object, bool)

    SCOPES = [
        "Gap Analysis",
        "Research Proposal",
        "Literature Review",
        "Review Paper",
        "Conference Paper",
        "Journal Article",
        "Research Idea Discovery",
        "Research Question Development",
        "Systematic Review Plan",
        "Scoping Review Plan",
        "Grant Proposal",
        "Pilot Study Paper",
    ]

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        root.addWidget(scroll, 1)
        container = QWidget()
        scroll.setWidget(container)
        layout = QVBoxLayout(container)

        header = QHBoxLayout()
        self.logo = QLabel()
        self.logo.setFixedSize(96, 96)
        self.logo.setScaledContents(True)
        pixmap = QPixmap("TheProf_logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap)
            header.addWidget(self.logo)
        title_box = QVBoxLayout()
        title = QLabel("Create a Research Project")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("Answer only what you know. The Prof will use local Ollama, configured API providers, then the safe rules fallback.")
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setWordWrap(True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box, 1)
        layout.addLayout(header)

        form_group = QGroupBox("Required")
        form = QFormLayout(form_group)
        self.topic = QPlainTextEdit()
        self.topic.setPlaceholderText("Example: AI-assisted diabetic retinopathy screening in primary care")
        self.topic.setMinimumHeight(90)
        self.scope = QComboBox()
        self.scope.addItems(self.SCOPES)
        self.discipline = QLineEdit()
        self.discipline.setPlaceholderText("Medicine, Education, Engineering, Business...")
        form.addRow("Topic / problem", self.topic)
        form.addRow("Output type", self.scope)
        form.addRow("Discipline", self.discipline)
        layout.addWidget(form_group)

        detail_group = QGroupBox("Optional guidance")
        detail = QFormLayout(detail_group)
        self.target_venue = QLineEdit()
        self.audience = QLineEdit()
        self.word_count = QLineEdit()
        self.word_count.setPlaceholderText("e.g. 2500, 6000, flexible")
        self.citation_style = QComboBox()
        self.citation_style.addItems(["APA 7", "IEEE", "Vancouver", "Harvard", "MLA", "Chicago"])
        self.methodology = QLineEdit()
        self.framework = QLineEdit()
        self.geo = QLineEdit()
        self.deadline = QLineEdit()
        detail.addRow("Target journal/venue", self.target_venue)
        detail.addRow("Audience", self.audience)
        detail.addRow("Word count", self.word_count)
        detail.addRow("Citation style", self.citation_style)
        detail.addRow("Preferred methodology", self.methodology)
        detail.addRow("Theory/framework", self.framework)
        detail.addRow("Geographic context", self.geo)
        detail.addRow("Deadline", self.deadline)
        layout.addWidget(detail_group)

        data_group = QGroupBox("Data, web access and model/provider choices")
        data = QFormLayout(data_group)
        self.data_availability = QComboBox()
        self.data_availability.addItems(["unknown", "no data yet", "public data", "private data", "simulated data", "literature only"])
        self.empirical = QComboBox()
        self.empirical.addItems(["unknown", "yes", "no", "planned"])
        self.files_exist = QCheckBox("I have files/data I may add manually")
        self.online_search = QCheckBox("Allow online source/API lookup when available")
        self.paid_apis = QCheckBox("Allow paid providers if I enabled them and added keys")
        self.browser_login = QCheckBox("Allow browser-login helpers only for sites where I log in manually")
        self.local_only = QCheckBox("Local-only mode (Ollama/rules only)")
        self.local_only.setChecked(True)
        self.gap_first = QCheckBox("Run gap analysis before drafting")
        self.gap_first.setChecked(True)
        data.addRow("Data availability", self.data_availability)
        data.addRow("Empirical data exists", self.empirical)
        data.addRow("Files", self.files_exist)
        data.addRow("Web/source APIs", self.online_search)
        data.addRow("Paid model APIs", self.paid_apis)
        data.addRow("Browser login", self.browser_login)
        data.addRow("Provider restriction", self.local_only)
        data.addRow("Workflow", self.gap_first)
        layout.addWidget(data_group)

        self.extra = QPlainTextEdit()
        self.extra.setPlaceholderText("Any constraints, must-use sources, excluded topics, country/sector, professor instructions...")
        self.extra.setMinimumHeight(120)
        layout.addWidget(QLabel("Extra instructions"))
        layout.addWidget(self.extra)
        layout.addStretch(1)

        actions = QHBoxLayout()
        self.create_button = QPushButton("Create Project")
        self.create_button.clicked.connect(lambda: self._emit_create(False))
        self.create_run_button = QPushButton("Create Project and Run")
        self.create_run_button.clicked.connect(lambda: self._emit_create(True))
        actions.addStretch(1)
        actions.addWidget(self.create_button)
        actions.addWidget(self.create_run_button)
        root.addLayout(actions)

    def _emit_create(self, run_after_create: bool) -> None:
        topic = self.topic.toPlainText().strip()
        if not topic:
            QMessageBox.warning(self, "Missing topic", "Please enter a research topic or problem first.")
            return
        intake = ProjectIntake(
            topic=topic,
            scope=self.scope.currentText(),
            discipline=self.discipline.text().strip(),
            target_venue=self.target_venue.text().strip(),
            audience=self.audience.text().strip(),
            word_count=self.word_count.text().strip(),
            citation_style=self.citation_style.currentText(),
            preferred_methodology=self.methodology.text().strip(),
            data_availability=self.data_availability.currentText(),
            theoretical_framework=self.framework.text().strip(),
            geographic_context=self.geo.text().strip(),
            deadline=self.deadline.text().strip(),
            empirical_data_exists=self.empirical.currentText(),
            user_files_exist=self.files_exist.isChecked(),
            online_search_allowed=self.online_search.isChecked(),
            paid_apis_allowed=self.paid_apis.isChecked(),
            browser_login_allowed=self.browser_login.isChecked(),
            local_only_mode=self.local_only.isChecked(),
            gap_analysis_first=self.gap_first.isChecked(),
            extra_answers={"extra_instructions": self.extra.toPlainText().strip()},
        )
        self.create_requested.emit(intake, run_after_create)
