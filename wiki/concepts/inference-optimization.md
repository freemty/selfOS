---
title: "Inference Optimization"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [serving, throughput, latency, optimization]
summary: "Techniques to make LLM serving faster and cheaper — from kernel-level to system-level optimizations"
---

# Inference Optimization

Serving LLMs at scale is a systems problem. A single GPT-4 query can cost cents — at millions of queries per day, optimization is existential.

## The Stack

From bottom to top:
1. **Hardware**: [[concepts/gpu-memory-hierarchy]], HBM bandwidth, interconnect
2. **Kernels**: [[concepts/flash-attention]], [[concepts/kernel-fusion]]
3. **Runtime**: [[concepts/kv-cache]] management, continuous batching
4. **Algorithm**: [[concepts/speculative-decoding]], [[concepts/quantization]]
5. **System**: [[entities/vllm]], [[entities/tensorrt-llm]]

## Key Techniques

- **[[concepts/kv-cache]]** + PagedAttention ([[entities/vllm]]) — avoid recomputation, manage memory like an OS
- **[[concepts/quantization]]** — INT8/INT4 weights, less memory, faster matmuls
- **[[concepts/speculative-decoding]]** — small model drafts, large model verifies
- **Continuous batching** — process new requests without waiting for batch completion

## The Economics

Every 2x speedup halves serving cost. This is why [[entities/nvidia]] GPUs, [[concepts/flash-attention]], and [[entities/vllm]] are so impactful — they compound.

See also: [[synthesis/serving-stack-2026]]
