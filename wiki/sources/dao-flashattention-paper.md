---
title: "FlashAttention: Fast and Memory-Efficient Exact Attention (Dao, 2022)"
type: source
created: 2022-05-27
updated: 2022-05-27
sources: []
tags: [paper, flash-attention, gpu, io-aware]
summary: "IO-aware exact attention respecting GPU memory hierarchy"
source_type: "paper"
---

# FlashAttention

[[entities/tri-dao]]'s paper that proved you don't need to approximate attention — you need to respect [[concepts/gpu-memory-hierarchy]]. Tiling + online softmax keeps computation in SRAM, avoiding O(N²) HBM writes. The canonical example of hardware-aware algorithm design.

See also: [[concepts/flash-attention]], [[concepts/attention-mechanism]], [[concepts/kernel-fusion]]
