---
title: "Tensor Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [distributed, training, parallelism]
summary: "Splitting individual tensor operations across devices — intra-layer parallelism for large matrices"
---

# Tensor Parallelism

Split large matrix multiplications across GPUs. For a linear layer Y = XW, split W column-wise across GPUs, compute partial results, then combine.

## In [[entities/megatron-lm]]

Column-parallel and row-parallel linear layers alternate, minimizing communication. Each attention head can be placed on a separate GPU.

## Requirements

High-bandwidth interconnect (NVLink) — tensor parallelism communicates every layer. Only practical within a single node.

See also: [[concepts/model-parallelism]], [[concepts/pipeline-parallelism]], [[concepts/distributed-training]], [[entities/nvidia]]
