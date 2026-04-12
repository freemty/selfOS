---
title: "Attention Mechanism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper", "dao-flashattention-paper"]
tags: [attention, self-attention, multi-head]
summary: "Weighted aggregation over input tokens — the core building block of transformers"
---

# Attention Mechanism

Attention computes a weighted sum over values, where weights are derived from query-key similarity. In self-attention, queries, keys, and values all come from the same sequence.

## The Math

`Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V`

This simple formula is the heart of the [[concepts/transformer-architecture]]. The softmax creates a probability distribution over positions, allowing each token to "attend to" relevant context.

## Computational Challenge

Standard attention is O(N²) in sequence length — both compute and memory. This bottleneck drove two lines of work:
1. **Approximation**: sparse attention, linear attention — trade accuracy for speed
2. **[[concepts/flash-attention]]**: keep exact attention, but respect [[concepts/gpu-memory-hierarchy]] — [[entities/tri-dao]]'s insight

The second approach won. [[concepts/flash-attention]] proved you don't need to approximate if you understand the hardware.

## In Practice

- **[[concepts/kv-cache]]** — caching keys/values across autoregressive steps
- **Multi-head attention** — parallel attention with different learned projections
- **Cross-attention** — queries from one sequence, keys/values from another (used in [[concepts/conditional-generation]])

See also: [[sources/vaswani-attention-paper]], [[sources/dao-flashattention-paper]]
