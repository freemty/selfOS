---
title: "Contrastive Learning"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["chen-simclr-paper"]
tags: [self-supervised, representation-learning]
summary: "Learning representations by pulling similar pairs together and pushing dissimilar pairs apart"
---

# Contrastive Learning

[[sources/chen-simclr-paper]] showed that contrastive learning — simple positive/negative pair training — could match supervised performance on ImageNet.

## Core Idea

Given an anchor, pull positive examples closer in embedding space, push negatives away. The InfoNCE loss formalizes this.

## Impact

Contrastive learning is the foundation of:
- [[concepts/embedding-models]] — how text embeddings are trained
- [[concepts/self-supervised-learning]] — learning without labels
- Vision-language models (CLIP) — aligning images and text

See also: [[entities/meta-ai]], [[entities/google-brain]]
