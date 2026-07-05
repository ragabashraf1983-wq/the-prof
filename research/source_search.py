from __future__ import annotations

import html
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from collections import OrderedDict
from typing import Any

import requests

from the_prof.core.models import SourceRecord


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def _abstract_from_openalex_index(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    words: list[tuple[int, str]] = []
    for word, positions in index.items():
        for pos in positions:
            words.append((pos, word))
    return _clean_text(" ".join(word for _, word in sorted(words)))


class SourceSearch:
    """Free academic source discovery.

    Uses no-key scholarly APIs first and optional-key APIs only when a user adds
    them later.  Returned records are metadata records, not proof that the paper
    supports a claim; downstream reports must cite them conservatively.
    """

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TheProf/0.2 (local academic research desktop app; polite free API use)"})

    def search(self, topic: str, online_allowed: bool, max_results: int = 24) -> list[SourceRecord]:
        if not online_allowed:
            return []
        searches = [
            ("Semantic Scholar", self.search_semantic_scholar, 8),
            ("OpenAlex", self.search_openalex, 8),
            ("Crossref", self.search_crossref, 6),
            ("PubMed", self.search_pubmed, 6),
            ("arXiv", self.search_arxiv, 6),
            ("OpenCitations", self.search_opencitations_metadata, 4),
        ]
        sources: list[SourceRecord] = []
        for _name, func, limit in searches:
            try:
                sources.extend(func(topic, max_results=limit))
                time.sleep(0.15)
            except Exception:
                continue
        return self._dedupe_rank(sources, max_results=max_results)

    def _dedupe_rank(self, sources: list[SourceRecord], max_results: int) -> list[SourceRecord]:
        deduped: OrderedDict[str, SourceRecord] = OrderedDict()
        for source in sources:
            key = source.doi.lower().strip() if source.doi else source.url.lower().strip() or source.title.lower().strip()
            if not key:
                continue
            if key in deduped:
                existing = deduped[key]
                if not existing.abstract and source.abstract:
                    existing.abstract = source.abstract
                if not existing.doi and source.doi:
                    existing.doi = source.doi
                if source.provenance and source.provenance not in existing.provenance:
                    existing.provenance += f" + {source.provenance}"
            else:
                deduped[key] = source
        def score(s: SourceRecord) -> tuple[int, int, int]:
            return (1 if s.doi else 0, 1 if s.abstract else 0, int(s.year or 0) if str(s.year).isdigit() else 0)
        return sorted(deduped.values(), key=score, reverse=True)[:max_results]

    def search_semantic_scholar(self, topic: str, max_results: int = 8) -> list[SourceRecord]:
        try:
            response = self.session.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={
                    "query": topic,
                    "limit": max_results,
                    "fields": "title,authors,year,venue,url,abstract,externalIds,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf",
                },
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        records = []
        for item in payload.get("data", []):
            external = item.get("externalIds") or {}
            doi = external.get("DOI", "")
            records.append(
                SourceRecord(
                    source_id=f"SRC-SS-{len(records)+1:04d}",
                    title=_clean_text(item.get("title", "")) or "Do not know.",
                    source_type="manual",
                    authors=[_clean_text(a.get("name", "")) for a in item.get("authors", []) if a.get("name")],
                    year=str(item.get("year", "") or ""),
                    venue=_clean_text(item.get("venue", "")),
                    doi=doi,
                    url=item.get("url", ""),
                    abstract=_clean_text(item.get("abstract", "")),
                    verification_status="verified",
                    citation_status="verified",
                    provenance="Semantic Scholar Graph API",
                    raw=item,
                )
            )
        return records

    def search_crossref(self, topic: str, max_results: int = 6) -> list[SourceRecord]:
        try:
            response = self.session.get(
                "https://api.crossref.org/works",
                params={"query.bibliographic": topic, "rows": max_results, "sort": "relevance"},
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
                full = " ".join(part for part in [author.get("given", "").strip(), author.get("family", "").strip()] if part).strip()
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
                    provenance="Crossref Works API",
                    raw=item,
                )
            )
        return records

    def search_openalex(self, topic: str, max_results: int = 8) -> list[SourceRecord]:
        try:
            response = self.session.get(
                "https://api.openalex.org/works",
                params={"search": topic, "per-page": max_results, "sort": "relevance_score:desc"},
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        records = []
        for item in payload.get("results", []):
            doi = item.get("doi", "") or ""
            if doi.startswith("https://doi.org/"):
                doi = doi.removeprefix("https://doi.org/")
            primary_location = item.get("primary_location") or {}
            source_meta = primary_location.get("source") or {}
            records.append(
                SourceRecord(
                    source_id=f"SRC-OA-{len(records)+1:04d}",
                    title=_clean_text(item.get("display_name", "")) or "Do not know.",
                    source_type="openalex",
                    authors=[auth.get("author", {}).get("display_name", "") for auth in item.get("authorships", []) if auth.get("author", {}).get("display_name")],
                    year=str(item.get("publication_year", "")),
                    venue=_clean_text(source_meta.get("display_name", "")),
                    doi=doi,
                    url=item.get("id", ""),
                    abstract=_abstract_from_openalex_index(item.get("abstract_inverted_index")),
                    verification_status="verified",
                    citation_status="verified",
                    provenance="OpenAlex Works API",
                    raw=item,
                )
            )
        return records

    def search_pubmed(self, topic: str, max_results: int = 6) -> list[SourceRecord]:
        try:
            search_response = self.session.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                params={"db": "pubmed", "term": topic, "retmode": "json", "retmax": max_results, "sort": "relevance"},
                timeout=20,
            )
            search_response.raise_for_status()
            ids = search_response.json().get("esearchresult", {}).get("idlist", [])
            if not ids:
                return []
            summary_response = self.session.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
                timeout=20,
            )
            summary_response.raise_for_status()
            payload = summary_response.json().get("result", {})
        except Exception:
            return []
        records = []
        for pmid in ids:
            item: dict[str, Any] = payload.get(pmid, {})
            authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
            pubdate = item.get("pubdate", "")
            records.append(
                SourceRecord(
                    source_id=f"SRC-PM-{len(records)+1:04d}",
                    title=_clean_text(item.get("title", "")) or "Do not know.",
                    source_type="manual",
                    authors=authors,
                    year=pubdate[:4] if pubdate else "",
                    venue=_clean_text(item.get("fulljournalname", "")),
                    doi="",
                    url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    abstract="",
                    verification_status="verified",
                    citation_status="verified",
                    provenance="PubMed E-utilities API",
                    raw=item,
                )
            )
        return records

    def search_arxiv(self, topic: str, max_results: int = 6) -> list[SourceRecord]:
        params = {"search_query": f"all:{topic}", "start": 0, "max_results": max_results, "sortBy": "relevance"}
        try:
            response = self.session.get("https://export.arxiv.org/api/query", params=params, timeout=20)
            response.raise_for_status()
            root = ET.fromstring(response.text)
        except Exception:
            return []
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        records = []
        for entry in root.findall("atom:entry", ns):
            published = entry.findtext("atom:published", default="", namespaces=ns)
            records.append(
                SourceRecord(
                    source_id=f"SRC-ARX-{len(records)+1:04d}",
                    title=_clean_text(entry.findtext("atom:title", default="", namespaces=ns)) or "Do not know.",
                    source_type="arxiv",
                    authors=[_clean_text(author.findtext("atom:name", default="", namespaces=ns)) for author in entry.findall("atom:author", ns)],
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

    def search_opencitations_metadata(self, topic: str, max_results: int = 4) -> list[SourceRecord]:
        # OpenCitations metadata works best by DOI, so first use Crossref DOIs.
        crossref = self.search_crossref(topic, max_results=max_results)
        records: list[SourceRecord] = []
        for source in crossref:
            if not source.doi:
                continue
            try:
                response = self.session.get(
                    f"https://opencitations.net/index/api/v2/metadata/{urllib.parse.quote(source.doi)}",
                    timeout=20,
                )
                if response.status_code != 200:
                    continue
                payload = response.json()
            except Exception:
                continue
            if payload:
                source.provenance += " + OpenCitations Metadata API"
                source.raw["opencitations"] = payload[0]
                records.append(source)
        return records
