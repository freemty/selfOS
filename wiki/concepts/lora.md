---
title: "LoRA"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hu-lora-paper"]
tags: [finetuning, low-rank, parameter-efficient]
summary: "Low-Rank Adaptation — efficient finetuning by injecting trainable low-rank matrices into frozen pretrained weights"
---

# LoRA

LoRA (Low-Rank Adaptation), from [[sources/hu-lora-paper]] by [[entities/microsoft]], made finetuning billion-parameter models practical. Instead of updating all weights, inject small trainable low-rank matrices: W' = W + BA, where B ∈ R^{d×r} and A ∈ R^{r×d} with r << d.

## Why It Works

The key hypothesis: the weight updates during finetuning have low intrinsic rank. You don't need full-rank updates to adapt a pretrained model to a new task.

## Practical Impact

- **Memory**: train a 7B model on a single consumer GPU
- **Storage**: swap tasks by swapping small adapter files (~MB vs GB)
- **Speed**: fewer trainable parameters = faster training

## Extensions

- **QLoRA** ([[sources/dettmers-qlora-paper]]) — combine with [[concepts/quantization]] for even lower memory
- **Adapter methods** — broader family of [[concepts/parameter-efficient-finetuning]] techniques

See also: [[concepts/pre-training]], [[synthesis/finetuning-decision-tree]]
