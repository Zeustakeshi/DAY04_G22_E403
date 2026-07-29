---
name: summarize
track: team
kind: algorithm
provider: local (extractive, no external API)
requires_env: []
inputs: [text, max_sentences]
outputs: [summary, key_points]
side_effect: false
---
# summarize

## Purpose

Summarize long articles or documents into concise key points.

## When to use

Use after `fetch` or when the user provides long text.

## Arguments

| name | type | required |
|------|------|----------|
| text | string | yes |
| max_sentences | integer | no (default 3) |

## Output

- Summary
- Key points
