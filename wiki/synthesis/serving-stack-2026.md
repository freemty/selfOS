---
title: "LLM Serving Stack in 2026"
type: synthesis
created: 2026-03-01
updated: 2026-03-01
sources: []
tags: [synthesis, serving, inference, systems]
summary: "The modern LLM serving stack — from kernel to API"
---

# LLM Serving Stack in 2026

Bottom-up:

1. **Hardware**: [[entities/nvidia]] GPUs, [[concepts/gpu-memory-hierarchy]]
2. **Kernels**: [[concepts/flash-attention]], [[concepts/kernel-fusion]] ([[entities/tensorrt-llm]])
3. **Runtime**: [[concepts/kv-cache]] + PagedAttention ([[entities/vllm]])
4. **Algorithm**: [[concepts/speculative-decoding]], [[concepts/quantization]]
5. **API**: load balancing, continuous batching, routing

Every layer compounds. 2x kernel speedup × 2x runtime efficiency × 2x quantization = 8x total throughput improvement.

See also: [[concepts/inference-optimization]], [[concepts/long-context]]
