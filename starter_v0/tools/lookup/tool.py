from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err


def web_search(query: str = "", topic: str = "general", timeframe: str | None = "week", max_results: int = 5) -> dict[str, Any]:
    try:
        key = os.getenv("TAVILY_API_KEY")
        if not key:
            raise RuntimeError("Missing TAVILY_API_KEY env var")
        
        valid_topics = ("general", "news")
        selected_topic = topic if topic in valid_topics else "general"
        
        body: dict[str, Any] = {
            "query": query,
            "topic": selected_topic,
            "max_results": int(max_results or 5),
            "search_depth": "basic"
        }
        
        valid_timeframes = ("day", "week", "month", "year", "d", "w", "m", "y")
        if timeframe and isinstance(timeframe, str) and timeframe.lower() in valid_timeframes:
            body["time_range"] = timeframe.lower()

        response = requests.post(
            "https://api.tavily.com/search",
            json=body,
            headers={"Authorization": f"Bearer {key}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        items = [{
            "title": item.get("title"),
            "url": item.get("url"),
            "source": domain(item.get("url", "")),
            "summary": item.get("content"),
            "score": item.get("score"),
        } for item in data.get("results", [])]
        return {"tool": "web_search", "query": query, "topic": selected_topic, "timeframe": timeframe, "items": items}
    except Exception as exc:
        # Fallback to DuckDuckGo if Tavily fails or raises an error
        try:
            from tools.web_search.tool import ddg_web_search
            fallback_res = ddg_web_search(query=query, max_results=max_results)
            if "items" in fallback_res:
                return {"tool": "web_search", "query": query, "topic": topic, "timeframe": timeframe, "items": fallback_res["items"], "fallback": "duckduckgo"}
        except Exception:
            pass
        return err("web_search", exc)


