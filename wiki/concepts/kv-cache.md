---
title: "KV Cache"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [inference, memory, attention, serving]
summary: "Caching key-value pairs across autoregressive decoding steps to avoid redundant computation"
---

# KV Cache

During [[concepts/autoregressive-generation]], each new token attends to all previous tokens. Without caching, this means recomputing all key-value pairs at every step — O(N²) total work for N tokens.

The KV cache stores computed key-value pairs, reducing each step to O(N) — a massive speedup.

## The Memory Problem

KV cache memory grows linearly with sequence length and batch size. For long-context models ([[concepts/long-context]]), it can dominate GPU memory.

## PagedAttention

[[entities/vllm]] introduced PagedAttention: manage KV cache like virtual memory with pages. This eliminates fragmentation and enables efficient memory sharing across requests.

## Connection to System Design

KV cache management is where [[concepts/attention-mechanism]] meets operating systems. The abstraction of paged memory, originally from OS design, turns out to be exactly right for LLM serving.

See also: [[concepts/inference-optimization]], [[concepts/flash-attention]], [[synthesis/serving-stack-2026]]
