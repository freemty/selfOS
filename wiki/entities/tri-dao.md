---
title: "Tri Dao"
type: entity
created: 2025-10-03
updated: 2026-01-20
sources: ["gem-2025-10-03-flash-attention-deep-dive", "notion-2025-09-15-research-taste-is-underrated"]
tags: [person, ml-systems, role-model, flash-attention]
summary: "FlashAttention creator — role model for systems research taste and hardware-aware algorithm design"
---

# Tri Dao

## Who

Princeton PhD, now at Together AI. Creator of FlashAttention and FlashAttention-2. One of the clearest examples of [[concepts/research-taste]] in ML systems — choosing the right problem at the right time with the right formulation.

## Why He Matters to Me

### As a Research Taste Exemplar

FlashAttention's genius wasn't the algorithm — it was the **problem selection**. While others were chasing sparse attention or linear attention approximations, Tri asked: "What if standard attention is fine, and the bottleneck is just IO?" That reframing from "approximate the math" to "respect the hardware" is what [[concepts/research-taste]] looks like (source: [[sources/gem-2025-10-03-flash-attention-deep-dive]]).

### As a Systems Research Role Model

He bridges the gap between:
- Deep mathematical understanding (the IO-complexity analysis is rigorous)
- Practical systems engineering (the implementation details that make it work on real GPUs)
- Strategic timing (long-context was about to become critical)

This is the kind of researcher I want to be. Not "theory person" or "systems person" — someone who uses hardware understanding to find elegant mathematical solutions to practical problems.

## Key Patterns I'm Distilling

1. **Start from hardware, not from math** — understand what the machine wants before designing the algorithm
2. **Exact > approximate** — if you can make the exact thing fast enough, don't approximate
3. **Clean formulation wins** — FlashAttention's tiling + online softmax is simple once you see it, but required deep insight to find
4. **Systems papers can be intellectually deep** — this work demolishes the "systems is just engineering" dismissal

## Connection to My Work

Studying Tri's approach directly influenced my [[concepts/career-pivots]] — choosing systems over theory. My FlashAttention reimplementation ([[concepts/learning-by-building]]) was a conscious attempt to develop the same kind of hardware intuition.

[[entities/study-group]] has read both FlashAttention papers. The group consensus: this is what "doing systems right" looks like.
