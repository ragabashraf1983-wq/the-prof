from __future__ import annotations

from datetime import datetime
from typing import Any

import requests

from .api_registry import APIRegistry


class APITester:
    def __init__(self, registry: APIRegistry) -> None:
        self.registry = registry

    def test_all(self) -> list[dict[str, Any]]:
        records = self.registry.load()
        for record in records:
            self._test_record(record)
        self.registry.save(records)
        return records

    def _test_record(self, record: dict[str, Any]) -> None:
        endpoint = record.get("endpoint", "")
        status = "not-tested"
        note = ""
        if not endpoint:
            status = "invalid"
            note = "Missing endpoint."
        elif record.get("auth_type") not in {"none", "optional-apiKey"}:
            status = "credentials-required"
            note = "Skipping live test because credentials are required."
        else:
            try:
                response = requests.get(endpoint, timeout=10)
                status = "ok" if response.status_code < 500 else f"http-{response.status_code}"
                note = f"HTTP {response.status_code}"
            except Exception as exc:
                status = "error"
                note = str(exc)
        record["last_test_status"] = status
        record["last_test_date"] = datetime.utcnow().date().isoformat()
        existing = record.get("notes", "")
        record["notes"] = f"{existing} | test: {note}".strip(" |")
