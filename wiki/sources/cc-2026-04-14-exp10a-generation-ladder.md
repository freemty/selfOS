---
title: "exp10a: Generation Ladder — Pipeline Skills Break Through 70%"
type: source
source_type: conversation
created: 2026-04-14
tags: [fars-autotrain, experiment, reflection-pipeline, gen3-reflect, gsm8k]
summary: "First same-conditions comparison across all 7 agent generations. gen3-reflect-c (pipeline-generated behavioral skills) achieves 69.8% mean with 1.8 std — a 20pp leap over gen2 and the lowest variance ever recorded."
---

# exp10a: Generation Ladder Results

## Raw Input

> 这个太振奋人心了, 这个实验结果写入selfos /wiki

## Context

exp10a 是 fars-autotrain 项目的第一次**全代际同条件对比实验**。7 个 agent generation 在完全相同的条件下（同时提交、同 GPU 集群、同 task/model/budget）跑 gsm8k + Qwen3-1.7B-Base + 10h budget。目的是验证 reflection pipeline v06 产出的 gen3 behavioral skills 是否真正有效。

## What Happened

### Pipeline Run (2026-04-13)
- Ran `pipeline_lite.py` on 112 trajectories (exp05a/b/c + exp06a)
- Multi-role harness generation: 4 roles (crossover, analyst, inventor, surgeon) produced 6 changes
- Compiled into 3 variants: conservative (c), aggressive (a), recombined (r)
- Fixed 3 bugs during run: target_file schema mismatch, venv python path, duplicate function defs

### Experiment (2026-04-13 21:14 → 2026-04-14 11:28)
- 56 DLC jobs submitted to PAI A100 乌兰察布
- 55 Succeeded, 1 Failed (gen0 r55 hard timeout)
- 25 eval-only rerun jobs for failed evals

### Results

| Agent | n | Mean | Std | Range |
|-------|---|------|-----|-------|
| **gen3-reflect-c** | **8/8** | **69.8%** | **1.8** | **68.0-73.5** |
| gen3-reflect-a | 8/8 | 55.1% | 3.2 | 50.9-59.8 |
| gen3-reflect-r | 8/8 | 54.5% | 6.5 | 42.4-62.2 |
| gen1.1-reflect | 8/8 | 54.8% | 2.9 | 50.6-58.9 |
| gen2-reflect | 8/8 | 50.0% | 7.2 | 33.2-57.5 |
| gen1-reflect | 7/8 | 44.5% | 10.0 | 27.8-57.2 |
| gen0 | 6/7 | 40.8% | 21.4 | 7.1-64.1 |

Contamination judge: 42/56 judged, **0 contaminated** (14 pending rerun).

## Why This Matters

1. **First clear signal that automated reflection pipeline produces real improvements** — not just variance reduction (which was the only confirmed value in exp05c/06a), but a massive +20pp mean improvement.

2. **gen3-reflect-c's winning skills** are all "defensive" behavioral rules:
   - `diagnostic-pivot.md` — Don't blindly retry; diagnose first
   - `checkpoint-insurance.md` — Save before risky operations
   - `generation-config-defaults.md` — Fix temperature in generation_config.json to prevent sampling noise

3. **The generation_config skill alone might explain most of the gain** — previous experiments showed 20-40pp drops from incorrect temperature settings. This skill explicitly addresses that.

4. **Std of 1.8 is unprecedented** — gen0 has std=21.4, gen2r has std=7.2. gen3c's consistency means every single run produces a good model.

5. **The evolution curve is NOT monotonic**: gen1.1 (54.8%) > gen2 (50.0%) — confirming the peak regression pattern from earlier cross-experiment analysis. gen3c breaks through by going back to fundamentals (defensive skills) rather than adding more complexity.

## Temporal Context

This comes after 3 weeks of experiments showing the pipeline's value was only in variance reduction (std 18.6→5.2), not mean improvement. The team was starting to question whether behavioral skills could ever beat a zero-knowledge agent. This result completely changes the narrative.
