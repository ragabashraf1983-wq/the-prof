from __future__ import annotations

import re

import requests

from the_prof.core.models import SourceRecord

DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)


class CitationValidator:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TheProf/0.1"})

    def validate(self, source: SourceRecord, online_allowed: bool) -> tuple[str, str]:
        if source.source_type in {"arxiv", "openalex", "crossref"} and source.verification_status == "verified":
            return "verified", "Verified by source search API."
        if source.doi:
            if not DOI_RE.match(source.doi):
                return "suspicious", "DOI format is invalid."
            if online_allowed:
                try:
                    response = self.session.get(f"https://api.crossref.org/works/{source.doi}", timeout=15)
                    if response.status_code == 200:
                        return "verified", "Crossref confirmed DOI existence."
                    return "unverified", f"Crossref returned status {response.status_code}."
                except Exception as exc:
                    return "unverified", str(exc)
        if source.title:
            if len(source.title.split()) < 3:
                return "suspicious", "Title is too short for safe reference matching."
        return "unverified", "No strong verification path available."
