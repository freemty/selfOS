---
title: "A Taxonomy of Parallelism Strategies"
type: synthesis
created: 2026-03-10
updated: 2026-03-10
sources: ["gpipe-paper"]
tags: [synthesis, distributed, parallelism, decision-framework]
summary: "When to use which parallelism strategy — a decision framework"
---

# Parallelism Taxonomy

| Strategy | Splits | Communication | Best For |
|----------|--------|--------------|----------|
| [[concepts/data-parallelism]] | Data | Allreduce | Model fits in 1 GPU |
| [[concepts/tensor-parallelism]] | Ops | Per-layer allreduce | Intra-node, fast interconnect |
| [[concepts/pipeline-parallelism]] | Layers | Point-to-point | Inter-node, high latency tolerance |
| FSDP/ZeRO | Optimizer+params | Allgather | Memory-constrained |

## Decision Framework

1. Model fits in 1 GPU? → [[concepts/data-parallelism]]
2. Doesn't fit? → Add FSDP/ZeRO ([[entities/deepspeed]])
3. Still doesn't fit? → [[concepts/tensor-parallelism]] within nodes ([[entities/megatron-lm]])
4. More nodes needed? → [[concepts/pipeline-parallelism]] across nodes

See also: [[concepts/distributed-training]]
