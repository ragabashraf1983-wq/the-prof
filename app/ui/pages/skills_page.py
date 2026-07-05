from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from the_prof.app.launcher import AppContext


class SkillsPage(QWidget):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.current_file: Path | None = None
        self._build_ui()
        self.load_skills()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Agent Skills")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("Edit YAML skill files used by the agent selector. Save carefully; invalid YAML can disable an agent.")
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        splitter = QSplitter()
        self.list_widget = QListWidget()
        self.editor = QPlainTextEdit()
        splitter.addWidget(self.list_widget)
        splitter.addWidget(self.editor)
        splitter.setSizes([320, 900])
        layout.addWidget(splitter, 1)

        actions = QHBoxLayout()
        reload_button = QPushButton("Reload")
        save_button = QPushButton("Save Skill")
        reload_button.clicked.connect(self.load_skills)
        save_button.clicked.connect(self.save_current)
        actions.addStretch(1)
        actions.addWidget(reload_button)
        actions.addWidget(save_button)
        layout.addLayout(actions)
        self.list_widget.currentTextChanged.connect(self.open_skill)

    def _skills_dir(self) -> Path:
        return self.context.source_root / "agents" / "skills"

    def load_skills(self) -> None:
        self.list_widget.clear()
        for path in sorted(self._skills_dir().glob("*.yaml")):
            self.list_widget.addItem(path.name)
        if self.list_widget.count():
            self.list_widget.setCurrentRow(0)

    def open_skill(self, filename: str) -> None:
        if not filename:
            return
        path = self._skills_dir() / filename
        self.current_file = path
        self.editor.setPlainText(path.read_text(encoding="utf-8"))

    def save_current(self) -> None:
        if not self.current_file:
            return
        self.current_file.write_text(self.editor.toPlainText(), encoding="utf-8")
        self.context.agent_registry.skills = self.context.agent_registry._load_skills()
        QMessageBox.information(self, "Saved", f"Saved {self.current_file.name}.")
