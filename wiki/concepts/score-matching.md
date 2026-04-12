---
title: "Score-Based Models"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["song-score-sde-paper"]
tags: [generative, score-function, sde]
summary: "Learning the gradient of the log-probability — a unified framework for diffusion and score-based generation"
---

# Score-Based Models

Score matching learns the score function ∇_x log p(x) — the gradient of the log-probability. Once you have the score, you can generate samples via Langevin dynamics.

## Unification with Diffusion

[[sources/song-score-sde-paper]] showed that DDPM ([[sources/ho-ddpm-paper]]) and score-based models are two views of the same framework, connected through [[concepts/stochastic-differential-equations]].

See also: [[concepts/diffusion-models]], [[synthesis/diffusion-foundations]]
