---
title: "Pipeline Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["gpipe-paper"]
tags: [distributed, training, pipeline]
summary: "Splitting model layers across stages that process micro-batches in pipeline fashion"
---

# Pipeline Parallelism

Split the model into stages (groups of layers), each on a different GPU. Micro-batches flow through the pipeline, keeping all stages busy.

## The Bubble Problem

When the pipeline starts and drains, some stages are idle — the "pipeline bubble." [[sources/gpipe-paper]] introduced micro-batching to minimize this. Modern schedules (1F1B, interleaved) reduce bubbles further.

## When to Use

Pipeline parallelism shines for very deep models across nodes with limited inter-node bandwidth. Combine with [[concepts/tensor-parallelism]] for intra-node and [[concepts/data-parallelism]] for scaling across groups.

See also: [[concepts/model-parallelism]], [[entities/megatron-lm]], [[synthesis/parallelism-taxonomy]]
