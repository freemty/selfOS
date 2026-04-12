---
title: "Reward Modeling"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ouyang-instructgpt-paper"]
tags: [alignment, preferences, rlhf]
summary: "Training a model to predict human preferences — the bridge between human judgment and optimization"
---

# Reward Modeling

A reward model takes a (prompt, response) pair and outputs a scalar score predicting human preference. It's the bridge between subjective human judgment and mathematical optimization in [[concepts/rlhf]].

## Training

Trained on pairwise comparisons: "Is response A or response B better?" Using the Bradley-Terry model to convert comparisons into a scalar reward.

## Challenges

- **Reward hacking** — the policy finds exploits the reward model didn't anticipate
- **Distribution shift** — the reward model was trained on outputs from a different policy
- **Underspecification** — human preferences are noisy and inconsistent

See also: [[concepts/rlhf]], [[concepts/alignment]], [[entities/openai]], [[entities/anthropic]]
