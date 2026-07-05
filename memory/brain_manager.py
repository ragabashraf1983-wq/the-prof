from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Iterable

from the_prof.core.models import FactRecord, utc_now_iso

from .memory_validator import MemoryValidator

FACT_HEADER_RE = re.compile(r"^## Fact ID: (?P<fact_id>FACT-\d{6})$", re.MULTILINE)
FIELD_RE = re.compile(r"^- (?P<key>[A-Za-z ]+):\s*(?P<value>.*)$")


class BrainManager:
    def __init__(self, root: Path, stable_days: int = 180, slow_days: int = 60, sensitive_days: int = 14) -> None:
        self.root = root
        self.brain_dir = root / "brain"
        self.brain_path = self.brain_dir / "brain.md"
        self.index_path = self.brain_dir / "brain_index.json"
        self.references_path = self.brain_dir / "references.bib"
        self.reference_notes_path = self.brain_dir / "reference_notes.md"
        self.memory_log_path = self.brain_dir / "memory_log.md"
        self.pending_path = self.brain_dir / "pending_verification.md"
        self.rejected_path = self.brain_dir / "rejected_claims.md"
        self.backup_dir = self.brain_dir / "backups"
        self.validator = MemoryValidator(stable_days, slow_days, sensitive_days)
        self.initialize()

    def initialize(self) -> None:
        self.brain_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        if not self.brain_path.exists():
            self.brain_path.write_text(
                "# brain.md\n\nPortable verified research memory for The Prof.\n\n",
                encoding="utf-8",
            )
        if not self.index_path.exists():
            self.index_path.write_text("[]\n", encoding="utf-8")
        if not self.references_path.exists():
            self.references_path.write_text("% Verified reference memory\n", encoding="utf-8")
        for path, title in [
            (self.reference_notes_path, "# Reference Notes\n\n"),
            (self.memory_log_path, "# Memory Log\n\n"),
            (self.pending_path, "# Pending Verification\n\n"),
            (self.rejected_path, "# Rejected Claims\n\n"),
        ]:
            if not path.exists():
                path.write_text(title, encoding="utf-8")
        self.rebuild_index()

    def _next_fact_id(self) -> str:
        facts = self.load_facts()
        max_num = 0
        for fact in facts:
            try:
                max_num = max(max_num, int(fact.fact_id.split("-")[1]))
            except Exception:
                continue
        return f"FACT-{max_num + 1:06d}"

    def backup(self) -> Path:
        backup_path = self.backup_dir / f"brain_{utc_now_iso().replace(':', '').replace('-', '')}.md"
        shutil.copy2(self.brain_path, backup_path)
        return backup_path

    def load_facts(self) -> list[FactRecord]:
        text = self.brain_path.read_text(encoding="utf-8")
        headers = list(FACT_HEADER_RE.finditer(text))
        facts: list[FactRecord] = []
        for idx, match in enumerate(headers):
            start = match.start()
            end = headers[idx + 1].start() if idx + 1 < len(headers) else len(text)
            block = text[start:end].strip()
            lines = block.splitlines()
            data: dict[str, str] = {"fact_id": match.group("fact_id")}
            current_key = ""
            for line in lines[1:]:
                field_match = FIELD_RE.match(line.strip())
                if field_match:
                    current_key = field_match.group("key").strip().lower().replace(" ", "_")
                    data[current_key] = field_match.group("value").strip()
                elif current_key and line.startswith("  -"):
                    existing = data.get(current_key, "")
                    addition = line.replace("  -", "", 1).strip()
                    data[current_key] = (existing + (" | " if existing else "") + addition).strip()
            facts.append(
                FactRecord(
                    fact_id=data.get("fact_id") or "FACT-000000",
                    statement=data.get("statement", ""),
                    category=data.get("category", ""),
                    source=data.get("source", ""),
                    citation_metadata=data.get("citation_metadata", ""),
                    date_added=data.get("date_added", ""),
                    last_verified=data.get("last_verified", ""),
                    stability=data.get("stability", "stable") or "stable",
                    verification_status=data.get("verification_status", "unverified") or "unverified",
                    confidence=data.get("confidence", "low") or "low",
                    added_by=data.get("added_by", "unknown"),
                    used_in_projects=[item.strip() for item in data.get("used_in_projects", "").split("|") if item.strip()],
                    notes=data.get("notes", ""),
                )
            )
        return facts

    def _fact_to_markdown(self, fact: FactRecord) -> str:
        used_in = ", ".join(fact.used_in_projects) if fact.used_in_projects else ""
        return "\n".join(
            [
                f"## Fact ID: {fact.fact_id}",
                "",
                f"- Statement: {fact.statement}",
                f"- Category: {fact.category}",
                f"- Source: {fact.source}",
                f"- Citation metadata: {fact.citation_metadata}",
                f"- Date added: {fact.date_added}",
                f"- Last verified: {fact.last_verified}",
                f"- Stability: {fact.stability}",
                f"- Verification status: {fact.verification_status}",
                f"- Confidence: {fact.confidence}",
                f"- Added by: {fact.added_by}",
                f"- Used in projects: {used_in}",
                f"- Notes: {fact.notes}",
                "",
            ]
        )

    def save_facts(self, facts: Iterable[FactRecord]) -> None:
        facts_list = list(facts)
        self.backup()
        content = ["# brain.md", "", "Portable verified research memory for The Prof.", ""]
        for fact in facts_list:
            content.append(self._fact_to_markdown(fact))
        self.brain_path.write_text("\n".join(content), encoding="utf-8")
        self.rebuild_index()
        self.log(f"Saved {len(facts_list)} fact records.")

    def rebuild_index(self) -> None:
        facts = self.load_facts()
        index = []
        for fact in facts:
            freshness, reusable = self.validator.classify_freshness(fact)
            index.append(
                {
                    "fact_id": fact.fact_id,
                    "statement": fact.statement,
                    "category": fact.category,
                    "verification_status": fact.verification_status,
                    "stability": fact.stability,
                    "freshness": freshness,
                    "reusable_without_recheck": reusable,
                }
            )
        self.index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    def search(self, query: str) -> list[FactRecord]:
        terms = [term.strip().lower() for term in query.split() if term.strip()]
        results = []
        for fact in self.load_facts():
            haystack = " ".join([fact.statement, fact.category, fact.notes, fact.source]).lower()
            if all(term in haystack for term in terms):
                results.append(fact)
        return results

    def propose_fact(self, statement: str, category: str, source: str, notes: str, added_by: str) -> FactRecord:
        fact = FactRecord(
            fact_id=self._next_fact_id(),
            statement=statement,
            category=category,
            source=source,
            citation_metadata="",
            date_added=utc_now_iso(),
            last_verified="",
            stability="time-sensitive",
            verification_status="unverified",
            confidence="low",
            added_by=added_by,
            notes=notes,
        )
        with self.pending_path.open("a", encoding="utf-8") as handle:
            handle.write(self._fact_to_markdown(fact) + "\n")
        self.log(f"Proposed fact {fact.fact_id}: {statement}")
        return fact

    def add_verified_fact(self, statement: str, category: str, source: str, citation_metadata: str, stability: str, added_by: str, notes: str = "") -> FactRecord:
        facts = self.load_facts()
        fact = FactRecord(
            fact_id=self._next_fact_id(),
            statement=statement,
            category=category,
            source=source,
            citation_metadata=citation_metadata,
            date_added=utc_now_iso(),
            last_verified=utc_now_iso(),
            stability=stability,
            verification_status="verified",
            confidence="high",
            added_by=added_by,
            notes=notes,
        )
        facts.append(fact)
        self.save_facts(facts)
        return fact

    def reject_fact(self, fact_markdown: str, reason: str) -> None:
        with self.rejected_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{fact_markdown}\n- Rejection reason: {reason}\n\n")
        self.log(f"Rejected fact proposal: {reason}")

    def export_brain(self, export_path: Path) -> None:
        export_path.write_text(self.brain_path.read_text(encoding="utf-8"), encoding="utf-8")
        self.log(f"Exported brain.md to {export_path}")

    def import_brain(self, import_path: Path) -> dict[str, int]:
        text = import_path.read_text(encoding="utf-8")
        imported_headers = FACT_HEADER_RE.findall(text)
        current_ids = {fact.fact_id for fact in self.load_facts()}
        duplicates = len([fid for fid in imported_headers if fid in current_ids])
        with self.pending_path.open("a", encoding="utf-8") as handle:
            handle.write("\n# Imported Brain Facts (marked pending)\n\n")
            handle.write(text)
            handle.write("\n")
        report = {"imported_fact_blocks": len(imported_headers), "duplicate_ids": duplicates}
        self.log(f"Imported external brain file from {import_path} with report {report}")
        return report

    def log(self, message: str) -> None:
        with self.memory_log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"- [{utc_now_iso()}] {message}\n")
