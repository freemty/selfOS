---
title: "Transformer Architecture"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper"]
tags: [architecture, deep-learning, nlp]
summary: "The dominant neural network architecture based on self-attention — replaced RNNs for sequence modeling"
---

# Transformer Architecture

The Transformer, introduced in [[sources/vaswani-attention-paper]], fundamentally changed how we process sequences. By replacing recurrence with [[concepts/attention-mechanism]], it enabled massive parallelization during training and set the stage for the scaling era.

## Core Components

1. **Multi-head self-attention** — the core innovation (see [[concepts/attention-mechanism]])
2. **[[concepts/positional-encoding]]** — injecting sequence order into a permutation-invariant architecture
3. **Feed-forward networks** — per-position nonlinear transformations
4. **Layer normalization + residual connections** — training stability

## Why It Won

The Transformer's parallelizability unlocked [[concepts/scaling-laws]]: once you can train efficiently on thousands of GPUs via [[concepts/distributed-training]], the path to billion-parameter models opens. [[entities/google-brain]] showed this first; [[entities/openai]] took it furthest.

## Variants and Extensions

- [[concepts/mixture-of-experts]] — sparse activation for massive capacity
- [[concepts/flash-attention]] — hardware-aware exact attention ([[entities/tri-dao]])
- [[concepts/rope]] — modern positional encoding for [[concepts/long-context]]

The architecture has proven remarkably robust. Most improvements since 2017 are about *training it better* ([[concepts/scaling-laws]], [[concepts/pre-training]]) or *serving it faster* ([[concepts/inference-optimization]]), not changing the core design.
