---
title: "Long Context"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [context-window, attention, scaling]
summary: "Extending transformer context windows beyond training length — a systems and algorithms co-design challenge"
---

# Long Context

Extending context from 2K → 128K+ tokens requires solving problems at every level:

## Algorithm

- **[[concepts/rope]]** scaling — NTK-aware interpolation, YaRN
- **[[concepts/flash-attention]]** — makes long-context attention practical
- Sparse attention patterns for ultra-long contexts

## Systems

- **[[concepts/kv-cache]]** management — memory grows linearly with context
- [[concepts/inference-optimization]] — longer contexts = more compute per token

## Who's Leading

[[entities/anthropic]] (Claude 200K), [[entities/openai]] (GPT-4 128K), Google (Gemini 1M). The race is both algorithmic and infrastructural.

See also: [[concepts/attention-mechanism]], [[synthesis/serving-stack-2026]]
