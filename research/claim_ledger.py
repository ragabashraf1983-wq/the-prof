from __future__ import annotations

from pathlib import Path
from typing import Iterable

from the_prof.core.models import ClaimRecord


class ClaimLedger:
    def __init__(self) -> None:
        self._counter = 0

    def next_id(self) -> str:
        self._counter += 1
        return f"CLAIM-{self._counter:04d}"

    def new_claim(
        self,
        claim_text: str,
        kind: str,
        source_support: list[str],
        memory_support: list[str],
        confidence: str,
        agent: str,
        verification_status: str,
        notes: str = "",
        final_inclusion: bool = True,
    ) -> ClaimRecord:
        return ClaimRecord(
            claim_id=self.next_id(),
            claim_text=claim_text,
            kind=kind,
            source_support=source_support,
            memory_support=memory_support,
            confidence=confidence,
            agent=agent,
            review_state="reviewed",
            final_inclusion=final_inclusion,
            verification_status=verification_status,
            notes=notes,
        )

    def write_markdown(self, path: Path, claims: Iterable[ClaimRecord]) -> None:
        lines = ["# Claim Ledger", ""]
        for claim in claims:
            lines.extend(
                [
                    f"## {claim.claim_id}",
                    "",
                    f"- **Claim:** {claim.claim_text}",
                    f"- **Kind:** {claim.kind}",
                    f"- **Source support:** {', '.join(claim.source_support) or 'None'}",
                    f"- **Memory support:** {', '.join(claim.memory_support) or 'None'}",
                    f"- **Confidence:** {claim.confidence}",
                    f"- **Agent:** {claim.agent}",
                    f"- **Review state:** {claim.review_state}",
                    f"- **Final inclusion:** {'Yes' if claim.final_inclusion else 'No'}",
                    f"- **Verification status:** {claim.verification_status}",
                    f"- **Notes:** {claim.notes or 'None'}",
                    "",
                ]
            )
        path.write_text("\n".join(lines), encoding="utf-8")
