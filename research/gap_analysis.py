from __future__ import annotations

from the_prof.core.models import ClaimRecord, ProjectIntake, SourceRecord

from .prior_art import PriorArtAnalyzer


class GapAnalysisBuilder:
    def __init__(self) -> None:
        self.analyzer = PriorArtAnalyzer()

    def build(
        self,
        intake: ProjectIntake,
        sources: list[SourceRecord],
        claims: list[ClaimRecord],
        memory_lines: list[str],
    ) -> str:
        themes = self.analyzer.theme_summary(sources)
        year_range = self.analyzer.year_range(sources)
        lines = [
            f"# Gap Analysis — {intake.topic}",
            "",
            "## Scope",
            "",
            f"- **Requested scope:** {intake.scope}",
            f"- **Discipline:** {intake.discipline or 'Do not know.'}",
            f"- **Research tone:** {intake.tone}",
            "",
            "## Evidence Base",
            "",
            f"- Verified external sources collected: {len(sources)}",
            f"- Approximate publication year span: {year_range}",
        ]
        if not sources:
            lines.append("- Evidence limitation: no verified external sources were collected in the current run.")
        lines.extend(["", "## Reused Brain Memory", ""])
        if memory_lines:
            lines.extend(memory_lines)
        else:
            lines.append("- No reusable verified brain facts were found for this topic.")
        lines.extend(["", "## Dominant Themes In Retrieved Source Titles", ""])
        if themes:
            for theme, count in themes:
                lines.append(f"- `{theme}` appears in {count} retrieved title(s).")
        else:
            lines.append("- Do not know.")
        lines.extend(["", "## Saturation Signals", ""])
        if len(sources) >= 4 and themes:
            lines.append("- Repeated title-level themes suggest at least some established literature concentration around the most common keywords above.")
            lines.append("- This is a title-level signal only; full-text saturation cannot be claimed from the current evidence set.")
        else:
            lines.append("- Do not know.")
        lines.extend(["", "## Candidate Gaps (Interpretive, Not Verified Facts)", ""])
        if themes:
            top_terms = ", ".join(theme for theme, _ in themes[:3])
            lines.append(f"- Potential gap candidate: compare dominant themes ({top_terms}) against underrepresented populations, regions, datasets, or evaluation settings in a deeper manual review.")
            lines.append("- Potential gap candidate: examine whether reproducibility, benchmark comparability, or methodological transparency are weak in the retrieved set.")
            lines.append("- Potential gap candidate: test whether adjacent disciplines use transferable methods that are not yet visible in the current topic query results.")
        else:
            lines.append("- Do not know.")
        lines.extend(["", "## Ranked Opportunity Hypotheses", ""])
        lines.append("1. Conservative opportunity: produce a structured literature map and audit unresolved methodological or reporting inconsistencies.")
        lines.append("2. Exploratory opportunity: evaluate whether overlooked contexts, populations, or datasets are weakly represented in the current evidence base.")
        lines.append("3. Ambitious opportunity: combine methods from neighboring domains only after a fresh source review confirms they are genuinely underexplored here.")
        lines.extend(["", "## Candidate Research Questions", ""])
        lines.append(f"- How is the topic '{intake.topic}' currently framed across the retrieved evidence base?")
        lines.append("- Which methodological choices are common, and which evaluation choices appear absent or weakly justified?")
        lines.append("- Which context-specific, temporal, or population-specific conditions appear insufficiently addressed?")
        lines.extend(["", "## Claim Traceability Snapshot", ""])
        if claims:
            for claim in claims[:8]:
                lines.append(f"- `{claim.claim_id}` {claim.claim_text} (sources: {', '.join(claim.source_support) or 'None'})")
        else:
            lines.append("- No claim records were generated.")
        lines.extend(["", "## Integrity Note", "", "- Any unsupported claim in this report has been avoided or marked as `Do not know.`", ""])
        return "\n".join(lines)
