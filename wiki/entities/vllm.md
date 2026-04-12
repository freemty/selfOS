---
title: "vLLM"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, serving, inference, pagedattention]
summary: "High-throughput LLM serving engine — PagedAttention for efficient KV cache management"
entity_type: "tool"
---

# vLLM

The most popular open-source LLM serving engine. Its key innovation, PagedAttention, manages [[concepts/kv-cache]] like an OS manages virtual memory — eliminating fragmentation and enabling efficient batching.

Core to the [[concepts/inference-optimization]] stack alongside [[concepts/flash-attention]], [[concepts/quantization]], and [[concepts/speculative-decoding]].

See also: [[entities/tensorrt-llm]], [[synthesis/serving-stack-2026]]
