from __future__ import annotations

import re
from collections import Counter

from the_prof.core.models import SourceRecord

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "using",
    "based",
    "study",
    "analysis",
    "review",
    "into",
    "toward",
    "through",
    "approach",
    "methods",
    "method",
}


class PriorArtAnalyzer:
    def extract_keywords(self, text: str) -> list[str]:
        tokens = [token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9\-]+", text)]
        return [token for token in tokens if token not in STOPWORDS and len(token) > 3]

    def theme_summary(self, sources: list[SourceRecord]) -> list[tuple[str, int]]:
        counter: Counter[str] = Counter()
        for source in sources:
            counter.update(self.extract_keywords(source.title))
        return counter.most_common(8)

    def year_range(self, sources: list[SourceRecord]) -> str:
        years = sorted({int(source.year) for source in sources if source.year.isdigit()})
        if not years:
            return "Do not know."
        if len(years) == 1:
            return str(years[0])
        return f"{years[0]}–{years[-1]}"
