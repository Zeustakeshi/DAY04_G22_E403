from __future__ import annotations

import re
from typing import Any
from tools._shared import fold_text, terms, err

def compress_text(text: str = "", focus_query: str = "", max_chars: int = 1500) -> dict[str, Any]:
    """
    Nén văn bản thông minh bằng cách lọc các câu/đoạn có chứa từ khóa liên quan đến focus_query,
    loại bỏ các câu rác và giới hạn kích thước tối đa để tiết kiệm token context window.
    """
    try:
        if not text:
            return {"tool": "smart_compress", "compressed_text": "", "original_chars": 0, "compressed_chars": 0, "token_savings_pct": 0.0}
        
        original_chars = len(text)
        
        # Split text into sentences / paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n+|\.\s+', text) if p.strip()]
        
        if focus_query:
            query_terms = terms(focus_query)
            scored_paragraphs = []
            for p in paragraphs:
                p_terms = terms(p)
                overlap = len(query_terms.intersection(p_terms))
                scored_paragraphs.append((overlap, len(p), p))
            
            # Sort by keyword overlap score descending
            scored_paragraphs.sort(key=lambda x: (x[0], -x[1]), reverse=True)
            selected = [p[2] for p in scored_paragraphs if p[0] > 0]
            if not selected:
                selected = paragraphs[:5]
        else:
            selected = paragraphs

        # Reconstruct compressed text up to max_chars
        compressed_chunks = []
        current_len = 0
        for chunk in selected:
            if current_len + len(chunk) + 2 > max_chars:
                break
            compressed_chunks.append(chunk)
            current_len += len(chunk) + 2

        compressed_text = ". ".join(compressed_chunks)
        compressed_chars = len(compressed_text)
        
        savings = round((1.0 - (compressed_chars / max(1, original_chars))) * 100, 1)

        return {
            "tool": "smart_compress",
            "compressed_text": compressed_text,
            "original_chars": original_chars,
            "compressed_chars": compressed_chars,
            "token_savings_pct": max(0.0, savings),
            "focus_query": focus_query
        }
    except Exception as exc:
        return err("smart_compress", exc)
