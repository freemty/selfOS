---
title: "Automated Agent Evolution"
type: concept
created: 2026-04-14
updated: 2026-04-14
sources: [cc-2026-04-14-exp10a-generation-ladder]
tags: [fars-autotrain, reflection-pipeline, meta-learning, agent-improvement]
summary: "Automatically improving AI agent behavior through evidence-grounded reflection pipelines — extracting patterns from agent trajectories and compiling behavioral skills for the next generation."
---

# Automated Agent Evolution

The idea that you can **automatically improve an AI agent's behavior** by analyzing what it did wrong (and right), extracting patterns, and injecting corrective behavioral rules — without changing the underlying model, only its instructions.

## Core Insight

An LLM agent's performance is bottlenecked not by its intelligence, but by its **decision-making process**. A zero-knowledge agent (gen0) with Claude Opus 4.6 achieves 40.8% on gsm8k post-training. The same model with 3 simple behavioral skills (gen3-reflect-c) achieves **69.8%** — a +29pp improvement from instructions alone.

### The Smoking Gun

gen0's best run (r48, 64.1%) **independently discovered and fixed** the same generation_config bug that gen3c's skill encodes. gen0's worst run (r50, 7.1%) didn't — a 57pp gap from pure luck. The pipeline's value is turning lucky discoveries into standard operations: **eliminating luck as a variable in agent performance.**

## The Reflection Pipeline

```
Trajectories → Summarize → Extract Evidence → Mine Patterns → Generate Skills → Compile Agent → Validate (A/B)
```

Each generation learns from the previous generation's mistakes. The pipeline is fully automated (42 min for 112 trajectories), with human review only at gates between stages.

## Key Finding: Defensive Skills > Ambitious Skills

exp10a (2026-04-14) showed that the **conservative variant** (diagnostic-pivot + checkpoint-insurance + generation-config-defaults) massively outperformed the aggressive variant (hyperparameter-search + diagnostic-probe). The winning skills are all about **preventing mistakes**, not discovering new strategies:

- Don't retry blindly — diagnose first
- Save checkpoints before risky operations  
- Fix generation config temperature to prevent eval sampling noise

This suggests agent failure modes are dominated by **preventable errors**, not lack of strategy.

## Evolution Curve (exp10a, same conditions)

| Generation | Mean | Std | Key Change |
|-----------|------|-----|------------|
| gen0 | 40.8% | 21.4 | No skills |
| gen1-reflect | 44.5% | 10.0 | First pipeline output |
| gen1.1-reflect | 54.8% | 2.9 | Pipeline v02 |
| gen2-reflect | 50.0% | 7.2 | Pipeline v04 (peak regression) |
| **gen3-reflect-c** | **69.8%** | **1.8** | **Pipeline v06 defensive skills** |

The curve is NOT monotonic — gen2 regressed from gen1.1. gen3c broke through by changing strategy from "add more complexity" to "prevent common errors."

## Implications

1. **Behavioral skills are a real lever** — not just noise reduction, but +29pp mean improvement
2. **The right 3 rules matter more than 10 mediocre rules** — gen3c has 10 skills but the 3 new defensive ones drive the gain
3. **Automated pipelines can discover effective skills** — no human wrote these rules; the pipeline extracted them from trajectory evidence
4. **Meta-learning on agent behavior works** — the autoresearch@home thesis is validated

## Open Questions

- Does gen3c's advantage transfer to other tasks (bfcl, humaneval)?
- Is the generation_config fix the dominant factor? (Ablation needed)
- Can the pipeline discover similarly impactful skills in future generations, or is this a one-time low-hanging-fruit correction?

(source: [[sources/cc-2026-04-14-exp10a-generation-ladder]])
