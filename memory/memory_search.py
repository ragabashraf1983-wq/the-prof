from __future__ import annotations

from .brain_manager import BrainManager
from .fact_model import BrainSearchResult


class MemorySearch:
    def __init__(self, brain_manager: BrainManager) -> None:
        self.brain_manager = brain_manager

    def search(self, query: str) -> list[BrainSearchResult]:
        results = []
        for fact in self.brain_manager.search(query):
            freshness, reusable = self.brain_manager.validator.classify_freshness(fact)
            results.append(BrainSearchResult(fact=fact, freshness=freshness, reusable_without_recheck=reusable))
        return results
