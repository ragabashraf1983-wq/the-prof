from __future__ import annotations

import html
import re
import urllib.parse
import xml.etree.ElementTree as ET
from collections import OrderedDict

import requests

from the_prof.core.models import SourceRecord


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


class SourceSearch:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TheProf/0.1 (local-first academic desktop app)"})

    def search(self, topic: str, online_allowed: bool, max_results: int = 6) -> list[SourceRecord]:
        if not online_allowed:
            return []
        sources: list[SourceRecord] = []
        sources.extend(self.search_crossref(topic, max_results=max_results // 2 or 3))
        sources.extend(self.search_openalex(topic, max_results=max_results // 2 or 3))
        sources.extend(self.search_arxiv(topic, max_results=max_results // 2 or 3))
        deduped: OrderedDict[str, SourceRecord] = OrderedDict()
        for source in sources:
            key = source.doi.lower() if source.doi else source.title.lower()
            if key and key not in deduped:
                deduped[key] = source
        return list(deduped.values())[:max_results]

    def search_crossref(self, topic: str, max_results: int = 3) -> list[SourceRecord]:
        try:
            response = self.session.get(
                "https://api.crossref.org/works",
                params={"query.title": topic, "rows": max_results, "sort": "relevance"},
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        records = []
        for item in payload.get("message", {}).get("items", []):
            title = _clean_text((item.get("title") or [""])[0])
            authors = []
            for author in item.get("author", []):
                given = author.get("given", "").strip()
                family = author.get("family", "").strip()
                full = " ".join(part for part in [given, family] if part).strip()
                if full:
                    authors.append(full)
            year = ""
            published = item.get("issued", {}).get("date-parts", [[]])
            if published and published[0]:
                year = str(published[0][0])
            records.append(
                SourceRecord(
                    source_id=f"SRC-CR-{len(records)+1:04d}",
                    title=title or "Do not know.",
                    source_type="crossref",
                    authors=authors,
                    year=year,
                    venue=_clean_text((item.get("container-title") or [""])[0]),
                    doi=item.get("DOI", ""),
                    url=item.get("URL", ""),
                    abstract=_clean_text(item.get("abstract", "")),
                    verification_status="verified",
                    citation_status="verified",
                    provenance="Crossref API",
                    raw=item,
                )
            )
        return records

    def search_openalex(self, topic: str, max_results: int = 3) -> list[SourceRecord]:
        try:
            response = self.session.get(
                "https://api.openalex.org/works",
                params={"search": topic, "per-page": max_results},
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        records = []
        for item in payload.get("results", []):
            title = _clean_text(item.get("display_name", ""))
            authors = [auth.get("author", {}).get("display_name", "") for auth in item.get("authorships", []) if auth.get("author", {}).get("display_name")]
            doi = item.get("doi", "")
            if doi.startswith("https://doi.org/"):
                doi = doi.removeprefix("https://doi.org/")
            primary_location = item.get("primary_location") or {}
            source_meta = primary_location.get("source") or {}
            records.append(
                SourceRecord(
                    source_id=f"SRC-OA-{len(records)+1:04d}",
                    title=title or "Do not know.",
                    source_type="openalex",
                    authors=authors,
                    year=str(item.get("publication_year", "")),
                    venue=_clean_text(source_meta.get("display_name", "")),
                    doi=doi,
                    url=item.get("id", ""),
                    abstract="",
                    verification_status="verified",
                    citation_status="verified",
                    provenance="OpenAlex API",
                    raw=item,
                )
            )
        return records

    def search_arxiv(self, topic: str, max_results: int = 3) -> list[SourceRecord]:
        url = "https://export.arxiv.org/api/query"
        params = {"search_query": f"all:{topic}", "start": 0, "max_results": max_results}
        try:
            response = self.session.get(url, params=params, timeout=20)
            response.raise_for_status()
        except Exception:
            return []
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError:
            return []
        records = []
        for entry in root.findall("atom:entry", ns):
            title = _clean_text(entry.findtext("atom:title", default="", namespaces=ns))
            authors = [_clean_text(author.findtext("atom:name", default="", namespaces=ns)) for author in entry.findall("atom:author", ns)]
            published = entry.findtext("atom:published", default="", namespaces=ns)
            records.append(
                SourceRecord(
                    source_id=f"SRC-ARX-{len(records)+1:04d}",
                    title=title or "Do not know.",
                    source_type="arxiv",
                    authors=[a for a in authors if a],
                    year=published[:4],
                    venue="arXiv",
                    doi="",
                    url=entry.findtext("atom:id", default="", namespaces=ns),
                    abstract=_clean_text(entry.findtext("atom:summary", default="", namespaces=ns)),
                    verification_status="verified",
                    citation_status="verified",
                    provenance="arXiv API",
                    raw={"published": published},
                )
            )
        return records
