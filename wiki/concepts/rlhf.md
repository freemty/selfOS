---
title: "RLHF"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ouyang-instructgpt-paper"]
tags: [alignment, reinforcement-learning, human-feedback]
summary: "Reinforcement Learning from Human Feedback — the dominant approach to aligning LLMs with human preferences"
---

# RLHF

Reinforcement Learning from Human Feedback, introduced at scale in [[sources/ouyang-instructgpt-paper]] by [[entities/openai]], is the technique that transformed raw language models into useful assistants.

## Pipeline

1. **Supervised finetuning** (SFT) — train on human-written demonstrations
2. **[[concepts/reward-modeling]]** — train a reward model on human preference comparisons
3. **PPO optimization** — optimize the policy against the reward model via [[concepts/ppo-algorithm]]

## Why It Works

Pre-trained models know a lot but don't know what humans *want*. RLHF bridges this gap by encoding human preferences into an optimizable signal. The reward model learns "what sounds good to a human" from pairwise comparisons.

## Limitations

- **Reward hacking** — the model finds exploits in the reward model
- **Human label quality** — garbage preferences in, garbage alignment out
- **Cost** — human labeling is expensive and slow

## Alternatives

- **[[concepts/constitutional-ai]]** — [[entities/anthropic]]'s approach using principles instead of human labels
- **DPO** — direct preference optimization, skipping the reward model entirely
- **RLAIF** — using AI feedback instead of human feedback

See also: [[concepts/alignment]], [[synthesis/alignment-landscape]]
