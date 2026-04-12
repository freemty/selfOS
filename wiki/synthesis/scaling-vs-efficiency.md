---
title: "Scaling Laws vs. Efficiency: Two Paths to Better Models"
type: synthesis
created: 2026-02-01
updated: 2026-02-01
sources: ["kaplan-scaling-paper", "hoffmann-chinchilla-paper"]
tags: [synthesis, comparison, scaling, efficiency]
summary: "The tension between scaling up and optimizing down — are they complementary?"
---

# Scaling Laws vs. Efficiency

Two approaches to better models:
1. **Scale up**: more parameters, more data, more compute ([[concepts/scaling-laws]])
2. **Optimize down**: [[concepts/quantization]], [[concepts/lora]], [[concepts/mixture-of-experts]]

## Are They Complementary?

Yes. Scale gets you capability; efficiency makes it deployable. [[concepts/chinchilla-optimal]] showed even the scaling path benefits from efficiency thinking (better data use). And efficiency techniques like [[concepts/flash-attention]] *enable* larger scale.

## The Players

- [[entities/openai]], [[entities/anthropic]] — primarily scale-first
- [[entities/meta-ai]] — scale + open-source + efficiency (LLaMA quantized)
- Community — efficiency-first (QLoRA, GGML)

See also: [[concepts/inference-optimization]], [[concepts/parameter-efficient-finetuning]]
