from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from the_prof.core.models import utc_now_iso


@dataclass(slots=True)
class ProviderUsageRecord:
    timestamp: str
    provider_name: str
    model: str
    task: str
    success: bool
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProviderUsageTracker:
    def __init__(self) -> None:
        self.records: list[ProviderUsageRecord] = []
        self.fallback_events: int = 0

    def record(self, provider_name: str, model: str, task: str, success: bool, error: str = "") -> None:
        self.records.append(
            ProviderUsageRecord(
                timestamp=utc_now_iso(),
                provider_name=provider_name,
                model=model,
                task=task,
                success=success,
                error=error,
            )
        )

    def mark_fallback(self) -> None:
        self.fallback_events += 1

    def summary(self) -> list[dict[str, Any]]:
        return [record.to_dict() for record in self.records]
