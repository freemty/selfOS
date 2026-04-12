---
title: "Kernel Fusion"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [gpu, optimization, fusion, memory]
summary: "Combining multiple GPU operations into a single kernel to reduce memory traffic and launch overhead"
---

# Kernel Fusion

Each GPU kernel launch reads inputs from HBM and writes outputs back to HBM. If two operations are chained (e.g., matmul → activation → layernorm), fusing them into one kernel avoids intermediate HBM reads/writes.

## Why It Matters

For memory-bound operations (which most ML ops are), fusion can give 2-5x speedups by reducing [[concepts/gpu-memory-hierarchy]] traffic.

## Tools

- **[[concepts/triton-compiler]]** — write fused kernels in Python-like DSL
- **[[entities/tensorrt-llm]]** — automatic fusion for inference
- **torch.compile** ([[entities/pytorch]]) — JIT fusion

See also: [[concepts/flash-attention]], [[concepts/inference-optimization]]
