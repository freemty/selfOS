---
title: "GPipe: Efficient Training of Giant Neural Networks (Huang et al., 2019)"
type: source
created: 2019-07-08
updated: 2019-07-08
sources: []
tags: [paper, pipeline-parallelism, distributed]
summary: "Micro-batch pipeline parallelism for large model training"
source_type: "paper"
---

# GPipe

[[entities/google-brain]]. Introduced micro-batch [[concepts/pipeline-parallelism]]: split model into stages, pipeline micro-batches to reduce bubble overhead. Foundation for modern [[concepts/distributed-training]] schedules.
