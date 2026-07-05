from __future__ import annotations

from pathlib import Path

from the_prof.core.models import SourceRecord


class SourceAudit:
    def write_registry(self, path: Path, sources: list[SourceRecord]) -> None:
        lines = ["# Source Registry", ""]
        if not sources:
            lines.append("- No external sources were collected for this project.")
        for source in sources:
            lines.extend(
                [
                    f"## {source.source_id}",
                    "",
                    f"- **Title:** {source.title}",
                    f"- **Type:** {source.source_type}",
                    f"- **Authors:** {', '.join(source.authors) or 'Do not know.'}",
                    f"- **Year:** {source.year or 'Do not know.'}",
                    f"- **Venue:** {source.venue or 'Do not know.'}",
                    f"- **DOI:** {source.doi or 'Do not know.'}",
                    f"- **URL/Path:** {source.url or 'Do not know.'}",
                    f"- **Verification state:** {source.verification_status}",
                    f"- **Used in output:** {'Yes' if source.used_in_output else 'No'}",
                    f"- **Citation status:** {source.citation_status}",
                    f"- **Notes:** {source.notes or 'None'}",
                    f"- **Provenance:** {source.provenance or 'Do not know.'}",
                    "",
                ]
            )
        path.write_text("\n".join(lines), encoding="utf-8")

    def write_final_audit(self, path: Path, sources: list[SourceRecord]) -> None:
        lines = ["# Source Audit", "", "## Summary", ""]
        if not sources:
            lines.append("- No verified external source was available. Output was restricted to user input, project data, and explicit `Do not know.` markers.")
        else:
            verified = sum(1 for source in sources if source.verification_status == "verified")
            lines.append(f"- Total sources considered: {len(sources)}")
            lines.append(f"- Verified sources: {verified}")
            lines.append(f"- Sources used in final output: {sum(1 for source in sources if source.used_in_output)}")
        lines.extend(["", "## Detailed Records", ""])
        for source in sources:
            lines.append(f"- `{source.source_id}` {source.title} — {source.verification_status} — {source.url or source.doi or 'Do not know.'}")
        path.write_text("\n".join(lines), encoding="utf-8")
