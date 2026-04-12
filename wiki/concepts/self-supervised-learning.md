---
title: "Self-Supervised Learning"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["chen-simclr-paper"]
tags: [pretext-task, representation, foundation]
summary: "Learning from unlabeled data by creating supervision from the data itself"
---

# Self-Supervised Learning

SSL creates supervisory signals from the data structure itself. No human labels needed.

## Forms

- **Next-token prediction** — [[concepts/pre-training]] for LLMs
- **Masked language modeling** — BERT-style
- **[[concepts/contrastive-learning]]** — SimCLR, MoCo for vision
- **Masked image modeling** — MAE for vision transformers

## Why It Matters

SSL is what makes foundation models possible. [[entities/meta-ai]]'s Yann LeCun ([[entities/yann-lecun]]) calls it "the dark matter of intelligence" — the bulk of what models learn comes from self-supervision, not from labeled examples.

See also: [[concepts/pre-training]], [[synthesis/ssl-to-foundation]]
