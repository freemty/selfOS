---
title: "AWQ: Activation-aware Weight Quantization (Lin et al., 2023)"
type: source
created: 2023-06-01
updated: 2023-06-01
sources: []
tags: [paper, quantization, inference]
summary: "Activation-aware weight quantization preserving important weights"
source_type: "paper"
---

# AWQ

Showed that a small fraction of weights are critical (determined by activation patterns). Protecting these during [[concepts/quantization]] preserves quality with aggressive compression. Used in [[concepts/inference-optimization]] pipelines alongside [[entities/tensorrt-llm]].
