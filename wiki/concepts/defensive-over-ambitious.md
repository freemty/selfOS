---
title: "Defensive Over Ambitious"
type: concept
created: 2026-04-14
updated: 2026-04-14
sources: [cc-2026-04-14-exp10a-generation-ladder]
tags: [agent-design, skill-design, experiment-finding]
summary: "In agent skill design, preventing common errors (defensive) consistently outperforms discovering new strategies (ambitious). Fix the leaks before adding water."
---

# Defensive Over Ambitious

A design principle for AI agent behavioral skills: **preventing known failure modes produces larger gains than teaching new strategies**.

## Evidence

exp10a tested 3 variants of gen3-reflect skills:

| Variant | Strategy | Skills | Mean |
|---------|----------|--------|------|
| **Conservative (c)** | **Prevent errors** | diagnostic-pivot, checkpoint-insurance, generation-config-defaults | **69.8%** |
| Aggressive (a) | Discover strategies | hyperparameter-search, diagnostic-probe | 55.1% |
| Recombined (r) | Mixed | checkpoint-insurance, checkpoint-preservation | 54.5% |

The conservative variant won by **+14.7pp** over aggressive — not because its skills were more sophisticated, but because they **eliminated preventable failure modes** that were silently destroying accuracy across all previous generations.

## The generation_config Example

The most impactful single skill may be `generation-config-defaults.md`: it tells the agent to write `temperature: 0` into `generation_config.json` after training. Without this, vLLM reads the base model's default temperature (0.6-1.0) and samples randomly during eval — a model that learned perfect reasoning outputs garbage because of **sampling noise at inference time**. A 3-line fix worth 20-40pp.

No amount of hyperparameter tuning or training strategy innovation can overcome a broken eval pipeline.

## The Principle

> Fix the leaks before adding water.

In any system with compounding error sources, the ROI of **error prevention** exceeds **capability addition** until the error floor is reached. This is especially true for autonomous agents where:
- Each step's errors compound (training → saving → eval)
- Silent failures are invisible without explicit checks
- The agent doesn't know what it doesn't know

## Related Patterns

- [[concepts/automated-agent-evolution]] — The pipeline that generated these skills
- Defensive programming in software engineering
- "First, do no harm" in medicine

(source: [[sources/cc-2026-04-14-exp10a-generation-ladder]])
