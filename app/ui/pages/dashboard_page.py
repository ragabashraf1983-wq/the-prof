from __future__ import annotations

import json
from pathlib import Path

import yaml
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget

from the_prof.app.launcher import AppContext


class DashboardPage(QWidget):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.project_path: Path | None = None
        self.summary_label = QLabel("No project loaded.")
        self.summary_label.setObjectName("SubtitleLabel")
        self.tabs = QTabWidget()
        self.text_tabs: dict[str, QPlainTextEdit] = {}
        for name in [
            "Project",
            "Workflow",
            "Agents",
            "Council Debate",
            "Brain",
            "Sources",
            "Drafts",
            "Reviews",
            "Logs",
            "Agent Skills",
            "Exports",
        ]:
            editor = QPlainTextEdit()
            editor.setReadOnly(True)
            self.text_tabs[name] = editor
            self.tabs.addTab(editor, name)
        self.provider_table = QTableWidget(0, 5)
        self.provider_table.setHorizontalHeaderLabels(["Provider", "Model", "Task", "Success", "Error"])
        self.provider_table.horizontalHeader().setStretchLastSection(True)
        self.tabs.addTab(self.provider_table, "Provider Usage")

        self.api_table = QTableWidget(0, 5)
        self.api_table.setHorizontalHeaderLabels(["Name", "Category", "Endpoint", "Status", "Source Repo"])
        self.api_table.horizontalHeader().setStretchLastSection(True)
        self.tabs.addTab(self.api_table, "API Registry")

        layout = QVBoxLayout(self)
        title = QLabel("Project Dashboard")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.tabs)
        self.refresh_api_registry()
        self.refresh_brain_summary()

    def load_project(self, project_path: Path) -> None:
        self.project_path = project_path
        project_yaml = yaml.safe_load((project_path / "project.yaml").read_text(encoding="utf-8"))
        self.summary_label.setText(
            f"Current project: {project_yaml.get('project_id', '')} | Stage: {project_yaml.get('current_stage', '')} | Status: {project_yaml.get('status', '')}"
        )
        mapping = {
            "Project": project_path / "intake.md",
            "Workflow": project_path / "workflow_plan.md",
            "Agents": project_path / "selected_agents.md",
            "Council Debate": project_path / "reviews" / "council_debate.md",
            "Brain": self.context.workflow_engine.brain_manager.brain_path,
            "Sources": project_path / "source_registry.md",
            "Drafts": project_path / "final" / "final_output.md",
            "Reviews": project_path / "reviews" / "internal_review.md",
            "Logs": project_path / "logs" / "workflow.md",
            "Agent Skills": self._skills_snapshot_path(project_path),
            "Exports": project_path / "final" / "integrity_report.md",
        }
        for name, path in mapping.items():
            text = path.read_text(encoding="utf-8") if path.exists() else "No content yet."
            self.text_tabs[name].setPlainText(text)
        self.refresh_provider_usage(project_path)
        self.refresh_api_registry()
        self.refresh_brain_summary()

    def _skills_snapshot_path(self, project_path: Path) -> Path:
        snapshot = project_path / "agent_outputs" / "_skill_snapshot.md"
        lines = ["# Agent Skill Snapshot", ""]
        for skill in self.context.agent_registry.list_skills()[:12]:
            lines.append(f"- **{skill.name}** — {skill.bounded_task}")
        snapshot.write_text("\n".join(lines), encoding="utf-8")
        return snapshot

    def refresh_provider_usage(self, project_path: Path | None = None) -> None:
        rows = self.context.workflow_engine.provider_router.provider_usage_rows()
        if project_path:
            provider_log_path = project_path / "provider_log.md"
            if provider_log_path.exists() and not rows:
                text = provider_log_path.read_text(encoding="utf-8")
                self.text_tabs["Logs"].appendPlainText("\n\n# Provider log snapshot\n\n" + text)
        self.provider_table.setRowCount(len(rows))
        for index, row in enumerate(rows):
            self.provider_table.setItem(index, 0, QTableWidgetItem(str(row.get("provider_name", ""))))
            self.provider_table.setItem(index, 1, QTableWidgetItem(str(row.get("model", ""))))
            self.provider_table.setItem(index, 2, QTableWidgetItem(str(row.get("task", ""))))
            self.provider_table.setItem(index, 3, QTableWidgetItem(str(row.get("success", ""))))
            self.provider_table.setItem(index, 4, QTableWidgetItem(str(row.get("error", ""))))

    def refresh_api_registry(self) -> None:
        records = self.context.api_registry.load()
        self.api_table.setRowCount(len(records))
        for index, record in enumerate(records):
            self.api_table.setItem(index, 0, QTableWidgetItem(record.get("name", "")))
            self.api_table.setItem(index, 1, QTableWidgetItem(record.get("category", "")))
            self.api_table.setItem(index, 2, QTableWidgetItem(record.get("endpoint", "")))
            self.api_table.setItem(index, 3, QTableWidgetItem(record.get("last_test_status", record.get("integration_status", "seeded"))))
            self.api_table.setItem(index, 4, QTableWidgetItem(record.get("source_repository", "")))

    def refresh_brain_summary(self) -> None:
        index = json.loads(self.context.workflow_engine.brain_manager.index_path.read_text(encoding="utf-8"))
        summary_lines = ["# Brain Summary", "", f"- Total indexed facts: {len(index)}", ""]
        for item in index[:10]:
            summary_lines.append(f"- `{item['fact_id']}` {item['statement']}")
        self.text_tabs["Brain"].setPlainText("\n".join(summary_lines))
