---
title: "DeepSpeed"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, microsoft, distributed, zero]
summary: "Microsoft's distributed training library — ZeRO optimizer sharding"
entity_type: "tool"
---

# DeepSpeed

[[entities/microsoft]]'s library for efficient [[concepts/distributed-training]]. Key innovation: **ZeRO** (Zero Redundancy Optimizer) — progressively shard optimizer states, gradients, and parameters across GPUs.

ZeRO stages:
- Stage 1: shard optimizer states
- Stage 2: + shard gradients
- Stage 3: + shard parameters (= FSDP)

See also: [[concepts/data-parallelism]], [[entities/megatron-lm]], [[synthesis/parallelism-taxonomy]]
