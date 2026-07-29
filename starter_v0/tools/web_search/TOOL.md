---
name: web_search
track: team
kind: live_api
provider: DuckDuckGo HTML (no API key)
requires_env: []
inputs: [query, max_results]
outputs: [items]
side_effect: false
---
# web_search

## Purpose

Search the open web for a query and return a list of results (title, url, snippet).

## When to use

Use when the user asks to search/find information on the web and no specific URL is
given yet. Do not use for a URL the user already provided (use `fetch` instead), and
do not use for scientific papers (use `paper_search`).

## Arguments

| name | type | required |
|------|------|----------|
| query | string | yes |
| max_results | integer | no (default 5) |

## Output

- `items`: list of `{title, url, source, summary}`
