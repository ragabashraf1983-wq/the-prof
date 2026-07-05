from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.db_dir = root / "storage" / "local_db"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.settings_path = self.db_dir / "settings.json"
        self.session_path = self.db_dir / "session.json"

    def read_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default

    def write_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_settings(self, default_settings: dict[str, Any]) -> dict[str, Any]:
        current = self.read_json(self.settings_path, {})
        merged = {**default_settings, **current}
        return merged

    def save_settings(self, settings: dict[str, Any]) -> None:
        self.write_json(self.settings_path, settings)

    def load_session(self) -> dict[str, Any]:
        return self.read_json(self.session_path, {"current_project_id": "", "current_project_path": ""})

    def save_session(self, session: dict[str, Any]) -> None:
        self.write_json(self.session_path, session)
