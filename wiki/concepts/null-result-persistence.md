---
title: "Null Result Persistence"
type: concept
created: 2026-04-14
updated: 2026-04-14
sources: [cc-2026-04-14-pipeline-vindication-moment, cc-2026-04-14-exp10a-generation-ladder]
tags: [research-methodology, motivation, experiment-design]
summary: "Breakthroughs often follow extended periods of null results. The discipline to keep iterating systematically — not abandon on intuition — is what separates eventual success from premature quit."
---

# Null Result Persistence

## The Pattern

```
Week 1-2: Build pipeline, first results look promising (gen1r +11.6pp)
Week 3:   Scale up → signal collapses (exp05c overturns gen1r at n=16)
Week 3-4: Iterate pipeline v02→v04 → still no mean improvement (gen2r ≈ gen0)
          Motivation drops. "This is just playing around."
Week 4:   Pipeline v06 + defensive skills → gen3c 69.8% (+29pp over gen0)
```

The breakthrough came **one iteration after the point of maximum doubt.**

## The Danger Zone

Between "promising early signal" and "validated breakthrough" lies a valley of null results. During this valley:
- The infrastructure feels over-engineered for the signal it produces
- Each new experiment confirms "roughly the same as baseline"
- The temptation is to pivot to something that feels more productive
- The internal narrative shifts from "this will work" to "this is just playing around"

**This is exactly when systematic iteration matters most.** The null results aren't wasted — they're eliminating hypotheses and narrowing the search space.

## What Saved This Project

1. **Same-conditions comparison** — Instead of trusting cross-experiment comparisons (which had temporal confounds), exp10a ran ALL 7 generations simultaneously. This eliminated noise that had obscured the signal.

2. **Multi-variant pipeline** — Instead of betting on one "best" variant, the evolutionary pipeline produced 3 (conservative/aggressive/recombined). The winner was the one nobody would have hand-designed.

3. **Defensive skill discovery** — The pipeline found that the biggest gains came from preventing errors (generation_config temperature fix), not from ambitious new strategies. A human designer would have focused on the ambitious direction.

## Connection to Research Taste

[[concepts/research-taste]] says good researchers pick the right problems. But equally important is **not quitting the right problem too early**. The reflection pipeline was the right approach — it just needed more iterations than intuition suggested.

> 在 null results 阶段保持信念，但用系统化的方式来验证而不是靠直觉判断方向。

## Evolution

| Date | Event | Belief State |
|------|-------|-------------|
| 2026-03-25 | Pipeline v01 first run, 58 evidence → 12 changes | "This is promising!" |
| 2026-04-03 | exp05a gen1r +11.6pp | "Skills work!" |
| 2026-04-06 | exp05c overturns gen1r at n=16 | "Shit, was that noise?" |
| 2026-04-07 | exp06a gen2r ≈ gen0 (50% vs 47.6%) | "Pipeline only reduces variance" |
| 2026-04-07~13 | "完全没想做这个project" | **Maximum doubt** |
| 2026-04-14 | exp10a gen3c 69.8% (std 1.8) | "这太振奋人心了" |

(source: [[sources/cc-2026-04-14-pipeline-vindication-moment]])
