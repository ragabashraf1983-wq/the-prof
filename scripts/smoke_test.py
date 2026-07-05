from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from the_prof.agents.registry import AgentRegistry
from the_prof.apis.api_registry import APIRegistry
from the_prof.core.models import ProjectIntake
from the_prof.core.workflow_engine import WorkflowEngine


def run() -> None:
    root = Path(__file__).resolve().parents[1]
    settings = {
        "project_storage_dir": "projects",
        "brain_enabled": True,
        "stable_revalidation_days": 180,
        "slow_changing_revalidation_days": 60,
        "time_sensitive_revalidation_days": 14,
        "provider_fallback_order": ["ollama", "rules"],
        "max_provider_failures_before_fallback": 1,
        "ollama_base_url": "http://localhost:11434",
        "local_only_mode": False,
    }
    registry = AgentRegistry(root / "the_prof" / "agents" / "skills")
    api_registry = APIRegistry(root / "the_prof" / "apis" / "imported_sources", root / "storage" / "local_db" / "api_registry.json")
    engine = WorkflowEngine(root, settings, registry, api_registry)

    engine.brain_manager.add_verified_fact(
        statement="Crossref provides DOI-linked metadata through its public Works API.",
        category="research infrastructure",
        source="https://api.crossref.org/works",
        citation_metadata="Crossref Works API",
        stability="slow-changing",
        added_by="smoke-test",
        notes="Used to verify brain memory integration.",
    )

    gap_intake = ProjectIntake(
        topic="Explainable AI in healthcare imaging",
        scope="Gap Analysis",
        discipline="Computer Science / Medical Imaging",
        online_search_allowed=True,
        local_only_mode=False,
        citation_style="APA 7",
        preferred_first_output="gap analysis",
    )
    gap_project = engine.create_project(gap_intake)
    gap_result = engine.run(gap_project, gap_intake, log=lambda message: print("[gap]", message))

    proposal_intake = ProjectIntake(
        topic="Federated learning for medical image segmentation",
        scope="Research Proposal",
        discipline="Computer Science / Medical Imaging",
        online_search_allowed=True,
        local_only_mode=False,
        preferred_methodology="comparative literature-backed proposal",
        citation_style="APA 7",
        preferred_first_output="proposal",
    )
    proposal_project = engine.create_project(proposal_intake)
    proposal_result = engine.run(proposal_project, proposal_intake, log=lambda message: print("[proposal]", message))

    print("SMOKE TEST COMPLETE")
    print(gap_result.final_output_path)
    print(proposal_result.final_output_path)


if __name__ == "__main__":
    run()
