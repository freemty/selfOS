---
title: "LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)"
type: source
created: 2021-06-17
updated: 2021-06-17
sources: []
tags: [paper, lora, finetuning, microsoft]
summary: "Low-rank adaptation — efficient finetuning with minimal parameters"
source_type: "paper"
---

# LoRA

[[entities/microsoft]]'s paper introducing [[concepts/lora]]. Key insight: weight updates during finetuning are low-rank. Inject trainable BA matrices (r << d), freeze everything else. Revolutionized [[concepts/parameter-efficient-finetuning]].
