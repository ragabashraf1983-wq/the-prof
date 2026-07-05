from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProviderCatalog:
    def __init__(self, default_path: Path, storage_path: Path) -> None:
        self.default_path = default_path
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.reset_to_defaults()

    def load(self) -> list[dict[str, Any]]:
        try:
            return json.loads(self.storage_path.read_text(encoding="utf-8"))
        except Exception:
            return json.loads(self.default_path.read_text(encoding="utf-8"))

    def save(self, profiles: list[dict[str, Any]]) -> None:
        self.storage_path.write_text(json.dumps(profiles, indent=2, ensure_ascii=False), encoding="utf-8")

    def reset_to_defaults(self) -> None:
        self.storage_path.write_text(self.default_path.read_text(encoding="utf-8"), encoding="utf-8")

    def update_profile(self, name: str, updates: dict[str, Any]) -> None:
        profiles = self.load()
        for profile in profiles:
            if profile.get("name") == name:
                profile.update(updates)
                break
        self.save(profiles)
