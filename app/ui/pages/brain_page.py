from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from the_prof.app.launcher import AppContext


class BrainPage(QWidget):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.search_edit = QLineEdit()
        self.import_edit = QLineEdit(str(context.root / "exports" / "brain_import.md"))
        self.export_edit = QLineEdit(str(context.root / "exports" / "brain_export.md"))
        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(False)
        self._build_ui()
        self.refresh_overview()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Brain Memory")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)
        layout.addWidget(QLabel("Search, inspect, import, export, and manually extend brain.md."))

        form = QFormLayout()
        form.addRow("Search brain", self.search_edit)
        form.addRow("Import path", self.import_edit)
        form.addRow("Export path", self.export_edit)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_overview)
        add_demo_button = QPushButton("Add Sample Verified Fact")
        add_demo_button.clicked.connect(self.add_sample_fact)
        import_button = QPushButton("Import")
        import_button.clicked.connect(self.import_brain)
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_brain)
        for widget in [search_button, refresh_button, add_demo_button, import_button, export_button]:
            buttons.addWidget(widget)
        layout.addLayout(buttons)
        layout.addWidget(self.result_box)

    def refresh_overview(self) -> None:
        index_path = self.context.workflow_engine.brain_manager.index_path
        brain_text = self.context.workflow_engine.brain_manager.brain_path.read_text(encoding="utf-8")
        self.result_box.setPlainText(brain_text + "\n\n# Index Path\n\n" + str(index_path))

    def search(self) -> None:
        query = self.search_edit.text().strip()
        results = self.context.workflow_engine.memory_search.search(query) if query else []
        lines = [f"# Search Results for: {query}", ""]
        if not results:
            lines.append("- No matching facts found.")
        else:
            for hit in results:
                lines.append(
                    f"- `{hit.fact.fact_id}` {hit.fact.statement} | verification={hit.fact.verification_status} | freshness={hit.freshness}"
                )
        self.result_box.setPlainText("\n".join(lines))

    def add_sample_fact(self) -> None:
        fact = self.context.workflow_engine.brain_manager.add_verified_fact(
            statement="Crossref exposes DOI-linked scholarly metadata via its public Works API.",
            category="research infrastructure",
            source="https://api.crossref.org/works",
            citation_metadata="Crossref Works API documentation",
            stability="slow-changing",
            added_by="user-approved sample",
            notes="Inserted as a portable sample fact to demonstrate brain memory behavior.",
        )
        self.result_box.setPlainText(f"Added sample fact {fact.fact_id}.\n\n" + self.context.workflow_engine.brain_manager.brain_path.read_text(encoding="utf-8"))

    def import_brain(self) -> None:
        path = Path(self.import_edit.text().strip())
        if not path.exists():
            self.result_box.setPlainText(f"Import file not found: {path}")
            return
        report = self.context.workflow_engine.brain_manager.import_brain(path)
        self.result_box.setPlainText(f"Imported brain file with report: {report}")

    def export_brain(self) -> None:
        path = Path(self.export_edit.text().strip())
        path.parent.mkdir(parents=True, exist_ok=True)
        self.context.workflow_engine.brain_manager.export_brain(path)
        self.result_box.setPlainText(f"Exported brain.md to {path}")
