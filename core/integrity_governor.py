from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import ClaimRecord, SourceRecord


@dataclass(slots=True)
class IntegrityIssue:
    severity: str
    message: str
    claim_id: str = ""


class IntegrityGovernor:
    """Applies global anti-hallucination rules before final output."""

    def validate_claims(self, claims: Iterable[ClaimRecord], sources: dict[str, SourceRecord]) -> list[IntegrityIssue]:
        issues: list[IntegrityIssue] = []
        for claim in claims:
            if claim.kind == "fact":
                if not claim.source_support and not claim.memory_support:
                    issues.append(IntegrityIssue("high", "Fact claim has no traceable support.", claim.claim_id))
                for source_id in claim.source_support:
                    source = sources.get(source_id)
                    if not source:
                        issues.append(IntegrityIssue("high", f"Claim references missing source {source_id}.", claim.claim_id))
                    elif source.verification_status not in {"verified", "partially verified"}:
                        issues.append(IntegrityIssue("medium", f"Claim references unverified source {source_id}.", claim.claim_id))
            if claim.verification_status == "hallucinated":
                issues.append(IntegrityIssue("high", "Hallucinated claim detected.", claim.claim_id))
        return issues

    def build_integrity_report(self, claims: Iterable[ClaimRecord], sources: dict[str, SourceRecord]) -> str:
        issues = self.validate_claims(claims, sources)
        lines = [
            "# Integrity Report",
            "",
            "## Global Rules",
            "",
            "- Verified facts only.",
            "- Unsupported claims must be marked `Do not know.`.",
            "- Facts, interpretation, and speculation must remain separate.",
            "- No fabricated citations, methods, results, or datasets.",
            "",
            "## Findings",
            "",
        ]
        if not issues:
            lines.append("- No blocking integrity issues were detected in the current artifact set.")
        else:
            for issue in issues:
                lines.append(f"- **{issue.severity.upper()}** `{issue.claim_id or 'global'}` — {issue.message}")
        lines.extend(
            [
                "",
                "## Enforcement Outcome",
                "",
                "- Any unsupported major claim must be removed or rewritten as `Do not know.` before release.",
            ]
        )
        return "\n".join(lines)
