---
title: "Megatron-LM"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, nvidia, distributed-training, parallelism]
summary: "NVIDIA's framework for 3D parallelism — tensor, pipeline, and data parallelism combined"
entity_type: "tool"
---

# Megatron-LM

[[entities/nvidia]]'s framework for training massive language models. Implements:
- [[concepts/tensor-parallelism]] — split attention heads and FFN across GPUs
- [[concepts/pipeline-parallelism]] — split layers across stages
- [[concepts/data-parallelism]] — replicate across groups

The reference implementation for [[concepts/distributed-training]] at scale.

See also: [[entities/deepspeed]], [[synthesis/parallelism-taxonomy]]
