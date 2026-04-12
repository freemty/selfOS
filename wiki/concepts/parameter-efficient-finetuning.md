---
title: "Parameter-Efficient Finetuning"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hu-lora-paper", "dettmers-qlora-paper"]
tags: [finetuning, efficiency, adaptation]
summary: "Methods to adapt large models with minimal trainable parameters"
---

# Parameter-Efficient Finetuning

Updating all parameters of a billion-parameter model is expensive. PEFT methods freeze most weights and only train a small subset.

## Methods

- **[[concepts/lora]]** — low-rank matrices ([[sources/hu-lora-paper]])
- **Adapters** — small bottleneck modules between layers
- **Prompt tuning** — learnable soft prompts
- **QLoRA** — [[concepts/lora]] + [[concepts/quantization]] ([[sources/dettmers-qlora-paper]])

See also: [[concepts/pre-training]], [[synthesis/finetuning-decision-tree]]
