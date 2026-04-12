---
title: "GPU Memory Hierarchy"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["dao-flashattention-paper"]
tags: [hardware, gpu, memory, bandwidth]
summary: "The layered memory system in GPUs — understanding it is key to writing efficient ML kernels"
---

# GPU Memory Hierarchy

Understanding this hierarchy is what separates efficient from naive GPU code:

| Level | Size | Bandwidth | Latency |
|-------|------|-----------|---------|
| Registers | ~256KB/SM | — | 0 cycles |
| SRAM (shared memory) | ~100-228KB/SM | ~19 TB/s | ~30 cycles |
| L2 Cache | ~40-50MB | ~6 TB/s | ~200 cycles |
| HBM (global memory) | 40-80GB | ~2-3 TB/s | ~400 cycles |

## The Insight Behind [[concepts/flash-attention]]

[[entities/tri-dao]] realized that standard attention writes O(N²) data to HBM when the computation could stay in SRAM. Respecting this hierarchy gave a 2-4x speedup with no approximation.

## Implications for ML Systems

Most ML operations are memory-bound, not compute-bound. [[concepts/kernel-fusion]] and tiling ([[concepts/triton-compiler]]) are about keeping data in fast memory.

See also: [[entities/nvidia]], [[concepts/inference-optimization]]
