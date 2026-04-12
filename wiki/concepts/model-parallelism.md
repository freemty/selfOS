---
title: "Model Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [distributed, training, parallelism]
summary: "Splitting the model itself across devices — necessary when models exceed single-GPU memory"
---

# Model Parallelism

When a model doesn't fit in one GPU, you split it across multiple GPUs. Two main approaches:

1. **[[concepts/tensor-parallelism]]** — split individual operations (intra-layer)
2. **[[concepts/pipeline-parallelism]]** — split layers across stages (inter-layer)

## Trade-offs

Tensor parallelism has high communication but no bubble overhead. Pipeline parallelism has lower communication but wastes compute in bubbles. [[entities/megatron-lm]] combines both in 3D parallelism.

See also: [[concepts/distributed-training]], [[concepts/data-parallelism]], [[synthesis/parallelism-taxonomy]]
