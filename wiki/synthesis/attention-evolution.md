---
title: "Attention Mechanism Evolution"
type: synthesis
created: 2026-01-15
updated: 2026-01-15
sources: ["vaswani-attention-paper", "dao-flashattention-paper"]
tags: [synthesis, attention, evolution, systems]
summary: "How attention went from bottleneck to efficient — and what's next"
---

# Attention Evolution

Timeline:
1. **Vanilla attention** ([[sources/vaswani-attention-paper]]) — O(N²) memory, simple but expensive
2. **Sparse/linear attention** (2019-2021) — approximate, trade quality for speed
3. **[[concepts/flash-attention]]** ([[sources/dao-flashattention-paper]]) — exact + fast via [[concepts/gpu-memory-hierarchy]]
4. **Ring attention** — distribute across devices for ultra-long contexts

## Lesson

The winning approach wasn't mathematical cleverness (approximation) but systems insight (IO-awareness). [[entities/tri-dao]] understood the hardware better than the approximation crowd understood the math.

See also: [[concepts/attention-mechanism]], [[concepts/long-context]], [[concepts/kernel-fusion]]
