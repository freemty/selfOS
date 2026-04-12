---
title: "Chinchilla Optimal Training"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hoffmann-chinchilla-paper"]
tags: [scaling, data-efficiency, compute-optimal]
summary: "Training regime that balances model size and data quantity for fixed compute budget"
---

# Chinchilla Optimal Training

[[entities/deepmind]]'s Chinchilla paper ([[sources/hoffmann-chinchilla-paper]]) showed that most LLMs were significantly undertrained. For a fixed compute budget, the optimal strategy trains a *smaller* model on *more data* than the prevailing practice.

## The Rule of Thumb

Tokens ≈ 20× parameters. A 7B model should see ~140B tokens. GPT-3 (175B params) was trained on only 300B tokens — Chinchilla says it should have seen ~3.5T tokens.

## Impact

This insight redirected the field toward [[concepts/data-efficiency]]. Suddenly, data quality and quantity mattered as much as model size. It also made smaller, well-trained models competitive with larger undertrained ones.

See also: [[concepts/scaling-laws]], [[concepts/pre-training]], [[synthesis/scaling-vs-efficiency]]
