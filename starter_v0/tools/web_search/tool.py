from __future__ import annotations

import html
import re
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import requests

from tools._shared import TIMEOUT, domain, err

_RESULT_RE = re.compile(
    r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>.*?'
    r'<a class="result__snippet"[^>]*>(.*?)</a>',
    re.DOTALL,
)


def _clean(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _resolve_url(raw_url: str) -> str:
    if raw_url.startswith("//duckduckgo.com/l/"):
        raw_url = "https:" + raw_url
    parsed = urlparse(raw_url)
    if parsed.netloc.endswith("duckduckgo.com") and parsed.path == "/l/":
        target = parse_qs(parsed.query).get("uddg", [""])[0]
        return unquote(target)
    return raw_url


def ddg_web_search(query: str = "", max_results: int = 5) -> dict[str, Any]:
    try:
        if not query:
            raise ValueError("query is required")
        response = requests.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers={"User-Agent": "Mozilla/5.0 (AI20k-Day04-Research-Agent/1.0)"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        items = []
        for raw_url, raw_title, raw_snippet in _RESULT_RE.findall(response.text):
            url = _resolve_url(raw_url)
            items.append({
                "title": _clean(raw_title),
                "url": url,
                "source": domain(url),
                "summary": _clean(raw_snippet),
            })
            if len(items) >= int(max_results or 5):
                break
        return {"tool": "ddg_web_search", "query": query, "items": items}
    except Exception as exc:
        return err("ddg_web_search", exc)
