---
title: "Stochastic Differential Equations"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["song-score-sde-paper"]
tags: [math, diffusion, continuous-time]
summary: "The continuous-time mathematical framework unifying score-based and diffusion generative models"
---

# Stochastic Differential Equations

[[sources/song-score-sde-paper]] showed that diffusion models can be described as SDEs: dx = f(x,t)dt + g(t)dw (forward) and the reverse SDE for generation. This unified [[concepts/score-matching]] and [[concepts/diffusion-models]] into one elegant framework.

See also: [[synthesis/diffusion-foundations]]
