from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class APIRegistry:
    def __init__(self, seed_dir: Path, registry_path: Path) -> None:
        self.seed_dir = seed_dir
        self.registry_path = registry_path
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self.import_seeds()

    def import_seeds(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for seed_file in sorted(self.seed_dir.glob("*.json")):
            records.extend(json.loads(seed_file.read_text(encoding="utf-8")))
        self.save(records)
        return records

    def load(self) -> list[dict[str, Any]]:
        if not self.registry_path.exists():
            return self.import_seeds()
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def save(self, records: list[dict[str, Any]]) -> None:
        self.registry_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    def normalize(self) -> list[dict[str, Any]]:
        normalized = []
        for record in self.load():
            normalized.append(
                {
                    "name": record.get("name", "Unknown API"),
                    "category": record.get("category", "Unknown"),
                    "endpoint": record.get("endpoint", ""),
                    "auth_type": record.get("auth_type", "unknown"),
                    "pricing": record.get("pricing", "unknown"),
                    "rate_limit": record.get("rate_limit", "unknown"),
                    "supported_function": record.get("supported_function", "unknown"),
                    "last_test_status": record.get("last_test_status", "not-tested"),
                    "last_test_date": record.get("last_test_date", ""),
                    "risk_notes": record.get("risk_notes", ""),
                    "integration_status": record.get("integration_status", "seeded"),
                    "source_repository": record.get("source_repository", "unknown"),
                    "notes": record.get("notes", ""),
                    "enabled": record.get("enabled", False),
                }
            )
        self.save(normalized)
        return normalized
