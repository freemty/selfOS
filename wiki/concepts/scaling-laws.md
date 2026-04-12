---
title: "Scaling Laws"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["kaplan-scaling-paper", "hoffmann-chinchilla-paper"]
tags: [scaling, compute, power-law]
summary: "Empirical power-law relationships between model size, data, compute, and loss"
---

# Scaling Laws

[[sources/kaplan-scaling-paper]] first showed that language model loss follows smooth power laws as functions of model size (N), dataset size (D), and compute budget (C). This was transformative: it meant you could *predict* performance before training.

## Key Findings

1. **Power-law scaling** — loss ∝ N^{-α} for fixed data, loss ∝ D^{-β} for fixed model size
2. **Compute-optimal allocation** — for a fixed compute budget, there's an optimal balance between N and D
3. **[[concepts/chinchilla-optimal]]** — [[entities/deepmind]]'s refinement showing most models were undertrained

## Impact

Scaling laws turned LLM development from art into engineering. [[entities/openai]] used them to plan GPT-4; every major lab now has internal scaling law fits.

They also opened philosophical questions: if bigger = better on a predictable curve, is [[concepts/pre-training]] just about throwing compute at the problem? The answer is nuanced — [[concepts/data-efficiency]] and architecture choices still matter, but scale is the dominant variable.

## Connections

- [[concepts/distributed-training]] — the infrastructure that makes scale possible
- [[concepts/mixture-of-experts]] — a way to scale parameters without proportional compute
- [[concepts/emergent-abilities]] — capabilities that appear only at sufficient scale
- [[synthesis/scaling-vs-efficiency]] — the tension between scaling up and optimizing down
