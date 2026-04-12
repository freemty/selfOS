---
title: "Alignment Approaches Compared: RLHF vs. Constitutional AI vs. DPO"
type: synthesis
created: 2026-02-15
updated: 2026-02-15
sources: ["ouyang-instructgpt-paper"]
tags: [synthesis, alignment, comparison]
summary: "Comparing three alignment paradigms — tradeoffs in scalability and robustness"
---

# Alignment Approaches Compared

| Approach | Human Labels? | Reward Model? | Key Player |
|----------|:---:|:---:|---|
| [[concepts/rlhf]] | Yes | Yes | [[entities/openai]] |
| [[concepts/constitutional-ai]] | No | Optional | [[entities/anthropic]] |
| DPO | Yes | No | Community |

## Trade-offs

- **RLHF**: most proven, but expensive (human labels) and fragile (reward hacking)
- **Constitutional AI**: scalable and auditable, but dependent on principle quality
- **DPO**: simple and stable, but less flexible than RL-based methods

All three start from [[concepts/pre-training]] and aim at [[concepts/alignment]].
