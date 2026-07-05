from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


Stability = Literal["stable", "slow-changing", "time-sensitive", "expired"]
VerificationStatus = Literal[
    "verified",
    "partially verified",
    "unverified",
    "disputed",
    "rejected",
]
ClaimKind = Literal["fact", "interpretation", "speculation", "user_input", "proposal"]
SourceType = Literal["crossref", "arxiv", "openalex", "brain", "user", "project_file", "manual"]


@dataclass(slots=True)
class ProviderConfig:
    name: str
    provider_type: str
    base_url: str = ""
    model: str = ""
    api_key_env: str = ""
    enabled: bool = True
    paid: bool = False
    experimental: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SourceRecord:
    source_id: str
    title: str
    source_type: SourceType
    authors: list[str] = field(default_factory=list)
    year: str = ""
    venue: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    verification_status: str = "unverified"
    notes: str = ""
    used_in_output: bool = False
    citation_status: str = "unverified"
    provenance: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ClaimRecord:
    claim_id: str
    claim_text: str
    kind: ClaimKind
    source_support: list[str] = field(default_factory=list)
    memory_support: list[str] = field(default_factory=list)
    confidence: str = "low"
    agent: str = ""
    review_state: str = "pending"
    final_inclusion: bool = False
    verification_status: str = "unverified"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FactRecord:
    fact_id: str
    statement: str
    category: str
    source: str
    citation_metadata: str
    date_added: str
    last_verified: str
    stability: Stability
    verification_status: VerificationStatus
    confidence: Literal["high", "medium", "low"]
    added_by: str
    used_in_projects: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProjectIntake:
    topic: str
    scope: str
    discipline: str = ""
    target_venue: str = ""
    audience: str = ""
    word_count: str = ""
    citation_style: str = "APA 7"
    preferred_methodology: str = ""
    data_availability: str = "unknown"
    theoretical_framework: str = ""
    geographic_context: str = ""
    deadline: str = ""
    empirical_data_exists: str = "unknown"
    user_files_exist: bool = False
    online_search_allowed: bool = False
    paid_apis_allowed: bool = False
    browser_login_allowed: bool = False
    local_only_mode: bool = True
    tone: str = "conservative"
    gap_analysis_first: bool = True
    source_collection_mode: str = "broad"
    preferred_first_output: str = "research plan"
    extra_answers: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AgentRunRecord:
    agent_name: str
    role: str
    task: str
    provider_used: str
    input_summary: str
    output_summary: str
    warning: str = ""
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class WorkflowResult:
    project_id: str
    project_path: Path
    stage: str
    final_output_path: Path
    source_audit_path: Path
    claim_ledger_path: Path
    integrity_report_path: Path
    memory_report_path: Path
    selected_agents: list[str]
    provider_log: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["project_path"] = str(self.project_path)
        data["final_output_path"] = str(self.final_output_path)
        data["source_audit_path"] = str(self.source_audit_path)
        data["claim_ledger_path"] = str(self.claim_ledger_path)
        data["integrity_report_path"] = str(self.integrity_report_path)
        data["memory_report_path"] = str(self.memory_report_path)
        return data
