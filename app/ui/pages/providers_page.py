from __future__ import annotations

import os
from typing import Any

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from the_prof.app.launcher import AppContext


class AddProviderDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Add OpenAI-compatible Provider")
        layout = QFormLayout(self)
        self.name = QLineEdit()
        self.label = QLineEdit()
        self.base_url = QLineEdit()
        self.model = QLineEdit()
        self.api_key_env = QLineEdit()
        self.category = QComboBox()
        self.category.addItems(["Free API", "Paid API", "Local", "Experimental"])
        self.notes = QLineEdit()
        layout.addRow("Unique name", self.name)
        layout.addRow("Display label", self.label)
        layout.addRow("Base URL", self.base_url)
        layout.addRow("Default model", self.model)
        layout.addRow("API key env name", self.api_key_env)
        layout.addRow("Category", self.category)
        layout.addRow("Notes", self.notes)
        buttons = QHBoxLayout()
        ok = QPushButton("Add")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        buttons.addStretch(1)
        buttons.addWidget(ok)
        buttons.addWidget(cancel)
        layout.addRow(buttons)

    def profile(self) -> dict[str, Any]:
        name = self.name.text().strip().lower().replace(" ", "-")
        env = self.api_key_env.text().strip().upper().replace(" ", "_")
        return {
            "name": name,
            "label": self.label.text().strip() or name,
            "provider_type": "api",
            "category": self.category.currentText(),
            "base_url": self.base_url.text().strip().rstrip("/"),
            "model": self.model.text().strip(),
            "api_key_env": env,
            "adapter": "openai-compatible",
            "enabled": True,
            "paid": self.category.currentText() == "Paid API",
            "experimental": self.category.currentText() == "Experimental",
            "notes": self.notes.text().strip(),
        }


