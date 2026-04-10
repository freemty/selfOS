---
title: "Flash Attention Deep Dive"
type: source
created: 2025-10-03
updated: 2025-10-03
sources: []
tags: [flash-attention, systems, gpu, ml-systems, tri-dao]
summary: "Technical deep dive into FlashAttention with Gemini — tiling, memory hierarchy, IO complexity"
richness: high
---

# Flash Attention Deep Dive

## Context

Extended Gemini session working through the FlashAttention and FlashAttention-2 papers line by line. Took about 3 hours. This was part of my [[concepts/learning-by-building]] practice — I implemented a simplified version in Triton afterward.

## Key Technical Insights

### The Core Trick: Tiling + Online Softmax

The insight isn't "make attention faster" — it's recognizing that standard attention is **memory-bound, not compute-bound**. The naive implementation writes O(N^2) intermediate values to HBM when the actual computation could stay in SRAM.

FlashAttention reorders the computation so that:
1. Blocks of Q, K, V are loaded into SRAM once
2. Softmax is computed incrementally (online softmax trick)
3. The O(N^2) attention matrix never materializes in HBM

### Why This Matters Beyond Speed

- Makes long-context models **practical**, not just theoretically possible
- Exact attention — no approximation, unlike sparse/linear variants
- The IO-complexity analysis is beautiful: O(N^2 d^2 M^{-1}) vs. O(N^2 d + N^2) for standard

### What I Learned From [[entities/tri-dao]]'s Approach

Tri didn't start from "how to approximate attention." He started from "what does the hardware actually want?" This is [[concepts/research-taste]] in action — the problem formulation came from understanding GPU memory hierarchy deeply, not from chasing benchmarks.

## Implementation Notes

My Triton implementation handled the forward pass but the backward pass was brutal. The recomputation strategy for gradients is where most of the engineering complexity lives. This is why [[concepts/learning-by-building]] works — you don't appreciate the difficulty gradient until you try.

## Open Questions

- How will FlashAttention evolve as hardware changes? (e.g., HBM4, larger SRAM)
- Could the tiling strategy generalize to other memory-bound operations in transformers?

## Connection to My Research

This deep dive confirmed my direction choice. [[concepts/career-pivots]] — choosing ML systems means exactly this kind of work: understanding hardware-software co-design. [[entities/alex-advisor]] was right that systems taste requires building intuition at the metal level.

(source: Gemini conversation, 2025-10-03)
