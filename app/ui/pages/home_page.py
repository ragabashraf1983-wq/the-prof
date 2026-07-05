from __future__ import annotations

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from the_prof.app.launcher import AppContext


class HomePage(QWidget):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.logo = QLabel()
        self.logo.setMaximumHeight(180)
        self.logo.setScaledContents(False)
        logo_path = self.context.root / "TheProf_logo.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                self.logo.setPixmap(pixmap.scaledToHeight(150))
        self.title = QLabel("The Prof")
        self.title.setObjectName("TitleLabel")
        self.subtitle = QLabel("Local-first autonomous academic research production. Connect Ollama or API providers, create a project, then click run.")
        self.subtitle.setObjectName("SubtitleLabel")
        self.subtitle.setWordWrap(True)
        self.provider_table = QTableWidget(0, 6)
        self.provider_table.setHorizontalHeaderLabels(["Provider", "Enabled", "Available", "Category", "Model", "Message"])
        self.provider_table.horizontalHeader().setStretchLastSection(True)
        self.models_box = QPlainTextEdit()
        self.models_box.setReadOnly(True)
        layout = QVBoxLayout(self)
        if self.logo.pixmap() is not None:
            layout.addWidget(self.logo)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(QLabel("Detected LLM Providers"))
        layout.addWidget(self.provider_table)
        layout.addWidget(QLabel("Ollama Model Suitability (if available)"))
        layout.addWidget(self.models_box)
        self.refresh()

    def refresh(self) -> None:
        rows = self.context.workflow_engine.provider_router.detect_available_providers()
        self.provider_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            self.provider_table.setItem(row_index, 0, QTableWidgetItem(row["label"]))
            self.provider_table.setItem(row_index, 1, QTableWidgetItem(row["enabled"]))
            self.provider_table.setItem(row_index, 2, QTableWidgetItem(row["available"]))
            self.provider_table.setItem(row_index, 3, QTableWidgetItem(row["category"]))
            self.provider_table.setItem(row_index, 4, QTableWidgetItem(row["model"]))
            self.provider_table.setItem(row_index, 5, QTableWidgetItem(row["message"]))
        self._refresh_models()

    def _refresh_models(self) -> None:
        provider = self.context.workflow_engine.provider_router.providers.get("ollama")
        if not provider:
            self.models_box.setPlainText("Ollama provider not configured.")
            return
        models = provider.list_models() if hasattr(provider, "list_models") else []
        if not models:
            self.models_box.setPlainText(
                "No Ollama models detected. Quick start:\n"
                "1) Install Ollama from https://ollama.com\n"
                "2) Run: ollama pull llama3.2\n"
                "3) Reopen The Prof or click Refresh/Test Availability in Providers.\n\n"
                "If you prefer cloud models, open Providers, disable Local-only, enable a free/API provider, paste its key, and save."
            )
            return
        lines = []
        for model in sorted(models, key=lambda item: item.size or 0):
            size_gb = (model.size or 0) / (1024 ** 3)
            if size_gb <= 6:
                rank = "Good for modest PCs"
            elif size_gb <= 20:
                rank = "Balanced for mid-range systems"
            else:
                rank = "Best for stronger hardware"
            lines.append(f"- {model.name} | ~{size_gb:.2f} GB | family={model.family or 'unknown'} | {rank}")
        self.models_box.setPlainText("\n".join(lines))
