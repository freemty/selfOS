---
title: "Positional Encoding"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper", "su-rope-paper"]
tags: [transformer, position, sequence-order]
summary: "Injecting sequence order information into transformers — which are otherwise permutation-invariant"
---

# Positional Encoding

The [[concepts/transformer-architecture]] processes all positions in parallel — it has no inherent notion of order. Positional encoding adds this information.

## Evolution

1. **Sinusoidal** (original, [[sources/vaswani-attention-paper]]) — fixed, frequency-based
2. **Learned** — trainable embeddings per position
3. **Relative** — encode distances rather than absolute positions
4. **[[concepts/rope]]** ([[sources/su-rope-paper]]) — rotary embeddings, the current standard

## Why [[concepts/rope]] Won

RoPE encodes relative position through rotation in complex space. It's elegant, efficient, and crucially enables [[concepts/long-context]] extrapolation beyond training length.

See also: [[concepts/attention-mechanism]], [[concepts/long-context]]
