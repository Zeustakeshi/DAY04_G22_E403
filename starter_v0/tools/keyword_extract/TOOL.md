---
name: keyword_extract
track: team
kind: algorithm
provider: local (frequency + proper-noun heuristic, no external API)
requires_env: []
inputs: [text, max_keywords]
outputs: [keywords]
side_effect: false
---
# keyword_extract

## Purpose

Extract important keywords from an article.

## When to use

Use when the user asks:

- key topics
- keywords
- important terms

## Arguments

- text (string, required)
- max_keywords (integer, optional, default 5)

## Output

- keywords: ordered list of strings (proper nouns like product/company names ranked
  first, then frequent terms)
