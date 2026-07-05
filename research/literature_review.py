from __future__ import annotations

from the_prof.core.models import ClaimRecord, ProjectIntake, SourceRecord

from .prior_art import PriorArtAnalyzer


class LiteratureReviewBuilder:
    def __init__(self) -> None:
        self.analyzer = PriorArtAnalyzer()

    def build_review(self, intake: ProjectIntake, sources: list[SourceRecord], claims: list[ClaimRecord]) -> str:
        themes = self.analyzer.theme_summary(sources)
        lines = [
            f"# Literature Review — {intake.topic}",
            "",
            "## Search Strategy",
            "",
            f"- Topic query basis: {intake.topic}",
            f"- Online search enabled: {'Yes' if intake.online_search_allowed else 'No'}",
            f"- Source collection mode: {intake.source_collection_mode}",
            "",
            "## Evidence Summary",
            "",
            f"- Verified sources reviewed: {len(sources)}",
            f"- Dominant title themes: {', '.join(theme for theme, _ in themes[:5]) or 'Do not know.'}",
            "",
            "## Included Sources",
            "",
        ]
        if sources:
            for source in sources:
                lines.append(f"- **{source.title}** ({source.year or 'Do not know.'}) — {source.venue or source.source_type}")
        else:
            lines.append("- Do not know.")
        lines.extend(["", "## Thematic Synthesis", ""])
        if themes:
            for theme, count in themes[:5]:
                lines.append(f"- Theme `{theme}` appears across {count} retrieved title(s); deeper synthesis requires abstract/full-text review.")
        else:
            lines.append("- Do not know.")
        lines.extend(["", "## Research Gaps", "", "- Gap claims require stronger manual or automated evidence review than title-only retrieval can provide.", "- Current safe conclusion: additional targeted source screening is required before asserting field-wide gaps.", "", "## Traceable Claims", ""])
        if claims:
            for claim in claims[:10]:
                lines.append(f"- `{claim.claim_id}` {claim.claim_text}")
        else:
            lines.append("- No claim ledger entries available.")
        lines.extend(["", "## Integrity Note", "", "- Unsupported synthesis claims have been avoided and replaced with `Do not know.` where needed."])
        return "\n".join(lines)

    def build_proposal(self, intake: ProjectIntake, sources: list[SourceRecord], claims: list[ClaimRecord]) -> str:
        themes = self.analyzer.theme_summary(sources)
        lines = [
            f"# Research Proposal — {intake.topic}",
            "",
            "## Working Title",
            "",
            f"- {intake.topic}: A conservative proposal for further academic investigation",
            "",
            "## Background",
            "",
        ]
        if sources:
            lines.append(f"- The current evidence set contains {len(sources)} verified source record(s) relevant to the topic query.")
            if themes:
                lines.append(f"- Common title-level themes include: {', '.join(theme for theme, _ in themes[:5])}.")
        else:
            lines.append("- Do not know.")
        lines.extend(["", "## Problem Statement", "", f"- The user is seeking a {intake.scope.lower()} on the topic '{intake.topic}'.", "- A validated field-wide problem statement requires stronger evidence review than the current run may provide.", "", "## Research Gap", "", "- Safe claim: additional targeted review is needed to distinguish saturated areas from underexplored ones.", "- If stronger evidence is required, rerun with online search enabled and/or user-provided literature files.", "", "## Aims and Objectives", "", "- Map the current evidence base relevant to the topic.", "- Identify methodological or contextual weaknesses in existing work.", "- Propose a bounded study design appropriate to the user’s constraints.", "", "## Research Questions", "", f"- What is currently known about {intake.topic}?", "- Which methods, datasets, populations, or contexts appear most emphasized?", "- Which unresolved or weakly supported directions merit follow-up study?", "", "## Proposed Methodology", "", f"- Preferred methodology from intake: {intake.preferred_methodology or 'Do not know.'}", "- Proposed design should remain conservative until the literature base is expanded and audited.", "- If empirical data exist, results must be written only from actual data, not projections.", "", "## Ethics", "", "- Review privacy, bias, copyright, and data-permission risks before collecting or uploading external material.", "", "## Expected Contribution", "", "- A traceable, audit-backed research plan with explicit uncertainty markers.", "", "## Risks and Limitations", "", "- Limited source retrieval reduces confidence in novelty claims.", "- Unsupported claims must remain as `Do not know.` until verified.", "", "## Traceable Claims", ""])
        if claims:
            for claim in claims[:10]:
                lines.append(f"- `{claim.claim_id}` {claim.claim_text}")
        else:
            lines.append("- No claim ledger entries available.")
        lines.extend(["", "## Integrity Note", "", "- This proposal intentionally avoids unverified novelty claims."])
        return "\n".join(lines)
