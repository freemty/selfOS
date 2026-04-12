---
title: "Triton"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["tillet-triton-paper"]
tags: [compiler, gpu, dsl, kernel]
summary: "Python-like DSL for writing GPU kernels — lowers the barrier to custom CUDA programming"
---

# Triton

[[sources/tillet-triton-paper]], from [[entities/openai]], introduced Triton: a Python-like language for writing GPU kernels. Instead of managing threads and shared memory manually (CUDA), you think in terms of blocks and let the compiler handle the rest.

## Impact

Triton democratized GPU programming for ML researchers. [[concepts/flash-attention]] was prototyped in Triton. Custom [[concepts/kernel-fusion]] became accessible without deep CUDA expertise.

See also: [[concepts/gpu-memory-hierarchy]], [[entities/nvidia]], [[synthesis/gpu-programming-landscape]]
