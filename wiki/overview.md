---
title: "Knowledge Base Overview"
type: overview
created: 2026-04-08
updated: 2026-04-08
summary: "A CS PhD student's journey from theory to ML systems — taste, building, and finding direction"
---

# Knowledge Base Overview

This knowledge base records the intellectual development of a CS PhD student (Alex Chen) navigating the transition from theoretical ML to ML systems research. Three source types — Notion reflections, Gemini deep-dives, and Claude conversations — capture a journey spanning September 2025 to January 2026.

The wiki currently contains 3 concepts, 3 entities, and 3 sources.

## Core Narrative: Finding Direction Through Taste

The central arc is a **career pivot** from theory to systems, driven by a growing sense of [[concepts/research-taste]]. The pivot wasn't a single decision but an accumulation of signals:

1. **The wake-up call** (Sept 2025) — [[entities/alex-advisor]] asks "Is this the right problem?" about a technically impressive but strategically irrelevant CUDA kernel. This triggers a reflection on what separates impactful research from merely clever research.

2. **The deep dive** (Oct 2025) — A 3-hour Gemini session on FlashAttention reveals that [[entities/tri-dao]]'s genius was in problem selection, not algorithm complexity. The tiling + online softmax trick came from asking "what does the GPU want?" — a hardware-first mindset that theory training doesn't develop.

3. **The crystallization** (Jan 2026) — A Claude conversation makes the implicit explicit: the energy, the output quality, the taste all point toward systems. The pivot is formalized.

## How the Nodes Connect

The graph has a dense core with three concept nodes tightly linked:

- **[[concepts/research-taste]]** is the central concept — it connects upward to the role model ([[entities/tri-dao]]) who exemplifies it, sideways to the methodology ([[concepts/learning-by-building]]) that develops it, and downward to the career decision ([[concepts/career-pivots]]) that applies it.

- **[[concepts/learning-by-building]]** is the methodology — building FlashAttention from scratch gave Alex intuitions that reading 50 papers wouldn't. The [[entities/study-group]] institutionalizes this practice.

- **[[concepts/career-pivots]]** is the outcome — all three sources converge on this decision, each from a different angle (reflection, technical deep-dive, dialogue).

The three entities form a support structure: [[entities/alex-advisor]] provides strategic guidance, [[entities/tri-dao]] provides a north star for what "good" looks like, and [[entities/study-group]] provides community and accountability.

## Key Insights

1. **Taste is the bottleneck, not skill** — every PhD student can implement a transformer; few can sense which problem will matter next
2. **Building is the fastest path to taste** — the gap between paper and implementation is where real understanding lives
3. **A pivot is a taste signal, not a failure** — following energy toward systems was the clearest expression of developing research taste
4. **Community accelerates calibration** — the study group provides faster feedback on ideas than the publication cycle
