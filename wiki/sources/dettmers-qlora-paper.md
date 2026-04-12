---
title: "QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023)"
type: source
created: 2023-05-23
updated: 2023-05-23
sources: []
tags: [paper, qlora, quantization, finetuning]
summary: "4-bit quantization + LoRA — finetune 65B on a single GPU"
source_type: "paper"
---

# QLoRA

Combined [[concepts/quantization]] (4-bit NormalFloat) with [[concepts/lora]] to finetune 65B models on a single 48GB GPU. Introduced double quantization and paged optimizers.

See also: [[concepts/parameter-efficient-finetuning]], [[synthesis/finetuning-decision-tree]]
