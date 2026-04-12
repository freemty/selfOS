---
title: "Speculative Decoding"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["leviathan-speculative-paper"]
tags: [inference, speed, autoregressive]
summary: "Using a small draft model to propose tokens verified by the large model — parallelizes autoregressive generation"
---

# Speculative Decoding

[[sources/leviathan-speculative-paper]] introduced a simple insight: use a small, fast "draft" model to propose K tokens, then verify all K in a single forward pass of the large model. Accepted tokens are free; rejected tokens cost one extra step.

## Why It Works

Large model forward passes are memory-bandwidth-bound, not compute-bound. Verifying K tokens costs nearly the same as generating 1. If the draft model has high acceptance rate, you get ~2-3x speedup.

## Connection to [[concepts/inference-optimization]]

Speculative decoding composes well with [[concepts/quantization]], [[concepts/kv-cache]], and [[concepts/flash-attention]]. It's a system-level optimization that sits on top of kernel-level ones.

See also: [[concepts/autoregressive-generation]], [[synthesis/serving-stack-2026]]
