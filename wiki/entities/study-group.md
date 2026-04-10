---
title: "Systems Paper Reading Group"
type: entity
created: 2025-10-03
updated: 2026-01-20
sources: ["gem-2025-10-03-flash-attention-deep-dive", "notion-2025-09-15-research-taste-is-underrated"]
tags: [group, community, learning, ml-systems]
summary: "Weekly paper reading group — 5 PhD students doing implementation-first systems reading"
---

# Systems Paper Reading Group

## What

A weekly reading group of 5 CS PhD students focused on ML systems papers. We meet Thursdays 4-6pm. Started Fall 2025 after I realized I needed a community for my [[concepts/career-pivots]] into systems.

## Members

- **Alex** (me) — efficient inference, KV-cache optimization
- **Priya** — distributed training, pipeline parallelism
- **Marcus** — compiler optimizations for ML workloads
- **Jing** — GPU kernel development, CUTLASS contributor
- **Ravi** — serving systems, request scheduling

## Format

We alternate between two modes:

### Reading Weeks (1st, 3rd week)
- One person presents a paper in depth
- Others read abstract + intro beforehand
- Discussion focuses on: What's the bottleneck? What's the insight? What would you do differently?

### Building Weeks (2nd, 4th week)
- Implement a key idea from the previous reading week
- Share code and findings — [[concepts/learning-by-building]] as group practice
- The gap between paper and implementation is always the best discussion

## Impact on My Thinking

### Taste Calibration

Pitching project ideas here is faster feedback than waiting for paper reviews. When I described my attention sink observation, Jing immediately said "that's a paper." When I pitched a vague efficiency idea, I got polite silence. That signal is invaluable for developing [[concepts/research-taste]] (source: [[sources/notion-2025-09-15-research-taste-is-underrated]]).

### Cross-Pollination

Priya's distributed training perspective and Marcus's compiler knowledge have directly influenced my inference work. Systems problems are inherently cross-cutting — a group with diverse specializations is more valuable than one focused on the same niche.

### Accountability

Knowing I need to present or demo something every two weeks keeps my [[concepts/learning-by-building]] practice consistent.

## Notable Sessions

- **FlashAttention deep dive** (2025-10): Jing walked us through the CUDA implementation. Combined with my Gemini session (source: [[sources/gem-2025-10-03-flash-attention-deep-dive]]), this was the deepest I've gone into any single system
- **Megatron-LM debate** (2025-11): 90 minutes arguing about tensor vs. pipeline parallelism tradeoffs
- **[[entities/tri-dao]] paper marathon** (2025-12): Read everything Tri published in 2024-2025, mapped the research trajectory

## Connection to Advisor

[[entities/alex-advisor]] encourages me to bring group insights to our 1-on-1s. She says the group gives me "systems intuition faster than any course."
