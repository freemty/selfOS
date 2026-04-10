---
title: "Research Taste"
type: concept
created: 2025-09-15
updated: 2026-01-20
sources: ["notion-2025-09-15-research-taste-is-underrated", "gem-2025-10-03-flash-attention-deep-dive", "cc-2026-01-20-why-i-chose-systems-over-theory"]
tags: [research, methodology, taste, career]
summary: "The ability to sense which problems will matter — separates impactful researchers from merely productive ones"
---

# Research Taste

## Definition

Research taste is the ability to select problems that are:
1. **Important** — will matter to the field in 2-3 years
2. **Tractable** — hard enough to be interesting, solvable enough to make progress
3. **Well-timed** — the tools and data to solve them are just becoming available

It is distinct from technical skill. Technical skill is necessary but not sufficient. Taste is what makes the difference between "that was clever" and "that changed how we think."

## How Taste Develops

### Through [[concepts/learning-by-building]]

Building systems gives you physical intuition for where the bottlenecks really are. Reading papers tells you where people *say* the bottlenecks are — often different. My FlashAttention deep dive (source: [[sources/gem-2025-10-03-flash-attention-deep-dive]]) taught me more about the memory hierarchy problem than any survey paper.

### Through Exposure to Role Models

Studying how [[entities/tri-dao]] chose the attention bottleneck as his target. He didn't follow the crowd toward sparse attention or linear attention — he went to the hardware level and asked "what does the GPU actually want?" That's taste in formulation.

### Through Community Calibration

[[entities/study-group]] serves as a taste calibration mechanism. Pitching project ideas and reading the room's reaction is a faster feedback loop than waiting for paper reviews.

## Taste vs. Ambition

Taste without ambition produces interesting but small work. Ambition without taste produces impressive but misguided work. The goal is alignment between the two.

## Connection to [[concepts/career-pivots]]

Choosing ML systems over theory was itself a taste decision. The bottleneck is moving from algorithms to infrastructure, and recognizing that shift early is a form of research taste (source: [[sources/cc-2026-01-20-why-i-chose-systems-over-theory]]).

## Open Questions

- Can taste be explicitly taught, or only developed through experience?
- Is taste domain-specific or transferable? (Does taste in systems transfer to taste in applications?)
- How do you distinguish genuine taste from contrarianism?
