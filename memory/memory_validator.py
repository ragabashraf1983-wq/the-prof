from __future__ import annotations

from datetime import datetime, timedelta, timezone

from the_prof.core.models import FactRecord


class MemoryValidator:
    def __init__(self, stable_days: int, slow_days: int, sensitive_days: int) -> None:
        self.thresholds = {
            "stable": stable_days,
            "slow-changing": slow_days,
            "time-sensitive": sensitive_days,
            "expired": 0,
        }

    def parse_date(self, value: str) -> datetime | None:
        if not value:
            return None
        try:
            if value.endswith("Z"):
                value = value[:-1] + "+00:00"
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def classify_freshness(self, fact: FactRecord) -> tuple[str, bool]:
        if fact.stability == "expired":
            return "expired", False
        last_verified = self.parse_date(fact.last_verified)
        if not last_verified:
            return "unknown", False
        if last_verified.tzinfo is None:
            last_verified = last_verified.replace(tzinfo=timezone.utc)
        age_days = (datetime.now(timezone.utc) - last_verified).days
        limit = self.thresholds.get(fact.stability, 30)
        reusable = age_days <= limit and fact.verification_status == "verified"
        if reusable:
            return "fresh", True
        return "stale", False
