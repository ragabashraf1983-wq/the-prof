from __future__ import annotations

from pathlib import Path

from the_prof.core.models import SourceRecord


class ReferenceMemory:
    def __init__(self, references_path: Path) -> None:
        self.references_path = references_path

    def add_reference_markdown(self, source: SourceRecord, project_id: str) -> None:
        entry = [
            f"% Project: {project_id}",
            f"% Verification: {source.verification_status}",
            f"@misc{{{source.source_id},",
            f"  title = {{{source.title}}},",
            f"  author = {{{' and '.join(source.authors)}}},",
            f"  year = {{{source.year}}},",
            f"  howpublished = {{{source.url or source.venue}}},",
            f"  note = {{{source.doi}}}",
            "}",
            "",
        ]
        with self.references_path.open("a", encoding="utf-8") as handle:
            handle.write("\n".join(entry))
