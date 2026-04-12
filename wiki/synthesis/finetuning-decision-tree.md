---
title: "When to Finetune: LoRA vs. Prompting vs. RAG"
type: synthesis
created: 2026-02-20
updated: 2026-02-20
sources: ["hu-lora-paper"]
tags: [synthesis, decision-framework, finetuning, rag]
summary: "Choosing between prompting, RAG, LoRA, and full finetuning"
---

# Finetuning Decision Tree

1. **Can prompting solve it?** → Yes: stop. No: continue.
2. **Need external knowledge?** → Yes: [[concepts/rag]]. No: continue.
3. **Need behavior change?** → Yes: [[concepts/lora]] or [[concepts/parameter-efficient-finetuning]].
4. **Need fundamental capability?** → Full finetuning or [[concepts/pre-training]].

## Key Insight

Most tasks don't need finetuning. [[concepts/rag]] handles knowledge gaps; good prompting handles most behavior. [[concepts/lora]] ([[sources/hu-lora-paper]]) is for when you truly need to change the model's outputs.

See also: [[concepts/parameter-efficient-finetuning]], [[concepts/quantization]]
