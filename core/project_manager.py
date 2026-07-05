from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .models import ProjectIntake, utc_now_iso


class ProjectManager:
    def __init__(self, root: Path, project_storage_dir: str = "projects") -> None:
        self.root = root
        self.projects_dir = root / project_storage_dir
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def slugify(text: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
        return slug[:48] or "project"

    def create_project(self, intake: ProjectIntake) -> Path:
        project_id = f"{utc_now_iso().replace(':', '').replace('-', '').replace('T', '_').replace('Z', '')}_{self.slugify(intake.topic)}"
        project_path = self.projects_dir / project_id
        for subdir in [
            "agent_outputs",
            "reviews",
            "drafts",
            "logs",
            "sources",
            "final",
        ]:
            (project_path / subdir).mkdir(parents=True, exist_ok=True)

        project_doc = {
            "project_id": project_id,
            "created_at": utc_now_iso(),
            "topic": intake.topic,
            "scope": intake.scope,
            "settings": intake.to_dict(),
            "status": "initialized",
            "current_stage": "project_initialization",
        }
        (project_path / "project.yaml").write_text(yaml.safe_dump(project_doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
        (project_path / "intake.md").write_text(self._build_intake_markdown(intake), encoding="utf-8")
        (project_path / "workflow_plan.md").write_text("# Workflow Plan\n\nPending workflow generation.\n", encoding="utf-8")
        (project_path / "selected_agents.md").write_text("# Selected Agents\n\nPending agent selection.\n", encoding="utf-8")
        (project_path / "provider_log.md").write_text("# Provider Log\n\n", encoding="utf-8")
        (project_path / "source_registry.md").write_text("# Source Registry\n\n", encoding="utf-8")
        (project_path / "claim_ledger.md").write_text("# Claim Ledger\n\n", encoding="utf-8")
        (project_path / "memory_usage.md").write_text("# Memory Usage\n\n", encoding="utf-8")
        (project_path / "logs" / "workflow.md").write_text("# Workflow Log\n\n", encoding="utf-8")
        return project_path

    def _build_intake_markdown(self, intake: ProjectIntake) -> str:
        lines = [
            "# Project Intake",
            "",
            f"- **Topic:** {intake.topic}",
            f"- **Scope:** {intake.scope}",
            f"- **Discipline:** {intake.discipline or 'Do not know.'}",
            f"- **Target venue:** {intake.target_venue or 'Do not know.'}",
            f"- **Audience:** {intake.audience or 'Do not know.'}",
            f"- **Word count:** {intake.word_count or 'Do not know.'}",
            f"- **Citation style:** {intake.citation_style}",
            f"- **Preferred methodology:** {intake.preferred_methodology or 'Do not know.'}",
            f"- **Data availability:** {intake.data_availability}",
            f"- **Theoretical framework:** {intake.theoretical_framework or 'Do not know.'}",
            f"- **Geographic context:** {intake.geographic_context or 'Do not know.'}",
            f"- **Deadline:** {intake.deadline or 'Do not know.'}",
            f"- **Empirical data exists:** {intake.empirical_data_exists}",
            f"- **User files exist:** {'Yes' if intake.user_files_exist else 'No'}",
            f"- **Online search allowed:** {'Yes' if intake.online_search_allowed else 'No'}",
            f"- **Paid APIs allowed:** {'Yes' if intake.paid_apis_allowed else 'No'}",
            f"- **Browser login allowed:** {'Yes' if intake.browser_login_allowed else 'No'}",
            f"- **Local only mode:** {'Yes' if intake.local_only_mode else 'No'}",
            f"- **Tone:** {intake.tone}",
            f"- **Gap analysis first:** {'Yes' if intake.gap_analysis_first else 'No'}",
            f"- **Source collection mode:** {intake.source_collection_mode}",
            f"- **Preferred first output:** {intake.preferred_first_output}",
            "",
            "## Extra Answers",
            "",
        ]
        if intake.extra_answers:
            for key, value in intake.extra_answers.items():
                lines.append(f"- **{key}:** {value}")
        else:
            lines.append("- None")
        lines.append("")
        return "\n".join(lines)

    def update_project_yaml(self, project_path: Path, updates: dict) -> None:
        project_file = project_path / "project.yaml"
        data = yaml.safe_load(project_file.read_text(encoding="utf-8")) or {}
        data.update(updates)
        project_file.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def append_markdown(self, path: Path, heading: str, body: str) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(f"\n## {heading}\n\n{body}\n")

    def write_json_artifact(self, path: Path, data: dict) -> None:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
