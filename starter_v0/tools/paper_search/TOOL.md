---
name: paper_search
track: team
kind: live_api
provider: arXiv Atom API (export.arxiv.org)
requires_env: []
inputs: [query, max_results]
outputs: [items]
side_effect: false
---
# paper_search

## Purpose

Search arXiv directly for scientific papers matching a query and return
title/authors/abstract/links (no API key needed).

## When to use

Use when the user asks for academic/research papers on a topic. Do not use for
general web results (use `web_search`) or news (use `lookup`).

## Arguments

| name | type | required |
|------|------|----------|
| query | string | yes |
| max_results | integer | no (default 5) |

## Output

- `items`: list of `{title, url, pdf_url, authors, summary, published}`
