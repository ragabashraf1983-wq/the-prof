from __future__ import annotations

from pathlib import Path
from typing import Callable

from the_prof.agents.agent_selector import AgentSelector
from the_prof.agents.registry import AgentRegistry
from the_prof.apis.api_registry import APIRegistry
from the_prof.core.audit_log import AuditLog
from the_prof.core.integrity_governor import IntegrityGovernor
from the_prof.core.models import AgentRunRecord, ProjectIntake, SourceRecord, WorkflowResult
from the_prof.memory.brain_manager import BrainManager
from the_prof.memory.memory_search import MemorySearch
from the_prof.memory.reference_memory import ReferenceMemory
from the_prof.providers.provider_catalog import ProviderCatalog
from the_prof.providers.provider_router import ProviderRouter
from the_prof.research.citation_validator import CitationValidator
from the_prof.research.claim_ledger import ClaimLedger
from the_prof.research.gap_analysis import GapAnalysisBuilder
from the_prof.research.literature_review import LiteratureReviewBuilder
from the_prof.research.source_audit import SourceAudit
from the_prof.research.source_search import SourceSearch

from .project_manager import ProjectManager
from .task_graph import DEFAULT_STAGES

LogCallback = Callable[[str], None]


class WorkflowEngine:
    def __init__(self, root: Path, settings: dict, agent_registry: AgentRegistry, api_registry: APIRegistry, provider_catalog: ProviderCatalog | None = None) -> None:
        self.root = root
        self.settings = settings
        self.agent_registry = agent_registry
        self.api_registry = api_registry
        self.project_manager = ProjectManager(root, settings.get("project_storage_dir", "projects"))
        self.brain_manager = BrainManager(
            root,
            stable_days=int(settings.get("stable_revalidation_days", 180)),
            slow_days=int(settings.get("slow_changing_revalidation_days", 60)),
            sensitive_days=int(settings.get("time_sensitive_revalidation_days", 14)),
        )
        self.memory_search = MemorySearch(self.brain_manager)
        self.reference_memory = ReferenceMemory(self.brain_manager.references_path)
        self.agent_selector = AgentSelector()
        self.provider_catalog = provider_catalog
        self.provider_router = ProviderRouter(settings, root, provider_catalog)
        self.source_search = SourceSearch()
        self.citation_validator = CitationValidator()
        self.source_audit = SourceAudit()
        self.claim_ledger = ClaimLedger()
        self.gap_builder = GapAnalysisBuilder()
        self.literature_builder = LiteratureReviewBuilder()
        self.integrity_governor = IntegrityGovernor()

    def create_project(self, intake: ProjectIntake) -> Path:
        return self.project_manager.create_project(intake)

    def run(self, project_path: Path, intake: ProjectIntake, log: LogCallback | None = None) -> WorkflowResult:
        log = log or (lambda message: None)
        audit = AuditLog(project_path / "logs" / "workflow.md")

        def note(message: str) -> None:
            audit.info(message)
            log(message)

        note("Workflow started.")
        self.project_manager.update_project_yaml(project_path, {"status": "running", "current_stage": "brain_memory_search"})

        memory_hits = self.memory_search.search(intake.topic) if self.settings.get("brain_enabled", True) else []
        memory_lines = []
        for hit in memory_hits:
            memory_lines.append(
                f"- `{hit.fact.fact_id}` {hit.fact.statement} — freshness: {hit.freshness} — reusable without recheck: {'Yes' if hit.reusable_without_recheck else 'No'}"
            )
        note(f"Brain search completed with {len(memory_hits)} matching fact(s).")

        selected_agent_names = self.agent_selector.select(intake)
        selected_agents_doc = ["# Selected Agents", ""]
        for name in selected_agent_names:
            skill = self.agent_registry.get(name)
            selected_agents_doc.extend([f"## {name}", "", f"- **Role:** {skill.role}", f"- **Bounded task:** {skill.bounded_task}", f"- **Skill file:** {skill.skill_file.name}", ""])
        (project_path / "selected_agents.md").write_text("\n".join(selected_agents_doc), encoding="utf-8")
        note(f"Selected {len(selected_agent_names)} agent(s).")

        workflow_plan = ["# Workflow Plan", ""]
        for stage in DEFAULT_STAGES:
            workflow_plan.append(f"- **{stage.name}** — {stage.description}")
        (project_path / "workflow_plan.md").write_text("\n".join(workflow_plan), encoding="utf-8")

        sources = self.source_search.search(intake.topic, online_allowed=intake.online_search_allowed and not intake.local_only_mode)
        for source in sources:
            status, notes = self.citation_validator.validate(source, online_allowed=intake.online_search_allowed)
            source.verification_status = status if status in {"verified", "unverified"} else "partially verified"
            source.citation_status = status
            source.notes = notes
            source.used_in_output = True
            self.reference_memory.add_reference_markdown(source, project_path.name)
        note(f"Collected {len(sources)} source(s).")
        self.source_audit.write_registry(project_path / "source_registry.md", sources)

        claims = []
        if sources:
            claims.append(
                self.claim_ledger.new_claim(
                    claim_text=f"The current run retrieved {len(sources)} verified source record(s) relevant to the topic query.",
                    kind="fact",
                    source_support=[source.source_id for source in sources],
                    memory_support=[],
                    confidence="medium",
                    agent="Prior Art Detective Agent",
                    verification_status="verified",
                )
            )
            if sources[0].title:
                claims.append(
                    self.claim_ledger.new_claim(
                        claim_text=f"At least one retrieved source title is '{sources[0].title}'.",
                        kind="fact",
                        source_support=[sources[0].source_id],
                        memory_support=[],
                        confidence="high",
                        agent="Prior Art Detective Agent",
                        verification_status="verified",
                    )
                )
        for hit in memory_hits[:3]:
            claims.append(
                self.claim_ledger.new_claim(
                    claim_text=hit.fact.statement,
                    kind="fact",
                    source_support=[],
                    memory_support=[hit.fact.fact_id],
                    confidence=hit.fact.confidence,
                    agent="Principal Investigator Agent",
                    verification_status=hit.fact.verification_status,
                    notes=f"Brain freshness: {hit.freshness}",
                )
            )

        draft_body = self._build_primary_output(intake, sources, claims, memory_lines)
        llm_augmented_body = self._llm_enhance_primary_output(intake, sources, draft_body)
        if llm_augmented_body:
            draft_body = llm_augmented_body

        review_prompt = (
            "Review the following academic draft conservatively. List only issues that can be justified by the provided text. "
            "If evidence is missing, say Do not know.\n\n" + draft_body[:5000]
        )
        review_result = self.provider_router.generate("internal_review", review_prompt)
        review_text = review_result.text or "Do not know."
        (project_path / "reviews" / "internal_review.md").write_text(f"# Internal Review\n\n{review_text}\n", encoding="utf-8")

        debate_prompt = (
            "Create a short council-style debate summary about the draft's strongest risk areas. "
            "Use only the provided text and say Do not know when support is absent.\n\n" + draft_body[:5000]
        )
        debate_result = self.provider_router.generate("council_debate", debate_prompt)
        debate_text = debate_result.text or "Do not know."
        (project_path / "reviews" / "council_debate.md").write_text(f"# Council Debate\n\n{debate_text}\n", encoding="utf-8")

        final_output_path = project_path / "final" / "final_output.md"
        source_audit_path = project_path / "final" / "source_audit.md"
        claim_ledger_path = project_path / "final" / "claim_ledger.md"
        integrity_report_path = project_path / "final" / "integrity_report.md"
        memory_report_path = project_path / "final" / "memory_report.md"

        final_output = draft_body + "\n\n## Internal Review Snapshot\n\n" + review_text + "\n\n## Council Debate Snapshot\n\n" + debate_text + "\n"
        final_output_path.write_text(final_output, encoding="utf-8")
        self.source_audit.write_final_audit(source_audit_path, sources)
        self.claim_ledger.write_markdown(claim_ledger_path, claims)
        integrity_report_path.write_text(self.integrity_governor.build_integrity_report(claims, {s.source_id: s for s in sources}), encoding="utf-8")
        memory_report_path.write_text(self._build_memory_report(memory_hits, project_path.name), encoding="utf-8")
        (project_path / "memory_usage.md").write_text(self._build_memory_report(memory_hits, project_path.name), encoding="utf-8")

        provider_log_lines = ["# Provider Log", ""]
        for row in self.provider_router.provider_usage_rows():
            provider_log_lines.append(
                f"- [{row['timestamp']}] {row['provider_name']} / {row['model']} / {row['task']} / success={row['success']} / error={row['error'] or 'none'}"
            )
        (project_path / "provider_log.md").write_text("\n".join(provider_log_lines), encoding="utf-8")

        for agent_name in selected_agent_names:
            skill = self.agent_registry.get(agent_name)
            record = AgentRunRecord(
                agent_name=agent_name,
                role=skill.role,
                task=skill.bounded_task,
                provider_used=review_result.provider_name if "Reviewer" in agent_name or "Markdown" in agent_name else "deterministic",
                input_summary=intake.topic,
                output_summary="Stage output recorded in project artifacts.",
            )
            (project_path / "agent_outputs" / f"{skill.skill_file.stem}.md").write_text(
                "# Agent Output Summary\n\n"
                f"- **Agent:** {record.agent_name}\n"
                f"- **Role:** {record.role}\n"
                f"- **Task:** {record.task}\n"
                f"- **Provider used:** {record.provider_used}\n"
                f"- **Input summary:** {record.input_summary}\n"
                f"- **Output summary:** {record.output_summary}\n",
                encoding="utf-8",
            )

        self.project_manager.update_project_yaml(project_path, {"status": "complete", "current_stage": "final_project_package"})
        note("Workflow completed.")
        return WorkflowResult(
            project_id=project_path.name,
            project_path=project_path,
            stage="final_project_package",
            final_output_path=final_output_path,
            source_audit_path=source_audit_path,
            claim_ledger_path=claim_ledger_path,
            integrity_report_path=integrity_report_path,
            memory_report_path=memory_report_path,
            selected_agents=selected_agent_names,
            provider_log=self.provider_router.provider_usage_rows(),
        )

    def _build_primary_output(self, intake: ProjectIntake, sources: list[SourceRecord], claims, memory_lines: list[str]) -> str:
        if intake.scope == "Gap Analysis":
            return self.gap_builder.build(intake, sources, claims, memory_lines)
        if intake.scope in {"Research Proposal", "Grant Proposal", "Pilot Study Paper"}:
            return self.literature_builder.build_proposal(intake, sources, claims)
        return self.literature_builder.build_review(intake, sources, claims)

    def _llm_enhance_primary_output(self, intake: ProjectIntake, sources: list[SourceRecord], draft_body: str) -> str:
        if not sources:
            return ""
        evidence_lines = []
        for source in sources[:8]:
            evidence_lines.append(
                f"- {source.source_id}: {source.title} | year={source.year or 'Do not know.'} | venue={source.venue or source.source_type}"
            )
        prompt = (
            f"Rewrite the following {intake.scope} draft into a clearer academic Markdown output. "
            "Rules: use only the provided evidence list and existing draft content; do not invent any citation, DOI, result, quote, statistic, or claim; "
            "if support is missing, write exactly Do not know.; keep the output conservative; preserve headings in Markdown.\n\n"
            "Evidence list:\n" + "\n".join(evidence_lines) + "\n\n"
            "Draft to improve:\n" + draft_body[:8000]
        )
        result = self.provider_router.generate("draft_rewrite", prompt)
        return result.text.strip() if result.success and result.text.strip() else ""

    def _build_memory_report(self, memory_hits, project_id: str) -> str:
        lines = ["# Memory Report", "", f"- Project: {project_id}", "", "## Retrieved Memory Facts", ""]
        if memory_hits:
            for hit in memory_hits:
                lines.append(
                    f"- `{hit.fact.fact_id}` {hit.fact.statement} | verification={hit.fact.verification_status} | freshness={hit.freshness} | reused_without_recheck={'Yes' if hit.reusable_without_recheck else 'No'}"
                )
        else:
            lines.append("- No reusable memory fact matched the current topic.")
        lines.extend(["", "## Auto-Proposed Memory Additions", "", "- None generated automatically in this version; proposals can be added from verified future runs."])
        return "\n".join(lines)
