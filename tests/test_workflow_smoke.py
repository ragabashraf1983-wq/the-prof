from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from the_prof.agents.registry import AgentRegistry
from the_prof.apis.api_registry import APIRegistry
from the_prof.core.models import ProjectIntake
from the_prof.core.workflow_engine import WorkflowEngine


class WorkflowSmokeTests(unittest.TestCase):
    def make_engine(self, root: Path) -> WorkflowEngine:
        settings = {
            "project_storage_dir": "projects",
            "brain_enabled": True,
            "stable_revalidation_days": 180,
            "slow_changing_revalidation_days": 60,
            "time_sensitive_revalidation_days": 14,
            "provider_fallback_order": ["rules"],
            "max_provider_failures_before_fallback": 1,
            "ollama_base_url": "http://localhost:11434",
            "local_only_mode": True,
        }
        registry = AgentRegistry(root / "the_prof" / "agents" / "skills")
        api_registry = APIRegistry(root / "the_prof" / "apis" / "imported_sources", root / "storage" / "local_db" / "api_registry.json")
        return WorkflowEngine(root, settings, registry, api_registry)

    def test_gap_analysis_local_only(self) -> None:
        root = Path(__file__).resolve().parents[1]
        engine = self.make_engine(root)
        engine.brain_manager.add_verified_fact(
            statement="Local-first systems reduce dependence on remote services for routine workflow continuity.",
            category="software architecture",
            source="user-approved internal note",
            citation_metadata="internal sample",
            stability="stable",
            added_by="test",
            notes="smoke test",
        )
        intake = ProjectIntake(topic="Local-first academic research tools", scope="Gap Analysis")
        project_path = engine.create_project(intake)
        result = engine.run(project_path, intake)
        self.assertTrue(result.final_output_path.exists())
        text = result.final_output_path.read_text(encoding="utf-8")
        self.assertIn("# Gap Analysis", text)
        self.assertTrue(result.source_audit_path.exists())
        self.assertTrue(result.claim_ledger_path.exists())
        self.assertTrue(result.memory_report_path.exists())

    def test_research_proposal_local_only(self) -> None:
        root = Path(__file__).resolve().parents[1]
        engine = self.make_engine(root)
        intake = ProjectIntake(topic="Privacy-aware literature review agents", scope="Research Proposal")
        project_path = engine.create_project(intake)
        result = engine.run(project_path, intake)
        text = result.final_output_path.read_text(encoding="utf-8")
        self.assertIn("# Research Proposal", text)
        self.assertIn("## Integrity Note", text)


if __name__ == "__main__":
    unittest.main()
