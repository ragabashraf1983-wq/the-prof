from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowStage:
    name: str
    description: str


DEFAULT_STAGES: list[WorkflowStage] = [
    WorkflowStage("project_initialization", "Create project directory and base documents."),
    WorkflowStage("user_intake", "Persist intake answers and derived scope configuration."),
    WorkflowStage("scope_interpretation", "Determine workflow template from requested academic scope."),
    WorkflowStage("brain_memory_search", "Check brain.md, references, and local cache first."),
    WorkflowStage("agent_selection", "Select only the required agents for the requested scope."),
    WorkflowStage("prior_art_scan", "Collect or reuse literature and prior-art signals."),
    WorkflowStage("source_audit", "Verify collected sources and create the source registry."),
    WorkflowStage("research_plan", "Build a bounded research or writing plan."),
    WorkflowStage("draft_outline", "Create conservative outline and section plan."),
    WorkflowStage("section_drafting", "Produce initial markdown sections using verified support only."),
    WorkflowStage("internal_review", "Run internal review and revision recommendations."),
    WorkflowStage("council_debate", "Resolve disagreements and document unresolved issues."),
    WorkflowStage("integrity_check", "Block unsupported claims and finalize audit reports."),
    WorkflowStage("markdown_formatting", "Write final markdown package."),
    WorkflowStage("memory_update_proposal", "Propose new facts for brain.md or mark pending."),
    WorkflowStage("final_project_package", "Persist final files and completion state."),
]
