from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPlainTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from the_prof.app.launcher import AppContext


class HomePage(QWidget):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.title = QLabel("The Prof")
        self.title.setObjectName("TitleLabel")
        self.subtitle = QLabel("Local-first autonomous academic research production for Windows desktop.")
        self.subtitle.setObjectName("SubtitleLabel")
        self.provider_table = QTableWidget(0, 3)
        self.provider_table.setHorizontalHeaderLabels(["Provider", "Available", "Message"])
        self.provider_table.horizontalHeader().setStretchLastSection(True)
        self.models_box = QPlainTextEdit()
        self.models_box.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(QLabel("Detected Providers"))
        layout.addWidget(self.provider_table)
        layout.addWidget(QLabel("Ollama Model Suitability (if available)"))
        layout.addWidget(self.models_box)
        self.refresh()

    def refresh(self) -> None:
        rows = self.context.workflow_engine.provider_router.detect_available_providers()
        self.provider_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            self.provider_table.setItem(row_index, 0, QTableWidgetItem(row["name"]))
            self.provider_table.setItem(row_index, 1, QTableWidgetItem(row["available"]))
            self.provider_table.setItem(row_index, 2, QTableWidgetItem(row["message"]))
        self._refresh_models()

    def _refresh_models(self) -> None:
        provider = self.context.workflow_engine.provider_router.providers.get("ollama")
        if not provider:
            self.models_box.setPlainText("Ollama provider not configured.")
            return
        models = provider.list_models() if hasattr(provider, "list_models") else []
        if not models:
            self.models_box.setPlainText(
                "No Ollama models detected. When Ollama is available, this panel ranks models roughly by portable suitability:\n"
                "- Small/8B-ish: best for lower-memory PCs\n"
                "- Medium/14B-32B-ish: balanced if RAM/VRAM allows\n"
                "- Large/70B+: only for high-end systems\n"
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
            lines.append(
                f"- {model.name} | ~{size_gb:.2f} GB | family={model.family or 'unknown'} | {rank}"
            )
        self.models_box.setPlainText("\n".join(lines))
