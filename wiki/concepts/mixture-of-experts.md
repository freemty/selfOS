---
title: "Mixture of Experts"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["shazeer-moe-paper"]
tags: [architecture, sparse, routing, scaling]
summary: "Architecture where only a subset of parameters activate per input — massive models with manageable compute"
---

# Mixture of Experts

MoE ([[sources/shazeer-moe-paper]]) replaces the dense feed-forward layer with multiple "expert" sub-networks and a routing mechanism that selects top-K experts per token.

## Why It Matters

MoE decouples model capacity from compute cost. A 1T parameter MoE model might only use 100B parameters per token — giving the knowledge of a huge model at the cost of a smaller one.

## Systems Challenges

- **Load balancing** — ensuring all experts get roughly equal traffic
- **Communication** — expert parallelism across GPUs requires all-to-all communication
- **Memory** — all expert weights must be in memory even if sparsely used

## Examples

- GShard, Switch Transformer ([[entities/google-brain]])
- Mixtral (Mistral AI)
- DeepSeek-V3

See also: [[concepts/transformer-architecture]], [[concepts/scaling-laws]], [[concepts/distributed-training]]
