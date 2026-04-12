---
title: "Rotary Position Embedding (RoPE)"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["su-rope-paper"]
tags: [position-encoding, rotation, long-context]
summary: "Position encoding via rotation in complex space — enables length extrapolation"
---

# RoPE

RoPE ([[sources/su-rope-paper]]) encodes position by rotating query and key vectors in complex space. The dot product between rotated vectors naturally encodes relative position.

## Why It's Elegant

- Relative position falls out of the math — no explicit relative position computation
- Works with any attention variant including [[concepts/flash-attention]]
- Enables [[concepts/long-context]] via frequency scaling (NTK-aware, YaRN)

## Adoption

Nearly all modern LLMs use RoPE: LLaMA ([[entities/meta-ai]]), Mistral, Qwen, etc. It replaced both learned and sinusoidal [[concepts/positional-encoding]].

See also: [[concepts/transformer-architecture]], [[concepts/attention-mechanism]]
