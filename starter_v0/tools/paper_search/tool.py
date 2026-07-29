from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

import requests

from tools._shared import TIMEOUT, err

_ATOM_NS = "{http://www.w3.org/2005/Atom}"


def _text(entry: ET.Element, tag: str) -> str:
    node = entry.find(f"{_ATOM_NS}{tag}")
    return (node.text or "").strip() if node is not None else ""


def _pdf_link(entry: ET.Element) -> str:
    for link in entry.findall(f"{_ATOM_NS}link"):
        if link.get("title") == "pdf":
            return link.get("href", "")
    return ""


def arxiv_paper_search(query: str = "", max_results: int = 5) -> dict[str, Any]:
    try:
        if not query:
            raise ValueError("query is required")
        response = requests.get(
            "http://export.arxiv.org/api/query",
            params={
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": int(max_results or 5),
                "sortBy": "relevance",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        root = ET.fromstring(response.text)
        items = []
        for entry in root.findall(f"{_ATOM_NS}entry"):
            authors = [
                _text(author, "name")
                for author in entry.findall(f"{_ATOM_NS}author")
            ]
            items.append({
                "title": " ".join(_text(entry, "title").split()),
                "url": _text(entry, "id"),
                "pdf_url": _pdf_link(entry),
                "authors": authors,
                "summary": " ".join(_text(entry, "summary").split()),
                "published": _text(entry, "published"),
            })
        return {"tool": "arxiv_paper_search", "query": query, "items": items}
    except Exception as exc:
        return err("arxiv_paper_search", exc)
