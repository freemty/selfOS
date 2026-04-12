---
title: "Distributed Training"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [training, parallelism, infrastructure]
summary: "Training models across multiple GPUs or nodes — essential for billion-parameter scale"
---

# Distributed Training

Training billion-parameter models requires distributing work across many GPUs. This is not just "run the same thing on more machines" — it's a deep systems problem involving communication, memory, and scheduling.

## Four Forms of Parallelism

1. **[[concepts/data-parallelism]]** — replicate model, split data. Simplest. Scales well until model doesn't fit in one GPU.
2. **[[concepts/tensor-parallelism]]** — split individual matrix operations across GPUs. Intra-layer. High communication.
3. **[[concepts/pipeline-parallelism]]** — split layers across stages. Inter-layer. Bubble overhead.
4. **[[concepts/model-parallelism]]** — umbrella term for tensor + pipeline parallelism.

Modern systems like [[entities/megatron-lm]] use **3D parallelism**: all three combined.

## Key Infrastructure

- **[[entities/pytorch]]** — DDP for data parallelism, FSDP for sharded data parallelism
- **[[entities/deepspeed]]** — ZeRO optimizer sharding
- **[[entities/nvidia]]** — NCCL for GPU collective communication
- **[[entities/megatron-lm]]** — NVIDIA's 3D parallelism framework

## The Communication Bottleneck

Every form of parallelism introduces communication overhead. The art is choosing the right strategy for your model size, cluster topology, and interconnect bandwidth.

See also: [[concepts/scaling-laws]], [[synthesis/parallelism-taxonomy]]
