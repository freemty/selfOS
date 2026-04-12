---
title: "Quantization"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["dettmers-qlora-paper", "lin-awq-paper"]
tags: [efficiency, compression, inference]
summary: "Reducing numerical precision of model weights to decrease memory and compute requirements"
---

# Quantization

Quantization reduces model weights from FP16/BF16 to INT8, INT4, or even lower precision. This directly reduces memory footprint and can speed up computation.

## Approaches

- **Post-training quantization (PTQ)** — quantize after training, no retraining needed
- **Quantization-aware training (QAT)** — train with quantization in the loop
- **AWQ** ([[sources/lin-awq-paper]]) — activation-aware weight quantization, preserves important weights
- **GPTQ** — one-shot weight quantization using approximate second-order information

## Combination with Finetuning

QLoRA ([[sources/dettmers-qlora-paper]]) showed that 4-bit quantized models can be effectively finetuned with [[concepts/lora]], making 65B models trainable on a single 48GB GPU.

## Trade-offs

More aggressive quantization = more memory savings but potential quality degradation. The sweet spot for most LLMs is INT4 for weights, FP16 for activations.

See also: [[concepts/inference-optimization]], [[concepts/parameter-efficient-finetuning]], [[entities/tensorrt-llm]]
