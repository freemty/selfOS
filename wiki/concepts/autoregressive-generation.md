---
title: "Autoregressive Generation"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [inference, generation, next-token]
summary: "Generating text token by token, conditioned on all previous tokens"
---

# Autoregressive Generation

LLMs generate text one token at a time. Each token is sampled from P(x_t | x_1, ..., x_{t-1}), making generation inherently sequential.

## The Bottleneck

Sequential generation means latency scales linearly with output length. Key optimizations:
- **[[concepts/kv-cache]]** — avoid recomputing attention for past tokens
- **[[concepts/speculative-decoding]]** — parallelize via draft-verify
- **Efficient sampling** — top-k, top-p, temperature

See also: [[concepts/transformer-architecture]], [[concepts/inference-optimization]]
