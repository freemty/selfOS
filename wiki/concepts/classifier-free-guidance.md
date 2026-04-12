---
title: "Classifier-Free Guidance"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ho-cfg-paper"]
tags: [diffusion, conditional, guidance]
summary: "Technique to improve conditional generation quality by combining conditional and unconditional predictions"
---

# Classifier-Free Guidance

[[sources/ho-cfg-paper]] introduced a simple trick: jointly train conditional and unconditional [[concepts/diffusion-models]], then at inference, extrapolate away from the unconditional prediction toward the conditional one.

`output = unconditional + guidance_scale × (conditional - unconditional)`

Higher guidance scale = stronger conditioning = higher quality but less diversity. This became essential for text-to-image generation.

See also: [[concepts/conditional-generation]], [[synthesis/diffusion-foundations]]
