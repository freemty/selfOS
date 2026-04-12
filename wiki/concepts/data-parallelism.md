---
title: "Data Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [distributed, training, parallelism]
summary: "Splitting training data across devices while replicating the model — the simplest form of distributed training"
---

# Data Parallelism

The simplest [[concepts/distributed-training]] strategy: replicate the full model on every GPU, split the data batch. Each GPU computes gradients on its shard, then gradients are synchronized via allreduce.

## Variants

- **DDP** ([[entities/pytorch]]) — vanilla allreduce after each backward pass
- **FSDP** — shard optimizer states and weights across GPUs (ZeRO-style)
- **[[entities/deepspeed]] ZeRO** — progressive sharding of optimizer/gradients/parameters

## When to Use

Data parallelism is the default choice when the model fits in one GPU's memory. When it doesn't, you need [[concepts/model-parallelism]].

See also: [[concepts/tensor-parallelism]], [[concepts/pipeline-parallelism]], [[synthesis/parallelism-taxonomy]]
