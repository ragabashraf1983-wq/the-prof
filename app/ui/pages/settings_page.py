from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from the_prof.app.launcher import AppContext


class SettingsPage(QWidget):
    settings_saved = Signal()

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self._build_ui()
        self.load_settings()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Settings")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("Configure storage, safety, and provider fallback behavior.")
        subtitle.setObjectName("SubtitleLabel")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        general = QGroupBox("General")
        form = QFormLayout(general)
        self.project_dir = QLineEdit()
        self.citation = QLineEdit()
        self.language = QLineEdit()
        self.ollama_url = QLineEdit()
        self.default_model = QLineEdit()
        form.addRow("Project storage directory", self.project_dir)
        form.addRow("Default citation style", self.citation)
        form.addRow("Default output language", self.language)
        form.addRow("Ollama URL", self.ollama_url)
        form.addRow("Default local model", self.default_model)
        layout.addWidget(general)

        access = QGroupBox("Model/API access")
        access_form = QFormLayout(access)
        self.local_only = QCheckBox("Use only local Ollama and deterministic rules")
        self.online_api = QCheckBox("Allow online API providers")
        self.paid_api = QCheckBox("Allow paid providers if enabled")
        self.browser_login = QCheckBox("Allow browser-login helpers only after manual user login")
        access_form.addRow(self.local_only)
        access_form.addRow(self.online_api)
        access_form.addRow(self.paid_api)
        access_form.addRow(self.browser_login)
        layout.addWidget(access)

        safety = QGroupBox("Safety and iteration limits")
        safety_form = QFormLayout(safety)
        self.brain = QCheckBox("Enable brain memory retrieval")
        self.auto_memory = QCheckBox("Suggest memory additions")
        self.iterations = QSpinBox()
        self.iterations.setRange(1, 25)
        self.failures = QSpinBox()
        self.failures.setRange(1, 10)
        self.fallback_order = QLineEdit()
        self.fallback_order.setPlaceholderText("ollama, openrouter, groq, google-ai-studio, rules")
        safety_form.addRow(self.brain)
        safety_form.addRow(self.auto_memory)
        safety_form.addRow("Max autonomous iterations", self.iterations)
        safety_form.addRow("Provider failures before fallback", self.failures)
        safety_form.addRow("Provider fallback order", self.fallback_order)
        layout.addWidget(safety)

        actions = QHBoxLayout()
        save = QPushButton("Save Settings")
        save.clicked.connect(self.save_settings)
        actions.addStretch(1)
        actions.addWidget(save)
        layout.addLayout(actions)
        layout.addStretch(1)

    def load_settings(self) -> None:
        s = self.context.settings
        self.project_dir.setText(str(s.get("project_storage_dir", "projects")))
        self.citation.setText(str(s.get("default_citation_style", "APA 7")))
        self.language.setText(str(s.get("default_output_language", "English")))
        self.ollama_url.setText(str(s.get("ollama_base_url", "http://localhost:11434")))
        self.default_model.setText(str(s.get("default_local_model", "llama3.2")))
        self.local_only.setChecked(bool(s.get("local_only_mode", True)))
        self.online_api.setChecked(bool(s.get("online_api_enabled", False)))
        self.paid_api.setChecked(bool(s.get("paid_api_enabled", False)))
        self.browser_login.setChecked(bool(s.get("browser_login_enabled", False)))
        self.brain.setChecked(bool(s.get("brain_enabled", True)))
        self.auto_memory.setChecked(bool(s.get("auto_suggest_memory_additions", True)))
        self.iterations.setValue(int(s.get("max_autonomous_iterations", 3)))
        self.failures.setValue(int(s.get("max_provider_failures_before_fallback", 2)))
        self.fallback_order.setText(", ".join(s.get("provider_fallback_order", ["ollama", "rules"])))

    def save_settings(self) -> None:
        s = dict(self.context.settings)
        s.update(
            {
                "project_storage_dir": self.project_dir.text().strip() or "projects",
                "default_citation_style": self.citation.text().strip() or "APA 7",
                "default_output_language": self.language.text().strip() or "English",
                "ollama_base_url": self.ollama_url.text().strip() or "http://localhost:11434",
                "default_local_model": self.default_model.text().strip() or "llama3.2",
                "local_only_mode": self.local_only.isChecked(),
                "online_api_enabled": self.online_api.isChecked(),
                "paid_api_enabled": self.paid_api.isChecked(),
                "browser_login_enabled": self.browser_login.isChecked(),
                "brain_enabled": self.brain.isChecked(),
                "auto_suggest_memory_additions": self.auto_memory.isChecked(),
                "max_autonomous_iterations": self.iterations.value(),
                "max_provider_failures_before_fallback": self.failures.value(),
                "provider_fallback_order": [p.strip() for p in self.fallback_order.text().split(",") if p.strip()],
            }
        )
        self.context.save_settings(s)
        QMessageBox.information(self, "Saved", "Settings saved.")
        self.settings_saved.emit()
