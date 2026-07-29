from __future__ import annotations

import re
from typing import Any

from tools._shared import err, terms

_PROPER_NOUN_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)?\b")


def _proper_nouns(text: str) -> list[str]:
    seen: list[str] = []
    for match in _PROPER_NOUN_RE.findall(text):
        if match not in seen:
            seen.append(match)
    return seen


def keyword_extract(text: str = "", max_keywords: int = 5) -> dict[str, Any]:
    try:
        if not text:
            raise ValueError("text is required")
        max_keywords = max(1, int(max_keywords or 5))

        freq: dict[str, int] = {}
        for term in terms(text):
            freq[term] = freq.get(term, 0) + 1
        ranked_terms = [t for t, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)]

        proper_nouns = _proper_nouns(text)

        keywords: list[str] = []
        for candidate in proper_nouns + ranked_terms:
            normalized = candidate.strip()
            if normalized and normalized.lower() not in [k.lower() for k in keywords]:
                keywords.append(normalized)
            if len(keywords) >= max_keywords:
                break

        return {"tool": "keyword_extract", "keywords": keywords}
    except Exception as exc:
        return err("keyword_extract", exc)
