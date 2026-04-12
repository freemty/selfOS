---
title: "GPU Programming: CUDA vs. Triton vs. Framework Kernels"
type: synthesis
created: 2026-03-15
updated: 2026-03-15
sources: ["tillet-triton-paper"]
tags: [synthesis, gpu, programming, comparison]
summary: "The tradeoff space in GPU programming — flexibility vs. productivity"
---

# GPU Programming Landscape

| Approach | Flexibility | Productivity | Performance |
|----------|:-:|:-:|:-:|
| CUDA | High | Low | Highest |
| [[concepts/triton-compiler]] | Medium | High | High |
| torch.compile ([[entities/pytorch]]) | Low | Highest | Medium |

## When to Use What

- **torch.compile**: default choice, good enough for most [[concepts/kernel-fusion]]
- **Triton** ([[sources/tillet-triton-paper]]): custom kernels, [[concepts/flash-attention]]-style work
- **CUDA**: maximum performance, [[entities/nvidia]]-specific features

See also: [[concepts/gpu-memory-hierarchy]]
