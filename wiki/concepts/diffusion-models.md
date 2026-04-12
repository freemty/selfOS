---
title: "Diffusion Models"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ho-ddpm-paper", "song-score-sde-paper"]
tags: [generative-models, denoising, image-generation]
summary: "Generative models that learn to reverse a gradual noising process — state of the art for image generation"
---

# Diffusion Models

Diffusion models generate data by learning to reverse a gradual noising process. Starting from pure noise, they iteratively denoise to produce high-quality samples.

## Two Perspectives

1. **DDPM** ([[sources/ho-ddpm-paper]]) — discrete-time denoising with a simple MSE loss
2. **Score SDE** ([[sources/song-score-sde-paper]]) — continuous-time framework via [[concepts/stochastic-differential-equations]]

Both views are equivalent — the score SDE framework by [[concepts/score-matching]] unified them mathematically.

## Key Techniques

- **[[concepts/classifier-free-guidance]]** — dramatically improves conditional generation quality
- **Noise scheduling** — the choice of noise schedule affects both training and sampling
- **Latent diffusion** — running diffusion in a compressed latent space (Stable Diffusion)

## Connection to ML Systems

Diffusion inference is expensive — hundreds of denoising steps per image. This creates systems challenges similar to LLM serving: batching, [[concepts/quantization]], [[concepts/kernel-fusion]].

See also: [[entities/google-brain]], [[synthesis/diffusion-foundations]]
