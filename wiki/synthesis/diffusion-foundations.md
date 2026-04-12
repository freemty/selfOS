---
title: "Diffusion Models: Mathematical Foundations"
type: synthesis
created: 2026-01-25
updated: 2026-01-25
sources: ["ho-ddpm-paper", "song-score-sde-paper", "ho-cfg-paper"]
tags: [synthesis, diffusion, math, foundations]
summary: "From Brownian motion to DALL-E — the mathematical path"
---

# Diffusion Foundations

The mathematical lineage:
1. **[[concepts/score-matching]]** — learn ∇log p(x) ([[sources/song-score-sde-paper]])
2. **[[concepts/diffusion-models]]** — reverse a noising process ([[sources/ho-ddpm-paper]])
3. **[[concepts/stochastic-differential-equations]]** — continuous-time unification
4. **[[concepts/classifier-free-guidance]]** — conditional control ([[sources/ho-cfg-paper]])

These build on each other. Understanding SDEs makes the design space clear: you're choosing a forward process (noise schedule) and learning the reverse.

See also: [[concepts/conditional-generation]], [[entities/google-brain]]
