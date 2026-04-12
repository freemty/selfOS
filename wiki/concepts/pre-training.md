---
title: "Pre-training"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["kaplan-scaling-paper"]
tags: [training, next-token-prediction, foundation]
summary: "Training on massive unlabeled corpora to learn general representations before task-specific finetuning"
---

# Pre-training

Pre-training is the first and most expensive phase of building an LLM. The model learns to predict the next token on trillions of tokens from the internet.

## Why Next-Token Prediction Works

Predicting the next token forces the model to learn syntax, semantics, facts, reasoning patterns, and even common sense. It's [[concepts/self-supervised-learning]] at its most elegant.

## Scale Requirements

Modern pre-training requires:
- Trillions of tokens ([[concepts/chinchilla-optimal]])
- Thousands of GPUs ([[concepts/distributed-training]])
- Months of training time
- Millions of dollars in compute

## After Pre-training

Raw pre-trained models are capable but not useful. They need:
- [[concepts/rlhf]] or [[concepts/constitutional-ai]] for alignment
- [[concepts/lora]] or [[concepts/parameter-efficient-finetuning]] for task adaptation

See also: [[concepts/scaling-laws]], [[entities/openai]], [[entities/meta-ai]]
