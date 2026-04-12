---
title: "Flash Attention"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["dao-flashattention-paper"]
tags: [attention, gpu, io-aware, memory-hierarchy]
summary: "IO-aware exact attention algorithm — makes long-context practical by respecting GPU memory hierarchy"
---

# Flash Attention

Created by [[entities/tri-dao]], FlashAttention (source: [[sources/dao-flashattention-paper]]) is the canonical example of hardware-aware algorithm design. The insight: standard attention isn't compute-bound — it's **memory-bound**. The O(N²) attention matrix writes to slow HBM when it could stay in fast SRAM.

## Core Technique: Tiling + Online Softmax

1. Load blocks of Q, K, V into SRAM
2. Compute attention incrementally using the online softmax trick
3. Never materialize the full N×N attention matrix in HBM

Result: same exact attention, but IO-complexity drops from O(N²) to O(N² d² M⁻¹).

## Why It Matters

- Enables [[concepts/long-context]] — 100K+ token windows become practical
- **Exact**, not approximate — unlike sparse/linear attention variants
- Made [[concepts/attention-mechanism]] fast enough that alternatives lost their appeal

## Broader Lesson

FlashAttention demonstrates that understanding [[concepts/gpu-memory-hierarchy]] can yield bigger speedups than algorithmic approximation. This is the core thesis of ML systems research: the hardware matters as much as the math.

See also: [[concepts/kernel-fusion]], [[concepts/inference-optimization]], [[entities/nvidia]]
