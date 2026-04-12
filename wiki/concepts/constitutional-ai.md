---
title: "Constitutional AI"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [alignment, safety, anthropic, self-improvement]
summary: "Anthropic's approach to alignment using principles for self-improvement without human labels"
---

# Constitutional AI

Developed by [[entities/anthropic]], Constitutional AI replaces human preference labels with a set of principles (a "constitution"). The model critiques and revises its own outputs based on these principles.

## How It Works

1. Generate responses
2. Ask the model to critique its response against the constitution
3. Ask the model to revise based on the critique
4. Train on the revised outputs

This is a form of [[concepts/self-critique]] — the model improves itself using explicit principles rather than implicit human preferences.

## Advantage Over [[concepts/rlhf]]

- **Scalable** — no human labelers needed per example
- **Transparent** — the principles are explicit and auditable
- **Controllable** — change behavior by changing the constitution

See also: [[concepts/alignment]], [[synthesis/alignment-landscape]]
