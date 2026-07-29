from __future__ import annotations

import re
from typing import Any

from tools._shared import err, terms


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?…])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def summarize_text(text: str = "", max_sentences: int = 3) -> dict[str, Any]:
    try:
        if not text:
            raise ValueError("text is required")
        max_sentences = max(1, int(max_sentences or 3))
        sentences = _sentences(text)
        if not sentences:
            raise ValueError("text has no sentences to summarize")
        if len(sentences) <= max_sentences:
            top_indices = list(range(len(sentences)))
        else:
            freq: dict[str, int] = {}
            for term in terms(text):
                freq[term] = freq.get(term, 0) + 1
            top_indices = sorted(
                sorted(
                    range(len(sentences)),
                    key=lambda i: sum(freq.get(t, 0) for t in terms(sentences[i])),
                    reverse=True,
                )[:max_sentences]
            )
        key_points = [sentences[i] for i in top_indices]
        return {
            "tool": "summarize_text",
            "summary": " ".join(key_points),
            "key_points": key_points,
            "sentence_count": len(sentences),
        }
    except Exception as exc:
        return err("summarize_text", exc)
