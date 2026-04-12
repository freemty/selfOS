---
title: "PPO (Proximal Policy Optimization)"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ouyang-instructgpt-paper"]
tags: [reinforcement-learning, optimization, policy-gradient]
summary: "The RL algorithm used to optimize LLMs against reward models in RLHF"
---

# PPO

Proximal Policy Optimization is the RL algorithm that makes [[concepts/rlhf]] work. It optimizes the policy (the LLM) to maximize the reward model's score while staying close to the original model via a KL penalty.

## Why PPO

- Stable training — clipped objective prevents catastrophic updates
- Sample efficient enough for the LLM setting
- Well-understood failure modes

See also: [[concepts/rlhf]], [[concepts/reward-modeling]]