class ProvidersPage(QWidget):
    COLUMNS = ["Enabled", "Provider", "Category", "Model", "Base URL", "API key env", "Available", "Message"]

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.profiles: list[dict[str, Any]] = []
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("LLM Providers")
        title.setObjectName("TitleLabel")
        subtitle = QLabel(
            "Enable a provider, paste its API key locally, and save. The Prof will try providers in fallback order and use the safe rules fallback if no model is available."
        )
        subtitle.setObjectName("SubtitleLabel")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        mode_box = QGroupBox("One-click mode")
        mode_layout = QHBoxLayout(mode_box)
        self.local_only = QCheckBox("Local-only: Ollama + rules")
        self.online_enabled = QCheckBox("Allow online API providers")
        self.paid_enabled = QCheckBox("Allow paid providers")
        self.browser_enabled = QCheckBox("Allow manual browser-login helpers")
        mode_layout.addWidget(self.local_only)
        mode_layout.addWidget(self.online_enabled)
        mode_layout.addWidget(self.paid_enabled)
        mode_layout.addWidget(self.browser_enabled)
        layout.addWidget(mode_box)

        self.table = QTableWidget(0, len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, 1)

        key_box = QGroupBox("API keys / tokens stored only on this computer")
        key_layout = QVBoxLayout(key_box)
        self.keys_layout = QFormLayout()
        key_layout.addLayout(self.keys_layout)
        layout.addWidget(key_box)
        self.key_inputs: dict[str, QLineEdit] = {}

        guide = QTextEdit()
        guide.setReadOnly(True)
        guide.setMaximumHeight(120)
        guide.setPlainText(
            "Free/easy options to try first: Ollama local (no key), Google AI Studio, Groq, OpenRouter free models, Hugging Face, Mistral trial/free tier, Cerebras, SambaNova, Together, NVIDIA NIM.\n"
            "Browser-login automation is intentionally limited: it can open/login manually, but it must not bypass CAPTCHAs, paywalls, or a site's rules."
        )
        layout.addWidget(guide)

        actions = QHBoxLayout()
        add = QPushButton("Add Provider")
        open_signup = QPushButton("Open Signup/Login for Selected")
        save = QPushButton("Save Providers and Keys")
        test = QPushButton("Refresh/Test Availability")
        reset = QPushButton("Reset Default Providers")
        add.clicked.connect(self.add_provider)
        open_signup.clicked.connect(self.open_selected_signup)
        save.clicked.connect(self.save)
        test.clicked.connect(self.refresh)
        reset.clicked.connect(self.reset_defaults)
        actions.addWidget(add)
        actions.addWidget(open_signup)
        actions.addStretch(1)
        actions.addWidget(test)
        actions.addWidget(reset)
        actions.addWidget(save)
        layout.addLayout(actions)

    def refresh(self) -> None:
        self.profiles = self.context.provider_catalog.load()
        settings = self.context.settings
        self.local_only.setChecked(bool(settings.get("local_only_mode", True)))
        self.online_enabled.setChecked(bool(settings.get("online_api_enabled", False)))
        self.paid_enabled.setChecked(bool(settings.get("paid_api_enabled", False)))
        self.browser_enabled.setChecked(bool(settings.get("browser_login_enabled", False)))

        detection = {row["name"]: row for row in self.context.workflow_engine.provider_router.detect_available_providers()}
        self.table.setRowCount(len(self.profiles))
        for row_idx, profile in enumerate(self.profiles):
            enabled = QTableWidgetItem()
            enabled.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            enabled.setCheckState(Qt.CheckState.Checked if profile.get("enabled", False) else Qt.CheckState.Unchecked)
            self.table.setItem(row_idx, 0, enabled)
            self.table.setItem(row_idx, 1, QTableWidgetItem(profile.get("label", profile.get("name", ""))))
            self.table.setItem(row_idx, 2, QTableWidgetItem(profile.get("category", "")))
            self.table.setItem(row_idx, 3, QTableWidgetItem(profile.get("model", "")))
            self.table.setItem(row_idx, 4, QTableWidgetItem(profile.get("base_url", "")))
            self.table.setItem(row_idx, 5, QTableWidgetItem(profile.get("api_key_env", "")))
            row = detection.get(profile.get("name", ""), {})
            self.table.setItem(row_idx, 6, QTableWidgetItem(row.get("available", "no")))
            self.table.setItem(row_idx, 7, QTableWidgetItem(row.get("message", "")))
        self._rebuild_key_inputs()

    def _rebuild_key_inputs(self) -> None:
        while self.keys_layout.rowCount():
            self.keys_layout.removeRow(0)
        self.key_inputs = {}
        env_names = []
        for profile in self.profiles:
            env = profile.get("api_key_env", "")
            if env and env not in env_names:
                env_names.append(env)
        for env in env_names:
            edit = QLineEdit()
            edit.setEchoMode(QLineEdit.EchoMode.Password)
            existing = self.context.secrets_store.get_secret(env) or os.getenv(env, "")
            if existing:
                edit.setPlaceholderText("Saved key exists; leave blank to keep it")
            else:
                edit.setPlaceholderText(f"Paste {env} here")
            self.key_inputs[env] = edit
            self.keys_layout.addRow(env, edit)

    def save(self) -> None:
        for row_idx, profile in enumerate(self.profiles):
            checkbox = self.table.item(row_idx, 0)
            profile["enabled"] = checkbox.checkState() == Qt.CheckState.Checked if checkbox else False
            profile["label"] = self.table.item(row_idx, 1).text().strip() if self.table.item(row_idx, 1) else profile.get("label", "")
            profile["category"] = self.table.item(row_idx, 2).text().strip() if self.table.item(row_idx, 2) else profile.get("category", "")
            profile["model"] = self.table.item(row_idx, 3).text().strip() if self.table.item(row_idx, 3) else profile.get("model", "")
            profile["base_url"] = self.table.item(row_idx, 4).text().strip().rstrip("/") if self.table.item(row_idx, 4) else profile.get("base_url", "")
            profile["api_key_env"] = self.table.item(row_idx, 5).text().strip() if self.table.item(row_idx, 5) else profile.get("api_key_env", "")
        self.context.provider_catalog.save(self.profiles)
        for env, edit in self.key_inputs.items():
            value = edit.text().strip()
            if value:
                self.context.secrets_store.set_secret(env, value)
                os.environ[env] = value
                edit.clear()
                edit.setPlaceholderText("Saved key exists; leave blank to keep it")
        settings = dict(self.context.settings)
        settings["local_only_mode"] = self.local_only.isChecked()
        settings["online_api_enabled"] = self.online_enabled.isChecked()
        settings["paid_api_enabled"] = self.paid_enabled.isChecked()
        settings["browser_login_enabled"] = self.browser_enabled.isChecked()
        self.context.save_settings(settings)
        QMessageBox.information(self, "Saved", "Providers, API keys, and model access settings were saved locally.")
        self.refresh()

    def add_provider(self) -> None:
        dialog = AddProviderDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        profile = dialog.profile()
        if not profile["name"] or not profile["base_url"] or not profile["model"]:
            QMessageBox.warning(self, "Missing details", "Name, base URL, and model are required.")
            return
        if any(p.get("name") == profile["name"] for p in self.profiles):
            QMessageBox.warning(self, "Duplicate", "A provider with this name already exists.")
            return
        self.profiles.append(profile)
        self.context.provider_catalog.save(self.profiles)
        self.context.workflow_engine.provider_router.providers = self.context.workflow_engine.provider_router._build_providers()
        self.refresh()

    def open_selected_signup(self) -> None:
        row = self.table.currentRow()
        if row < 0 or row >= len(self.profiles):
            QMessageBox.information(self, "Select provider", "Click a provider row first.")
            return
        url = self.profiles[row].get("signup_url", "")
        if not url:
            QMessageBox.information(self, "No link", "This provider profile has no signup/login URL yet.")
            return
        QDesktopServices.openUrl(QUrl(url))

    def reset_defaults(self) -> None:
        if QMessageBox.question(self, "Reset providers", "Reset provider list to the built-in defaults? Saved API keys are not deleted.") != QMessageBox.StandardButton.Yes:
            return
        self.context.provider_catalog.reset_to_defaults()
        self.context.workflow_engine.provider_router.providers = self.context.workflow_engine.provider_router._build_providers()
        self.refresh()
