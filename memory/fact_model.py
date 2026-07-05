from __future__ import annotations

from dataclasses import dataclass

from the_prof.core.models import FactRecord


@dataclass(slots=True)
class BrainSearchResult:
    fact: FactRecord
    freshness: str
    reusable_without_recheck: bool
