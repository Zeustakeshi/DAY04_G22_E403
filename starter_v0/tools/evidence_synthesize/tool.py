from __future__ import annotations

from typing import Any
from tools._shared import domain, err

def synthesize_evidence(sources: list[dict[str, Any]] | None = None, max_items: int = 5) -> dict[str, Any]:
    """
    Hợp nhất và khử trùng lặp các nguồn thông tin nghiên cứu (web, paper, social),
    tạo ra bảng bằng chứng tinh gọn chuẩn hóa để truyền vào prompt/digest mà không bị lãng phí token.
    """
    try:
        if not sources:
            return {"tool": "evidence_synthesize", "synthesized_items": [], "total_input_items": 0, "deduped_count": 0}

        seen_urls = set()
        seen_titles = set()
        synthesized = []

        for item in sources:
            if not isinstance(item, dict):
                continue
            
            url = (item.get("url") or item.get("pdf_url") or "").strip()
            title = (item.get("title") or "").strip()
            summary = (item.get("summary") or item.get("content") or "").strip()
            source = item.get("source") or domain(url)

            # Deduplication key
            url_key = url.lower() if url else ""
            title_key = title.lower() if title else ""

            if url_key and url_key in seen_urls:
                continue
            if title_key and title_key in seen_titles:
                continue

            if url_key:
                seen_urls.add(url_key)
            if title_key:
                seen_titles.add(title_key)

            # Truncate overly long summary per item to preserve token budget
            short_summary = summary[:400] + "..." if len(summary) > 400 else summary

            synthesized.append({
                "title": title or "Untitled Resource",
                "url": url,
                "source": source or "Unknown Source",
                "summary": short_summary,
                "relevance_score": item.get("score") or item.get("relevance", 1.0)
            })

            if len(synthesized) >= int(max_items or 5):
                break

        return {
            "tool": "evidence_synthesize",
            "total_input_items": len(sources),
            "synthesized_count": len(synthesized),
            "deduped_count": len(sources) - len(synthesized),
            "items": synthesized
        }
    except Exception as exc:
        return err("evidence_synthesize", exc)
