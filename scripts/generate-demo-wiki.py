#!/usr/bin/env python3
"""Generate ~90 demo wiki nodes with dense cross-references."""
from pathlib import Path

WIKI = Path.home() / "selfOS" / "wiki"

def write_page(subdir, slug, content):
    d = WIKI / subdir
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{slug}.md"
    if p.exists():
        return False
    p.write_text(content, encoding="utf-8")
    return True

# ============================================================
# CONCEPTS (40)
# ============================================================
CONCEPTS = {
"transformer-architecture": """---
title: "Transformer Architecture"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper"]
tags: [architecture, deep-learning, nlp]
summary: "The dominant neural network architecture based on self-attention — replaced RNNs for sequence modeling"
---

# Transformer Architecture

The Transformer, introduced in [[sources/vaswani-attention-paper]], fundamentally changed how we process sequences. By replacing recurrence with [[concepts/attention-mechanism]], it enabled massive parallelization during training and set the stage for the scaling era.

## Core Components

1. **Multi-head self-attention** — the core innovation (see [[concepts/attention-mechanism]])
2. **[[concepts/positional-encoding]]** — injecting sequence order into a permutation-invariant architecture
3. **Feed-forward networks** — per-position nonlinear transformations
4. **Layer normalization + residual connections** — training stability

## Why It Won

The Transformer's parallelizability unlocked [[concepts/scaling-laws]]: once you can train efficiently on thousands of GPUs via [[concepts/distributed-training]], the path to billion-parameter models opens. [[entities/google-brain]] showed this first; [[entities/openai]] took it furthest.

## Variants and Extensions

- [[concepts/mixture-of-experts]] — sparse activation for massive capacity
- [[concepts/flash-attention]] — hardware-aware exact attention ([[entities/tri-dao]])
- [[concepts/rope]] — modern positional encoding for [[concepts/long-context]]

The architecture has proven remarkably robust. Most improvements since 2017 are about *training it better* ([[concepts/scaling-laws]], [[concepts/pre-training]]) or *serving it faster* ([[concepts/inference-optimization]]), not changing the core design.
""",

"attention-mechanism": """---
title: "Attention Mechanism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper", "dao-flashattention-paper"]
tags: [attention, self-attention, multi-head]
summary: "Weighted aggregation over input tokens — the core building block of transformers"
---

# Attention Mechanism

Attention computes a weighted sum over values, where weights are derived from query-key similarity. In self-attention, queries, keys, and values all come from the same sequence.

## The Math

`Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V`

This simple formula is the heart of the [[concepts/transformer-architecture]]. The softmax creates a probability distribution over positions, allowing each token to "attend to" relevant context.

## Computational Challenge

Standard attention is O(N²) in sequence length — both compute and memory. This bottleneck drove two lines of work:
1. **Approximation**: sparse attention, linear attention — trade accuracy for speed
2. **[[concepts/flash-attention]]**: keep exact attention, but respect [[concepts/gpu-memory-hierarchy]] — [[entities/tri-dao]]'s insight

The second approach won. [[concepts/flash-attention]] proved you don't need to approximate if you understand the hardware.

## In Practice

- **[[concepts/kv-cache]]** — caching keys/values across autoregressive steps
- **Multi-head attention** — parallel attention with different learned projections
- **Cross-attention** — queries from one sequence, keys/values from another (used in [[concepts/conditional-generation]])

See also: [[sources/vaswani-attention-paper]], [[sources/dao-flashattention-paper]]
""",

"scaling-laws": """---
title: "Scaling Laws"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["kaplan-scaling-paper", "hoffmann-chinchilla-paper"]
tags: [scaling, compute, power-law]
summary: "Empirical power-law relationships between model size, data, compute, and loss"
---

# Scaling Laws

[[sources/kaplan-scaling-paper]] first showed that language model loss follows smooth power laws as functions of model size (N), dataset size (D), and compute budget (C). This was transformative: it meant you could *predict* performance before training.

## Key Findings

1. **Power-law scaling** — loss ∝ N^{-α} for fixed data, loss ∝ D^{-β} for fixed model size
2. **Compute-optimal allocation** — for a fixed compute budget, there's an optimal balance between N and D
3. **[[concepts/chinchilla-optimal]]** — [[entities/deepmind]]'s refinement showing most models were undertrained

## Impact

Scaling laws turned LLM development from art into engineering. [[entities/openai]] used them to plan GPT-4; every major lab now has internal scaling law fits.

They also opened philosophical questions: if bigger = better on a predictable curve, is [[concepts/pre-training]] just about throwing compute at the problem? The answer is nuanced — [[concepts/data-efficiency]] and architecture choices still matter, but scale is the dominant variable.

## Connections

- [[concepts/distributed-training]] — the infrastructure that makes scale possible
- [[concepts/mixture-of-experts]] — a way to scale parameters without proportional compute
- [[concepts/emergent-abilities]] — capabilities that appear only at sufficient scale
- [[synthesis/scaling-vs-efficiency]] — the tension between scaling up and optimizing down
""",

"flash-attention": """---
title: "Flash Attention"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["dao-flashattention-paper"]
tags: [attention, gpu, io-aware, memory-hierarchy]
summary: "IO-aware exact attention algorithm — makes long-context practical by respecting GPU memory hierarchy"
---

# Flash Attention

Created by [[entities/tri-dao]], FlashAttention (source: [[sources/dao-flashattention-paper]]) is the canonical example of hardware-aware algorithm design. The insight: standard attention isn't compute-bound — it's **memory-bound**. The O(N²) attention matrix writes to slow HBM when it could stay in fast SRAM.

## Core Technique: Tiling + Online Softmax

1. Load blocks of Q, K, V into SRAM
2. Compute attention incrementally using the online softmax trick
3. Never materialize the full N×N attention matrix in HBM

Result: same exact attention, but IO-complexity drops from O(N²) to O(N² d² M⁻¹).

## Why It Matters

- Enables [[concepts/long-context]] — 100K+ token windows become practical
- **Exact**, not approximate — unlike sparse/linear attention variants
- Made [[concepts/attention-mechanism]] fast enough that alternatives lost their appeal

## Broader Lesson

FlashAttention demonstrates that understanding [[concepts/gpu-memory-hierarchy]] can yield bigger speedups than algorithmic approximation. This is the core thesis of ML systems research: the hardware matters as much as the math.

See also: [[concepts/kernel-fusion]], [[concepts/inference-optimization]], [[entities/nvidia]]
""",

"rlhf": """---
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
""",

"diffusion-models": """---
title: "Diffusion Models"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ho-ddpm-paper", "song-score-sde-paper"]
tags: [generative-models, denoising, image-generation]
summary: "Generative models that learn to reverse a gradual noising process — state of the art for image generation"
---

# Diffusion Models

Diffusion models generate data by learning to reverse a gradual noising process. Starting from pure noise, they iteratively denoise to produce high-quality samples.

## Two Perspectives

1. **DDPM** ([[sources/ho-ddpm-paper]]) — discrete-time denoising with a simple MSE loss
2. **Score SDE** ([[sources/song-score-sde-paper]]) — continuous-time framework via [[concepts/stochastic-differential-equations]]

Both views are equivalent — the score SDE framework by [[concepts/score-matching]] unified them mathematically.

## Key Techniques

- **[[concepts/classifier-free-guidance]]** — dramatically improves conditional generation quality
- **Noise scheduling** — the choice of noise schedule affects both training and sampling
- **Latent diffusion** — running diffusion in a compressed latent space (Stable Diffusion)

## Connection to ML Systems

Diffusion inference is expensive — hundreds of denoising steps per image. This creates systems challenges similar to LLM serving: batching, [[concepts/quantization]], [[concepts/kernel-fusion]].

See also: [[entities/google-brain]], [[synthesis/diffusion-foundations]]
""",

"lora": """---
title: "LoRA"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hu-lora-paper"]
tags: [finetuning, low-rank, parameter-efficient]
summary: "Low-Rank Adaptation — efficient finetuning by injecting trainable low-rank matrices into frozen pretrained weights"
---

# LoRA

LoRA (Low-Rank Adaptation), from [[sources/hu-lora-paper]] by [[entities/microsoft]], made finetuning billion-parameter models practical. Instead of updating all weights, inject small trainable low-rank matrices: W' = W + BA, where B ∈ R^{d×r} and A ∈ R^{r×d} with r << d.

## Why It Works

The key hypothesis: the weight updates during finetuning have low intrinsic rank. You don't need full-rank updates to adapt a pretrained model to a new task.

## Practical Impact

- **Memory**: train a 7B model on a single consumer GPU
- **Storage**: swap tasks by swapping small adapter files (~MB vs GB)
- **Speed**: fewer trainable parameters = faster training

## Extensions

- **QLoRA** ([[sources/dettmers-qlora-paper]]) — combine with [[concepts/quantization]] for even lower memory
- **Adapter methods** — broader family of [[concepts/parameter-efficient-finetuning]] techniques

See also: [[concepts/pre-training]], [[synthesis/finetuning-decision-tree]]
""",

"distributed-training": """---
title: "Distributed Training"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [training, parallelism, infrastructure]
summary: "Training models across multiple GPUs or nodes — essential for billion-parameter scale"
---

# Distributed Training

Training billion-parameter models requires distributing work across many GPUs. This is not just "run the same thing on more machines" — it's a deep systems problem involving communication, memory, and scheduling.

## Four Forms of Parallelism

1. **[[concepts/data-parallelism]]** — replicate model, split data. Simplest. Scales well until model doesn't fit in one GPU.
2. **[[concepts/tensor-parallelism]]** — split individual matrix operations across GPUs. Intra-layer. High communication.
3. **[[concepts/pipeline-parallelism]]** — split layers across stages. Inter-layer. Bubble overhead.
4. **[[concepts/model-parallelism]]** — umbrella term for tensor + pipeline parallelism.

Modern systems like [[entities/megatron-lm]] use **3D parallelism**: all three combined.

## Key Infrastructure

- **[[entities/pytorch]]** — DDP for data parallelism, FSDP for sharded data parallelism
- **[[entities/deepspeed]]** — ZeRO optimizer sharding
- **[[entities/nvidia]]** — NCCL for GPU collective communication
- **[[entities/megatron-lm]]** — NVIDIA's 3D parallelism framework

## The Communication Bottleneck

Every form of parallelism introduces communication overhead. The art is choosing the right strategy for your model size, cluster topology, and interconnect bandwidth.

See also: [[concepts/scaling-laws]], [[synthesis/parallelism-taxonomy]]
""",

"inference-optimization": """---
title: "Inference Optimization"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [serving, throughput, latency, optimization]
summary: "Techniques to make LLM serving faster and cheaper — from kernel-level to system-level optimizations"
---

# Inference Optimization

Serving LLMs at scale is a systems problem. A single GPT-4 query can cost cents — at millions of queries per day, optimization is existential.

## The Stack

From bottom to top:
1. **Hardware**: [[concepts/gpu-memory-hierarchy]], HBM bandwidth, interconnect
2. **Kernels**: [[concepts/flash-attention]], [[concepts/kernel-fusion]]
3. **Runtime**: [[concepts/kv-cache]] management, continuous batching
4. **Algorithm**: [[concepts/speculative-decoding]], [[concepts/quantization]]
5. **System**: [[entities/vllm]], [[entities/tensorrt-llm]]

## Key Techniques

- **[[concepts/kv-cache]]** + PagedAttention ([[entities/vllm]]) — avoid recomputation, manage memory like an OS
- **[[concepts/quantization]]** — INT8/INT4 weights, less memory, faster matmuls
- **[[concepts/speculative-decoding]]** — small model drafts, large model verifies
- **Continuous batching** — process new requests without waiting for batch completion

## The Economics

Every 2x speedup halves serving cost. This is why [[entities/nvidia]] GPUs, [[concepts/flash-attention]], and [[entities/vllm]] are so impactful — they compound.

See also: [[synthesis/serving-stack-2026]]
""",

"quantization": """---
title: "Quantization"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["dettmers-qlora-paper", "lin-awq-paper"]
tags: [efficiency, compression, inference]
summary: "Reducing numerical precision of model weights to decrease memory and compute requirements"
---

# Quantization

Quantization reduces model weights from FP16/BF16 to INT8, INT4, or even lower precision. This directly reduces memory footprint and can speed up computation.

## Approaches

- **Post-training quantization (PTQ)** — quantize after training, no retraining needed
- **Quantization-aware training (QAT)** — train with quantization in the loop
- **AWQ** ([[sources/lin-awq-paper]]) — activation-aware weight quantization, preserves important weights
- **GPTQ** — one-shot weight quantization using approximate second-order information

## Combination with Finetuning

QLoRA ([[sources/dettmers-qlora-paper]]) showed that 4-bit quantized models can be effectively finetuned with [[concepts/lora]], making 65B models trainable on a single 48GB GPU.

## Trade-offs

More aggressive quantization = more memory savings but potential quality degradation. The sweet spot for most LLMs is INT4 for weights, FP16 for activations.

See also: [[concepts/inference-optimization]], [[concepts/parameter-efficient-finetuning]], [[entities/tensorrt-llm]]
""",

"kv-cache": """---
title: "KV Cache"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [inference, memory, attention, serving]
summary: "Caching key-value pairs across autoregressive decoding steps to avoid redundant computation"
---

# KV Cache

During [[concepts/autoregressive-generation]], each new token attends to all previous tokens. Without caching, this means recomputing all key-value pairs at every step — O(N²) total work for N tokens.

The KV cache stores computed key-value pairs, reducing each step to O(N) — a massive speedup.

## The Memory Problem

KV cache memory grows linearly with sequence length and batch size. For long-context models ([[concepts/long-context]]), it can dominate GPU memory.

## PagedAttention

[[entities/vllm]] introduced PagedAttention: manage KV cache like virtual memory with pages. This eliminates fragmentation and enables efficient memory sharing across requests.

## Connection to System Design

KV cache management is where [[concepts/attention-mechanism]] meets operating systems. The abstraction of paged memory, originally from OS design, turns out to be exactly right for LLM serving.

See also: [[concepts/inference-optimization]], [[concepts/flash-attention]], [[synthesis/serving-stack-2026]]
""",

"chinchilla-optimal": """---
title: "Chinchilla Optimal Training"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hoffmann-chinchilla-paper"]
tags: [scaling, data-efficiency, compute-optimal]
summary: "Training regime that balances model size and data quantity for fixed compute budget"
---

# Chinchilla Optimal Training

[[entities/deepmind]]'s Chinchilla paper ([[sources/hoffmann-chinchilla-paper]]) showed that most LLMs were significantly undertrained. For a fixed compute budget, the optimal strategy trains a *smaller* model on *more data* than the prevailing practice.

## The Rule of Thumb

Tokens ≈ 20× parameters. A 7B model should see ~140B tokens. GPT-3 (175B params) was trained on only 300B tokens — Chinchilla says it should have seen ~3.5T tokens.

## Impact

This insight redirected the field toward [[concepts/data-efficiency]]. Suddenly, data quality and quantity mattered as much as model size. It also made smaller, well-trained models competitive with larger undertrained ones.

See also: [[concepts/scaling-laws]], [[concepts/pre-training]], [[synthesis/scaling-vs-efficiency]]
""",

"reward-modeling": """---
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
""",

"alignment": """---
title: "AI Alignment"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [safety, alignment, values]
summary: "Ensuring AI systems behave in accordance with human values and intentions"
---

# AI Alignment

The challenge of making AI systems do what humans actually want, not just what they're literally told. As models become more capable, alignment becomes more critical.

## Current Approaches

1. **[[concepts/rlhf]]** — learning from human preference data ([[entities/openai]])
2. **[[concepts/constitutional-ai]]** — self-improvement from principles ([[entities/anthropic]])
3. **DPO** — direct preference optimization without a separate reward model

## The Hard Problem

Current alignment techniques work for current models. Whether they'll scale to much more capable systems is an open question — the core concern of [[entities/anthropic]] and the alignment research community.

See also: [[concepts/reward-modeling]], [[synthesis/alignment-landscape]]
""",

"constitutional-ai": """---
title: "Constitutional AI"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [alignment, safety, anthropic, self-improvement]
summary: "Anthropic's approach to alignment using principles for self-improvement without human labels"
---

# Constitutional AI

Developed by [[entities/anthropic]], Constitutional AI replaces human preference labels with a set of principles (a "constitution"). The model critiques and revises its own outputs based on these principles.

## How It Works

1. Generate responses
2. Ask the model to critique its response against the constitution
3. Ask the model to revise based on the critique
4. Train on the revised outputs

This is a form of [[concepts/self-critique]] — the model improves itself using explicit principles rather than implicit human preferences.

## Advantage Over [[concepts/rlhf]]

- **Scalable** — no human labelers needed per example
- **Transparent** — the principles are explicit and auditable
- **Controllable** — change behavior by changing the constitution

See also: [[concepts/alignment]], [[synthesis/alignment-landscape]]
""",

"mixture-of-experts": """---
title: "Mixture of Experts"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["shazeer-moe-paper"]
tags: [architecture, sparse, routing, scaling]
summary: "Architecture where only a subset of parameters activate per input — massive models with manageable compute"
---

# Mixture of Experts

MoE ([[sources/shazeer-moe-paper]]) replaces the dense feed-forward layer with multiple "expert" sub-networks and a routing mechanism that selects top-K experts per token.

## Why It Matters

MoE decouples model capacity from compute cost. A 1T parameter MoE model might only use 100B parameters per token — giving the knowledge of a huge model at the cost of a smaller one.

## Systems Challenges

- **Load balancing** — ensuring all experts get roughly equal traffic
- **Communication** — expert parallelism across GPUs requires all-to-all communication
- **Memory** — all expert weights must be in memory even if sparsely used

## Examples

- GShard, Switch Transformer ([[entities/google-brain]])
- Mixtral (Mistral AI)
- DeepSeek-V3

See also: [[concepts/transformer-architecture]], [[concepts/scaling-laws]], [[concepts/distributed-training]]
""",

"positional-encoding": """---
title: "Positional Encoding"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper", "su-rope-paper"]
tags: [transformer, position, sequence-order]
summary: "Injecting sequence order information into transformers — which are otherwise permutation-invariant"
---

# Positional Encoding

The [[concepts/transformer-architecture]] processes all positions in parallel — it has no inherent notion of order. Positional encoding adds this information.

## Evolution

1. **Sinusoidal** (original, [[sources/vaswani-attention-paper]]) — fixed, frequency-based
2. **Learned** — trainable embeddings per position
3. **Relative** — encode distances rather than absolute positions
4. **[[concepts/rope]]** ([[sources/su-rope-paper]]) — rotary embeddings, the current standard

## Why [[concepts/rope]] Won

RoPE encodes relative position through rotation in complex space. It's elegant, efficient, and crucially enables [[concepts/long-context]] extrapolation beyond training length.

See also: [[concepts/attention-mechanism]], [[concepts/long-context]]
""",

"rope": """---
title: "Rotary Position Embedding (RoPE)"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["su-rope-paper"]
tags: [position-encoding, rotation, long-context]
summary: "Position encoding via rotation in complex space — enables length extrapolation"
---

# RoPE

RoPE ([[sources/su-rope-paper]]) encodes position by rotating query and key vectors in complex space. The dot product between rotated vectors naturally encodes relative position.

## Why It's Elegant

- Relative position falls out of the math — no explicit relative position computation
- Works with any attention variant including [[concepts/flash-attention]]
- Enables [[concepts/long-context]] via frequency scaling (NTK-aware, YaRN)

## Adoption

Nearly all modern LLMs use RoPE: LLaMA ([[entities/meta-ai]]), Mistral, Qwen, etc. It replaced both learned and sinusoidal [[concepts/positional-encoding]].

See also: [[concepts/transformer-architecture]], [[concepts/attention-mechanism]]
""",

"long-context": """---
title: "Long Context"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [context-window, attention, scaling]
summary: "Extending transformer context windows beyond training length — a systems and algorithms co-design challenge"
---

# Long Context

Extending context from 2K → 128K+ tokens requires solving problems at every level:

## Algorithm

- **[[concepts/rope]]** scaling — NTK-aware interpolation, YaRN
- **[[concepts/flash-attention]]** — makes long-context attention practical
- Sparse attention patterns for ultra-long contexts

## Systems

- **[[concepts/kv-cache]]** management — memory grows linearly with context
- [[concepts/inference-optimization]] — longer contexts = more compute per token

## Who's Leading

[[entities/anthropic]] (Claude 200K), [[entities/openai]] (GPT-4 128K), Google (Gemini 1M). The race is both algorithmic and infrastructural.

See also: [[concepts/attention-mechanism]], [[synthesis/serving-stack-2026]]
""",

"pre-training": """---
title: "Pre-training"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["kaplan-scaling-paper"]
tags: [training, next-token-prediction, foundation]
summary: "Training on massive unlabeled corpora to learn general representations before task-specific finetuning"
---

# Pre-training

Pre-training is the first and most expensive phase of building an LLM. The model learns to predict the next token on trillions of tokens from the internet.

## Why Next-Token Prediction Works

Predicting the next token forces the model to learn syntax, semantics, facts, reasoning patterns, and even common sense. It's [[concepts/self-supervised-learning]] at its most elegant.

## Scale Requirements

Modern pre-training requires:
- Trillions of tokens ([[concepts/chinchilla-optimal]])
- Thousands of GPUs ([[concepts/distributed-training]])
- Months of training time
- Millions of dollars in compute

## After Pre-training

Raw pre-trained models are capable but not useful. They need:
- [[concepts/rlhf]] or [[concepts/constitutional-ai]] for alignment
- [[concepts/lora]] or [[concepts/parameter-efficient-finetuning]] for task adaptation

See also: [[concepts/scaling-laws]], [[entities/openai]], [[entities/meta-ai]]
""",

"data-parallelism": """---
title: "Data Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [distributed, training, parallelism]
summary: "Splitting training data across devices while replicating the model — the simplest form of distributed training"
---

# Data Parallelism

The simplest [[concepts/distributed-training]] strategy: replicate the full model on every GPU, split the data batch. Each GPU computes gradients on its shard, then gradients are synchronized via allreduce.

## Variants

- **DDP** ([[entities/pytorch]]) — vanilla allreduce after each backward pass
- **FSDP** — shard optimizer states and weights across GPUs (ZeRO-style)
- **[[entities/deepspeed]] ZeRO** — progressive sharding of optimizer/gradients/parameters

## When to Use

Data parallelism is the default choice when the model fits in one GPU's memory. When it doesn't, you need [[concepts/model-parallelism]].

See also: [[concepts/tensor-parallelism]], [[concepts/pipeline-parallelism]], [[synthesis/parallelism-taxonomy]]
""",

"model-parallelism": """---
title: "Model Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [distributed, training, parallelism]
summary: "Splitting the model itself across devices — necessary when models exceed single-GPU memory"
---

# Model Parallelism

When a model doesn't fit in one GPU, you split it across multiple GPUs. Two main approaches:

1. **[[concepts/tensor-parallelism]]** — split individual operations (intra-layer)
2. **[[concepts/pipeline-parallelism]]** — split layers across stages (inter-layer)

## Trade-offs

Tensor parallelism has high communication but no bubble overhead. Pipeline parallelism has lower communication but wastes compute in bubbles. [[entities/megatron-lm]] combines both in 3D parallelism.

See also: [[concepts/distributed-training]], [[concepts/data-parallelism]], [[synthesis/parallelism-taxonomy]]
""",

"pipeline-parallelism": """---
title: "Pipeline Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["gpipe-paper"]
tags: [distributed, training, pipeline]
summary: "Splitting model layers across stages that process micro-batches in pipeline fashion"
---

# Pipeline Parallelism

Split the model into stages (groups of layers), each on a different GPU. Micro-batches flow through the pipeline, keeping all stages busy.

## The Bubble Problem

When the pipeline starts and drains, some stages are idle — the "pipeline bubble." [[sources/gpipe-paper]] introduced micro-batching to minimize this. Modern schedules (1F1B, interleaved) reduce bubbles further.

## When to Use

Pipeline parallelism shines for very deep models across nodes with limited inter-node bandwidth. Combine with [[concepts/tensor-parallelism]] for intra-node and [[concepts/data-parallelism]] for scaling across groups.

See also: [[concepts/model-parallelism]], [[entities/megatron-lm]], [[synthesis/parallelism-taxonomy]]
""",

"tensor-parallelism": """---
title: "Tensor Parallelism"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [distributed, training, parallelism]
summary: "Splitting individual tensor operations across devices — intra-layer parallelism for large matrices"
---

# Tensor Parallelism

Split large matrix multiplications across GPUs. For a linear layer Y = XW, split W column-wise across GPUs, compute partial results, then combine.

## In [[entities/megatron-lm]]

Column-parallel and row-parallel linear layers alternate, minimizing communication. Each attention head can be placed on a separate GPU.

## Requirements

High-bandwidth interconnect (NVLink) — tensor parallelism communicates every layer. Only practical within a single node.

See also: [[concepts/model-parallelism]], [[concepts/pipeline-parallelism]], [[concepts/distributed-training]], [[entities/nvidia]]
""",

"speculative-decoding": """---
title: "Speculative Decoding"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["leviathan-speculative-paper"]
tags: [inference, speed, autoregressive]
summary: "Using a small draft model to propose tokens verified by the large model — parallelizes autoregressive generation"
---

# Speculative Decoding

[[sources/leviathan-speculative-paper]] introduced a simple insight: use a small, fast "draft" model to propose K tokens, then verify all K in a single forward pass of the large model. Accepted tokens are free; rejected tokens cost one extra step.

## Why It Works

Large model forward passes are memory-bandwidth-bound, not compute-bound. Verifying K tokens costs nearly the same as generating 1. If the draft model has high acceptance rate, you get ~2-3x speedup.

## Connection to [[concepts/inference-optimization]]

Speculative decoding composes well with [[concepts/quantization]], [[concepts/kv-cache]], and [[concepts/flash-attention]]. It's a system-level optimization that sits on top of kernel-level ones.

See also: [[concepts/autoregressive-generation]], [[synthesis/serving-stack-2026]]
""",

"gpu-memory-hierarchy": """---
title: "GPU Memory Hierarchy"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["dao-flashattention-paper"]
tags: [hardware, gpu, memory, bandwidth]
summary: "The layered memory system in GPUs — understanding it is key to writing efficient ML kernels"
---

# GPU Memory Hierarchy

Understanding this hierarchy is what separates efficient from naive GPU code:

| Level | Size | Bandwidth | Latency |
|-------|------|-----------|---------|
| Registers | ~256KB/SM | — | 0 cycles |
| SRAM (shared memory) | ~100-228KB/SM | ~19 TB/s | ~30 cycles |
| L2 Cache | ~40-50MB | ~6 TB/s | ~200 cycles |
| HBM (global memory) | 40-80GB | ~2-3 TB/s | ~400 cycles |

## The Insight Behind [[concepts/flash-attention]]

[[entities/tri-dao]] realized that standard attention writes O(N²) data to HBM when the computation could stay in SRAM. Respecting this hierarchy gave a 2-4x speedup with no approximation.

## Implications for ML Systems

Most ML operations are memory-bound, not compute-bound. [[concepts/kernel-fusion]] and tiling ([[concepts/triton-compiler]]) are about keeping data in fast memory.

See also: [[entities/nvidia]], [[concepts/inference-optimization]]
""",

"kernel-fusion": """---
title: "Kernel Fusion"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [gpu, optimization, fusion, memory]
summary: "Combining multiple GPU operations into a single kernel to reduce memory traffic and launch overhead"
---

# Kernel Fusion

Each GPU kernel launch reads inputs from HBM and writes outputs back to HBM. If two operations are chained (e.g., matmul → activation → layernorm), fusing them into one kernel avoids intermediate HBM reads/writes.

## Why It Matters

For memory-bound operations (which most ML ops are), fusion can give 2-5x speedups by reducing [[concepts/gpu-memory-hierarchy]] traffic.

## Tools

- **[[concepts/triton-compiler]]** — write fused kernels in Python-like DSL
- **[[entities/tensorrt-llm]]** — automatic fusion for inference
- **torch.compile** ([[entities/pytorch]]) — JIT fusion

See also: [[concepts/flash-attention]], [[concepts/inference-optimization]]
""",

"triton-compiler": """---
title: "Triton"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["tillet-triton-paper"]
tags: [compiler, gpu, dsl, kernel]
summary: "Python-like DSL for writing GPU kernels — lowers the barrier to custom CUDA programming"
---

# Triton

[[sources/tillet-triton-paper]], from [[entities/openai]], introduced Triton: a Python-like language for writing GPU kernels. Instead of managing threads and shared memory manually (CUDA), you think in terms of blocks and let the compiler handle the rest.

## Impact

Triton democratized GPU programming for ML researchers. [[concepts/flash-attention]] was prototyped in Triton. Custom [[concepts/kernel-fusion]] became accessible without deep CUDA expertise.

See also: [[concepts/gpu-memory-hierarchy]], [[entities/nvidia]], [[synthesis/gpu-programming-landscape]]
""",

"rag": """---
title: "Retrieval-Augmented Generation"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["lewis-rag-paper"]
tags: [retrieval, generation, knowledge]
summary: "Augmenting LLM generation with retrieved documents — reduces hallucination and enables knowledge updates"
---

# RAG

RAG ([[sources/lewis-rag-paper]], [[entities/meta-ai]]) combines a retriever with a generator. Given a query, retrieve relevant documents from a knowledge base, then generate an answer conditioned on both the query and retrieved context.

## Why RAG

- **Reduces hallucination** — ground generation in real documents
- **Updatable knowledge** — change the document store, no retraining needed
- **Auditable** — you can see which documents informed the answer

## Architecture

1. **Embedding** — encode documents with [[concepts/embedding-models]]
2. **Index** — store in [[concepts/vector-databases]] ([[entities/pinecone]], [[entities/chromadb]])
3. **Retrieve** — find top-K relevant documents
4. **Generate** — condition the LLM on query + retrieved documents

See also: [[synthesis/rag-architecture-patterns]], [[synthesis/finetuning-decision-tree]]
""",

"embedding-models": """---
title: "Embedding Models"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [embeddings, similarity, retrieval]
summary: "Models that map text to dense vectors — the backbone of semantic search and retrieval systems"
---

# Embedding Models

Embedding models encode text into dense vectors where semantic similarity corresponds to vector proximity. They power [[concepts/rag]], semantic search, and clustering.

## Training

Trained via [[concepts/contrastive-learning]] on (query, positive_doc, negative_doc) triplets. The model learns to pull matching pairs together and push non-matching pairs apart.

## Key Players

- [[entities/openai]] — text-embedding-3 series
- [[entities/cohere]] — Embed v3
- Sentence-BERT, E5, BGE — open-source options

## Infrastructure

Vectors need specialized storage: [[concepts/vector-databases]] like [[entities/pinecone]] and [[entities/chromadb]] provide ANN search at scale.

See also: [[concepts/rag]], [[synthesis/rag-architecture-patterns]]
""",

"vector-databases": """---
title: "Vector Databases"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [database, vectors, search, infrastructure]
summary: "Specialized databases for storing and querying high-dimensional vectors — infrastructure for RAG systems"
---

# Vector Databases

Vector databases store dense embeddings and support approximate nearest neighbor (ANN) search. They're the infrastructure layer for [[concepts/rag]] and semantic search.

## Core Algorithms

- **HNSW** — hierarchical navigable small world graphs (most popular)
- **IVF** — inverted file index for large-scale search
- **Product quantization** — compress vectors for memory efficiency

## Key Tools

- [[entities/pinecone]] — managed, production-focused
- [[entities/chromadb]] — open-source, prototyping-friendly

See also: [[concepts/embedding-models]], [[synthesis/rag-architecture-patterns]]
""",

"contrastive-learning": """---
title: "Contrastive Learning"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["chen-simclr-paper"]
tags: [self-supervised, representation-learning]
summary: "Learning representations by pulling similar pairs together and pushing dissimilar pairs apart"
---

# Contrastive Learning

[[sources/chen-simclr-paper]] showed that contrastive learning — simple positive/negative pair training — could match supervised performance on ImageNet.

## Core Idea

Given an anchor, pull positive examples closer in embedding space, push negatives away. The InfoNCE loss formalizes this.

## Impact

Contrastive learning is the foundation of:
- [[concepts/embedding-models]] — how text embeddings are trained
- [[concepts/self-supervised-learning]] — learning without labels
- Vision-language models (CLIP) — aligning images and text

See also: [[entities/meta-ai]], [[entities/google-brain]]
""",

"self-supervised-learning": """---
title: "Self-Supervised Learning"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["chen-simclr-paper"]
tags: [pretext-task, representation, foundation]
summary: "Learning from unlabeled data by creating supervision from the data itself"
---

# Self-Supervised Learning

SSL creates supervisory signals from the data structure itself. No human labels needed.

## Forms

- **Next-token prediction** — [[concepts/pre-training]] for LLMs
- **Masked language modeling** — BERT-style
- **[[concepts/contrastive-learning]]** — SimCLR, MoCo for vision
- **Masked image modeling** — MAE for vision transformers

## Why It Matters

SSL is what makes foundation models possible. [[entities/meta-ai]]'s Yann LeCun ([[entities/yann-lecun]]) calls it "the dark matter of intelligence" — the bulk of what models learn comes from self-supervision, not from labeled examples.

See also: [[concepts/pre-training]], [[synthesis/ssl-to-foundation]]
""",

"score-matching": """---
title: "Score-Based Models"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["song-score-sde-paper"]
tags: [generative, score-function, sde]
summary: "Learning the gradient of the log-probability — a unified framework for diffusion and score-based generation"
---

# Score-Based Models

Score matching learns the score function ∇_x log p(x) — the gradient of the log-probability. Once you have the score, you can generate samples via Langevin dynamics.

## Unification with Diffusion

[[sources/song-score-sde-paper]] showed that DDPM ([[sources/ho-ddpm-paper]]) and score-based models are two views of the same framework, connected through [[concepts/stochastic-differential-equations]].

See also: [[concepts/diffusion-models]], [[synthesis/diffusion-foundations]]
""",

"classifier-free-guidance": """---
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
""",

"parameter-efficient-finetuning": """---
title: "Parameter-Efficient Finetuning"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hu-lora-paper", "dettmers-qlora-paper"]
tags: [finetuning, efficiency, adaptation]
summary: "Methods to adapt large models with minimal trainable parameters"
---

# Parameter-Efficient Finetuning

Updating all parameters of a billion-parameter model is expensive. PEFT methods freeze most weights and only train a small subset.

## Methods

- **[[concepts/lora]]** — low-rank matrices ([[sources/hu-lora-paper]])
- **Adapters** — small bottleneck modules between layers
- **Prompt tuning** — learnable soft prompts
- **QLoRA** — [[concepts/lora]] + [[concepts/quantization]] ([[sources/dettmers-qlora-paper]])

See also: [[concepts/pre-training]], [[synthesis/finetuning-decision-tree]]
""",

"autoregressive-generation": """---
title: "Autoregressive Generation"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [inference, generation, next-token]
summary: "Generating text token by token, conditioned on all previous tokens"
---

# Autoregressive Generation

LLMs generate text one token at a time. Each token is sampled from P(x_t | x_1, ..., x_{t-1}), making generation inherently sequential.

## The Bottleneck

Sequential generation means latency scales linearly with output length. Key optimizations:
- **[[concepts/kv-cache]]** — avoid recomputing attention for past tokens
- **[[concepts/speculative-decoding]]** — parallelize via draft-verify
- **Efficient sampling** — top-k, top-p, temperature

See also: [[concepts/transformer-architecture]], [[concepts/inference-optimization]]
""",

"conditional-generation": """---
title: "Conditional Generation"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["ho-cfg-paper"]
tags: [generation, conditioning, text-to-image]
summary: "Generating outputs conditioned on input signals like text prompts or class labels"
---

# Conditional Generation

Conditioning generation on external signals (text, class labels, images). [[concepts/classifier-free-guidance]] ([[sources/ho-cfg-paper]]) is the key technique for [[concepts/diffusion-models]], enabling high-quality text-to-image generation.

See also: [[concepts/diffusion-models]], [[synthesis/diffusion-foundations]]
""",

"stochastic-differential-equations": """---
title: "Stochastic Differential Equations"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["song-score-sde-paper"]
tags: [math, diffusion, continuous-time]
summary: "The continuous-time mathematical framework unifying score-based and diffusion generative models"
---

# Stochastic Differential Equations

[[sources/song-score-sde-paper]] showed that diffusion models can be described as SDEs: dx = f(x,t)dt + g(t)dw (forward) and the reverse SDE for generation. This unified [[concepts/score-matching]] and [[concepts/diffusion-models]] into one elegant framework.

See also: [[synthesis/diffusion-foundations]]
""",

"self-critique": """---
title: "Self-Critique / Self-Improvement"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [alignment, iterative, improvement]
summary: "LLMs evaluating and improving their own outputs"
---

# Self-Critique

A key mechanism in [[concepts/constitutional-ai]]: the model evaluates its own outputs against explicit principles, then revises. This enables iterative improvement without human feedback.

Also used in chain-of-thought verification, code debugging, and agentic workflows.

See also: [[concepts/alignment]], [[entities/anthropic]]
""",

"data-efficiency": """---
title: "Data Efficiency"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: ["hoffmann-chinchilla-paper"]
tags: [data, quality, curation]
summary: "Getting more from less data through quality curation, deduplication, and curriculum strategies"
---

# Data Efficiency

After [[concepts/chinchilla-optimal]] showed data quantity matters, the focus shifted to data *quality*. Key strategies:

- **Deduplication** — removing repeated content improves training efficiency
- **Quality filtering** — heuristics and classifiers to select high-quality text
- **Curriculum learning** — ordering data from easy to hard
- **Data mixing** — balancing domains (code, math, natural language)

See also: [[concepts/scaling-laws]], [[concepts/pre-training]]
""",

"ppo-algorithm": """---
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
""",

"emergent-abilities": """---
title: "Emergent Abilities"
type: concept
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [scaling, capabilities, phase-transition]
summary: "Capabilities that appear only at sufficient scale — chain-of-thought, in-context learning, instruction following"
---

# Emergent Abilities

Some capabilities appear to emerge discontinuously as models scale: chain-of-thought reasoning, in-context learning, instruction following. Whether these are truly emergent or just gradually improving is debated.

## Connection to [[concepts/scaling-laws]]

Scaling laws predict *loss*, but emergent abilities suggest that *capabilities* can appear unpredictably. This is why [[entities/openai]] and others continue scaling despite diminishing returns on loss.

See also: [[concepts/pre-training]], [[concepts/alignment]]
""",
}

# ============================================================
# ENTITIES (20)
# ============================================================
ENTITIES = {
"geoffrey-hinton": """---
title: "Geoffrey Hinton"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [person, deep-learning, pioneer]
summary: "Deep learning pioneer, Turing Award, Nobel Prize 2024 — backpropagation and Boltzmann machines"
entity_type: "person"
---

# Geoffrey Hinton

Deep learning pioneer. Co-invented backpropagation, Boltzmann machines, and dropout. Turing Award 2018, Nobel Prize in Physics 2024. Left Google in 2023 to speak freely about AI risks.

His students and academic descendants dominate the field: [[entities/yann-lecun]], [[entities/ilya-sutskever]], and many others. The "Godfather of Deep Learning."

Connected to: [[concepts/pre-training]], [[concepts/self-supervised-learning]], [[concepts/alignment]]
""",

"yann-lecun": """---
title: "Yann LeCun"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [person, meta-ai, self-supervised-learning]
summary: "Chief AI Scientist at Meta, Turing Award — champion of self-supervised learning"
entity_type: "person"
---

# Yann LeCun

Chief AI Scientist at [[entities/meta-ai]]. Turing Award 2018 (with [[entities/geoffrey-hinton]] and Yoshua Bengio). Invented convolutional networks, champion of [[concepts/self-supervised-learning]].

Vocal advocate for open-source AI and critic of doomer narratives. Believes [[concepts/self-supervised-learning]] (not [[concepts/rlhf]]) is the path to human-level AI.

See also: [[concepts/contrastive-learning]], [[concepts/pre-training]]
""",

"andrej-karpathy": """---
title: "Andrej Karpathy"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [person, educator, tesla, nanogpt]
summary: "ML educator and builder — former Tesla AI director, creator of nanoGPT"
entity_type: "person"
---

# Andrej Karpathy

Former director of AI at Tesla, former researcher at [[entities/openai]]. Created nanoGPT, minGPT, and legendary teaching materials that have taught a generation of ML engineers.

His unique value: translating complex [[concepts/transformer-architecture]] concepts into accessible code. The "build it from scratch" philosophy embodies [[concepts/learning-by-building]].

See also: [[concepts/autoregressive-generation]], [[concepts/pre-training]]
""",

"openai": """---
title: "OpenAI"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: ["kaplan-scaling-paper", "ouyang-instructgpt-paper"]
tags: [organization, gpt, chatgpt, scaling]
summary: "AI research lab behind GPT-4, ChatGPT — driving the scaling paradigm"
entity_type: "organization"
---

# OpenAI

The lab that brought LLMs to the mainstream. Key contributions:
- **[[concepts/scaling-laws]]** ([[sources/kaplan-scaling-paper]])
- **[[concepts/rlhf]]** pipeline ([[sources/ouyang-instructgpt-paper]])
- **[[concepts/triton-compiler]]** ([[sources/tillet-triton-paper]])
- GPT series, ChatGPT, DALL-E

Notable people: [[entities/ilya-sutskever]] (co-founder, departed), [[entities/andrej-karpathy]] (departed).

See also: [[entities/anthropic]], [[entities/deepmind]], [[concepts/alignment]]
""",

"anthropic": """---
title: "Anthropic"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [organization, claude, safety, constitutional-ai]
summary: "AI safety company building Claude — pioneered Constitutional AI"
entity_type: "organization"
---

# Anthropic

Founded by former [[entities/openai]] researchers (Dario and Daniela Amodei). Safety-first approach to AI development.

Key contributions:
- **[[concepts/constitutional-ai]]** — alignment without human labels
- **Claude** — their model family, known for [[concepts/long-context]] capabilities
- Advancing [[concepts/alignment]] research

See also: [[concepts/rlhf]], [[concepts/self-critique]]
""",

"deepmind": """---
title: "DeepMind"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: ["hoffmann-chinchilla-paper"]
tags: [organization, google, alphafold, gemini]
summary: "Google's AI research lab — from AlphaGo to Gemini"
entity_type: "organization"
---

# DeepMind

Google's AI research arm. From game-playing AI (AlphaGo) to protein folding (AlphaFold) to Gemini.

Key contribution to LLMs: **[[concepts/chinchilla-optimal]]** ([[sources/hoffmann-chinchilla-paper]]) — showing most models were undertrained. This reshaped how the entire field thinks about [[concepts/scaling-laws]] and [[concepts/data-efficiency]].

See also: [[entities/google-brain]], [[concepts/alignment]]
""",

"meta-ai": """---
title: "Meta AI (FAIR)"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: ["lewis-rag-paper", "chen-simclr-paper"]
tags: [organization, llama, open-source]
summary: "Meta's AI research division — driving open-source LLMs and SSL research"
entity_type: "organization"
---

# Meta AI (FAIR)

Led by [[entities/yann-lecun]]. Key contributions:
- **LLaMA** series — the most impactful open-source LLMs
- **[[concepts/self-supervised-learning]]** research (SimCLR, DINO, MAE)
- **[[concepts/rag]]** ([[sources/lewis-rag-paper]])
- **[[concepts/contrastive-learning]]** foundations

The open-source strategy fundamentally changed the LLM landscape. LLaMA enabled an entire ecosystem of finetuned models.

See also: [[concepts/pre-training]], [[entities/openai]]
""",

"google-brain": """---
title: "Google Brain / Google Research"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: ["vaswani-attention-paper", "ho-ddpm-paper", "ho-cfg-paper", "chen-simclr-paper", "shazeer-moe-paper"]
tags: [organization, transformer, tpu]
summary: "Birthplace of the Transformer — merged into Google DeepMind"
entity_type: "organization"
---

# Google Brain

The research group that created the [[concepts/transformer-architecture]] ([[sources/vaswani-attention-paper]]). Also produced:
- **DDPM** ([[sources/ho-ddpm-paper]]) — practical [[concepts/diffusion-models]]
- **[[concepts/classifier-free-guidance]]** ([[sources/ho-cfg-paper]])
- **[[concepts/mixture-of-experts]]** ([[sources/shazeer-moe-paper]])
- **SimCLR** ([[sources/chen-simclr-paper]])

Merged with [[entities/deepmind]] into Google DeepMind in 2023.
""",

"nvidia": """---
title: "NVIDIA"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [organization, gpu, cuda, hardware]
summary: "The hardware company powering modern AI — GPUs, CUDA, training infrastructure"
entity_type: "organization"
---

# NVIDIA

The essential hardware platform for AI. Key contributions:
- **GPUs** — the compute substrate for all modern ML
- **CUDA** — the programming model for GPU compute
- **[[entities/megatron-lm]]** — 3D parallelism for large-scale [[concepts/distributed-training]]
- **[[entities/tensorrt-llm]]** — optimized LLM inference
- **NCCL** — collective communication library

Understanding [[concepts/gpu-memory-hierarchy]] — NVIDIA's HBM/SRAM/register hierarchy — is essential for [[concepts/flash-attention]] and [[concepts/kernel-fusion]].
""",

"microsoft": """---
title: "Microsoft"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: ["hu-lora-paper"]
tags: [organization, azure, deepspeed, copilot]
summary: "Major AI investor and platform — DeepSpeed, LoRA, Copilot"
entity_type: "organization"
---

# Microsoft

Key AI contributions:
- **[[concepts/lora]]** ([[sources/hu-lora-paper]]) — parameter-efficient finetuning
- **[[entities/deepspeed]]** — distributed training with ZeRO
- **GitHub Copilot** — AI-powered coding
- **Azure AI** — cloud infrastructure for model serving

Major investor in [[entities/openai]].

See also: [[concepts/parameter-efficient-finetuning]], [[concepts/distributed-training]]
""",

"pytorch": """---
title: "PyTorch"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, framework, deep-learning]
summary: "The dominant deep learning framework — dynamic computation graphs, Python-native"
entity_type: "tool"
---

# PyTorch

The standard framework for ML research and increasingly production. Key features:
- Dynamic computation graphs (eager mode)
- DDP / FSDP for [[concepts/data-parallelism]]
- torch.compile for [[concepts/kernel-fusion]]

Developed by [[entities/meta-ai]], used by virtually every lab.

See also: [[concepts/distributed-training]], [[entities/megatron-lm]]
""",

"vllm": """---
title: "vLLM"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, serving, inference, pagedattention]
summary: "High-throughput LLM serving engine — PagedAttention for efficient KV cache management"
entity_type: "tool"
---

# vLLM

The most popular open-source LLM serving engine. Its key innovation, PagedAttention, manages [[concepts/kv-cache]] like an OS manages virtual memory — eliminating fragmentation and enabling efficient batching.

Core to the [[concepts/inference-optimization]] stack alongside [[concepts/flash-attention]], [[concepts/quantization]], and [[concepts/speculative-decoding]].

See also: [[entities/tensorrt-llm]], [[synthesis/serving-stack-2026]]
""",

"megatron-lm": """---
title: "Megatron-LM"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, nvidia, distributed-training, parallelism]
summary: "NVIDIA's framework for 3D parallelism — tensor, pipeline, and data parallelism combined"
entity_type: "tool"
---

# Megatron-LM

[[entities/nvidia]]'s framework for training massive language models. Implements:
- [[concepts/tensor-parallelism]] — split attention heads and FFN across GPUs
- [[concepts/pipeline-parallelism]] — split layers across stages
- [[concepts/data-parallelism]] — replicate across groups

The reference implementation for [[concepts/distributed-training]] at scale.

See also: [[entities/deepspeed]], [[synthesis/parallelism-taxonomy]]
""",

"deepspeed": """---
title: "DeepSpeed"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, microsoft, distributed, zero]
summary: "Microsoft's distributed training library — ZeRO optimizer sharding"
entity_type: "tool"
---

# DeepSpeed

[[entities/microsoft]]'s library for efficient [[concepts/distributed-training]]. Key innovation: **ZeRO** (Zero Redundancy Optimizer) — progressively shard optimizer states, gradients, and parameters across GPUs.

ZeRO stages:
- Stage 1: shard optimizer states
- Stage 2: + shard gradients
- Stage 3: + shard parameters (= FSDP)

See also: [[concepts/data-parallelism]], [[entities/megatron-lm]], [[synthesis/parallelism-taxonomy]]
""",

"tensorrt-llm": """---
title: "TensorRT-LLM"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, nvidia, inference, optimization]
summary: "NVIDIA's LLM inference library — kernel fusion, quantization, batching"
entity_type: "tool"
---

# TensorRT-LLM

[[entities/nvidia]]'s inference optimization library. Combines [[concepts/kernel-fusion]], [[concepts/quantization]], and advanced batching for maximum throughput.

Complements [[entities/vllm]] — TensorRT-LLM focuses on kernel-level optimization, vLLM on system-level scheduling.

See also: [[concepts/inference-optimization]], [[synthesis/serving-stack-2026]]
""",

"pinecone": """---
title: "Pinecone"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, vector-database, managed]
summary: "Managed vector database for semantic search and RAG"
entity_type: "tool"
---

# Pinecone

Managed [[concepts/vector-databases]] service. Production-focused: handles scaling, indexing, and ANN search so you can focus on building [[concepts/rag]] applications.

See also: [[entities/chromadb]], [[concepts/embedding-models]]
""",

"chromadb": """---
title: "ChromaDB"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [tool, vector-database, open-source]
summary: "Open-source embedding database — lightweight, popular for prototyping RAG"
entity_type: "tool"
---

# ChromaDB

Open-source [[concepts/vector-databases]]. Lightweight, easy to embed in Python applications. Popular for prototyping [[concepts/rag]] systems before moving to production solutions like [[entities/pinecone]].

See also: [[concepts/embedding-models]], [[synthesis/rag-architecture-patterns]]
""",

"cohere": """---
title: "Cohere"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [organization, embeddings, enterprise]
summary: "Enterprise NLP company — strong embedding models and retrieval APIs"
entity_type: "organization"
---

# Cohere

Enterprise NLP company focused on [[concepts/embedding-models]] and [[concepts/rag]]. Their Embed v3 model is widely used for production retrieval systems.

See also: [[entities/openai]], [[concepts/vector-databases]]
""",

"ilya-sutskever": """---
title: "Ilya Sutskever"
type: entity
created: 2026-01-01
updated: 2026-04-01
sources: []
tags: [person, openai, ssi, scaling]
summary: "OpenAI co-founder turned SSI founder — early advocate of scaling as path to AGI"
entity_type: "person"
---

# Ilya Sutskever

Student of [[entities/geoffrey-hinton]]. Co-founded [[entities/openai]], then left to found SSI (Safe Superintelligence Inc.). Early and persistent advocate that [[concepts/scaling-laws]] + [[concepts/pre-training]] would lead to AGI.

Key insight: "The data is the data" — [[concepts/pre-training]] on internet-scale data is sufficient for general intelligence. This belief drove OpenAI's scaling trajectory.

See also: [[concepts/alignment]], [[concepts/emergent-abilities]]
""",
}

# ============================================================
# SOURCES (18)
# ============================================================
SOURCES = {
"vaswani-attention-paper": """---
title: "Attention Is All You Need (Vaswani et al., 2017)"
type: source
created: 2017-06-12
updated: 2017-06-12
sources: []
tags: [paper, transformer, attention]
summary: "The original Transformer paper — self-attention replaces recurrence"
source_type: "paper"
---

# Attention Is All You Need

The paper that started the modern AI era. Introduced the [[concepts/transformer-architecture]] with [[concepts/attention-mechanism]] as the sole sequence modeling mechanism, replacing RNNs.

## Key Contributions
- Multi-head self-attention
- [[concepts/positional-encoding]] (sinusoidal)
- Encoder-decoder architecture
- Demonstrated on machine translation

Published by [[entities/google-brain]]. Everything since — GPT, BERT, LLaMA, Claude — descends from this architecture.
""",

"kaplan-scaling-paper": """---
title: "Scaling Laws for Neural Language Models (Kaplan et al., 2020)"
type: source
created: 2020-01-23
updated: 2020-01-23
sources: []
tags: [paper, scaling-laws, openai]
summary: "First systematic study of neural scaling laws — power-law relationships"
source_type: "paper"
---

# Scaling Laws for Neural Language Models

[[entities/openai]] showed that LLM loss follows smooth power laws in model size, data size, and compute. This paper made [[concepts/scaling-laws]] a science: you could predict performance before training.

Key finding: model size matters more than data size (later revised by [[sources/hoffmann-chinchilla-paper]]).
""",

"hoffmann-chinchilla-paper": """---
title: "Training Compute-Optimal Large Language Models (Hoffmann et al., 2022)"
type: source
created: 2022-03-29
updated: 2022-03-29
sources: []
tags: [paper, chinchilla, scaling, deepmind]
summary: "The Chinchilla paper — most LLMs are undertrained, use more data"
source_type: "paper"
---

# Chinchilla

[[entities/deepmind]] corrected [[sources/kaplan-scaling-paper]]: the optimal data-to-parameter ratio is ~20:1, meaning most models were undertrained. This redirected the field toward [[concepts/data-efficiency]] and [[concepts/chinchilla-optimal]] training.
""",

"ouyang-instructgpt-paper": """---
title: "Training Language Models to Follow Instructions (Ouyang et al., 2022)"
type: source
created: 2022-03-04
updated: 2022-03-04
sources: []
tags: [paper, instructgpt, rlhf, openai]
summary: "InstructGPT — introduced the RLHF pipeline for aligning LLMs"
source_type: "paper"
---

# InstructGPT

The [[entities/openai]] paper that made [[concepts/rlhf]] practical at scale. Introduced the three-stage pipeline: SFT → [[concepts/reward-modeling]] → [[concepts/ppo-algorithm]] optimization. This became the template for aligning every major LLM.
""",

"hu-lora-paper": """---
title: "LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)"
type: source
created: 2021-06-17
updated: 2021-06-17
sources: []
tags: [paper, lora, finetuning, microsoft]
summary: "Low-rank adaptation — efficient finetuning with minimal parameters"
source_type: "paper"
---

# LoRA

[[entities/microsoft]]'s paper introducing [[concepts/lora]]. Key insight: weight updates during finetuning are low-rank. Inject trainable BA matrices (r << d), freeze everything else. Revolutionized [[concepts/parameter-efficient-finetuning]].
""",

"dettmers-qlora-paper": """---
title: "QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023)"
type: source
created: 2023-05-23
updated: 2023-05-23
sources: []
tags: [paper, qlora, quantization, finetuning]
summary: "4-bit quantization + LoRA — finetune 65B on a single GPU"
source_type: "paper"
---

# QLoRA

Combined [[concepts/quantization]] (4-bit NormalFloat) with [[concepts/lora]] to finetune 65B models on a single 48GB GPU. Introduced double quantization and paged optimizers.

See also: [[concepts/parameter-efficient-finetuning]], [[synthesis/finetuning-decision-tree]]
""",

"dao-flashattention-paper": """---
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
""",

"ho-ddpm-paper": """---
title: "Denoising Diffusion Probabilistic Models (Ho et al., 2020)"
type: source
created: 2020-06-19
updated: 2020-06-19
sources: []
tags: [paper, ddpm, diffusion, generative]
summary: "Made diffusion models practical — simple MSE objective, high-quality generation"
source_type: "paper"
---

# DDPM

[[entities/google-brain]]'s paper that made [[concepts/diffusion-models]] practical. Simple training objective (predict noise), iterative denoising at inference. Connected to [[concepts/score-matching]] through [[sources/song-score-sde-paper]].
""",

"song-score-sde-paper": """---
title: "Score-Based Generative Modeling through SDEs (Song et al., 2020)"
type: source
created: 2020-11-26
updated: 2020-11-26
sources: []
tags: [paper, score-sde, diffusion, continuous-time]
summary: "Unified framework connecting score-based models and diffusion through SDEs"
source_type: "paper"
---

# Score SDE

Unified [[concepts/score-matching]] and [[concepts/diffusion-models]] through [[concepts/stochastic-differential-equations]]. Showed both are views of the same continuous-time generative process.

See also: [[sources/ho-ddpm-paper]], [[synthesis/diffusion-foundations]]
""",

"ho-cfg-paper": """---
title: "Classifier-Free Diffusion Guidance (Ho & Salimans, 2022)"
type: source
created: 2022-07-26
updated: 2022-07-26
sources: []
tags: [paper, cfg, diffusion, conditioning]
summary: "Classifier-free guidance for better conditional generation"
source_type: "paper"
---

# Classifier-Free Guidance

[[entities/google-brain]]. Introduced [[concepts/classifier-free-guidance]]: jointly train conditional and unconditional models, extrapolate toward the conditional at inference. Essential for text-to-image [[concepts/diffusion-models]].
""",

"lewis-rag-paper": """---
title: "Retrieval-Augmented Generation (Lewis et al., 2020)"
type: source
created: 2020-05-22
updated: 2020-05-22
sources: []
tags: [paper, rag, retrieval, meta]
summary: "Original RAG paper — combining retrieval with generation"
source_type: "paper"
---

# RAG Paper

[[entities/meta-ai]]'s original [[concepts/rag]] paper. Showed that combining parametric (LM) and non-parametric (retrieval) memory improves knowledge-intensive tasks. Foundation for modern RAG systems using [[concepts/embedding-models]] and [[concepts/vector-databases]].
""",

"chen-simclr-paper": """---
title: "SimCLR: A Simple Framework for Contrastive Learning (Chen et al., 2020)"
type: source
created: 2020-02-13
updated: 2020-02-13
sources: []
tags: [paper, simclr, contrastive, self-supervised]
summary: "Simple contrastive framework matching supervised performance"
source_type: "paper"
---

# SimCLR

[[entities/google-brain]]. Showed [[concepts/contrastive-learning]] with simple augmentations could match supervised ImageNet performance. Proved [[concepts/self-supervised-learning]] works at scale.
""",

"shazeer-moe-paper": """---
title: "Outrageously Large Neural Networks: Sparsely-Gated MoE (Shazeer et al., 2017)"
type: source
created: 2017-01-23
updated: 2017-01-23
sources: []
tags: [paper, moe, sparse, routing]
summary: "Modern MoE with learnable gating — conditional computation"
source_type: "paper"
---

# Sparsely-Gated MoE

[[entities/google-brain]]. Introduced modern [[concepts/mixture-of-experts]] with learnable top-K routing. Enabled massive model capacity with sublinear compute cost. Ancestor of Mixtral, DeepSeek-V3.
""",

"leviathan-speculative-paper": """---
title: "Fast Inference via Speculative Decoding (Leviathan et al., 2022)"
type: source
created: 2022-11-30
updated: 2022-11-30
sources: []
tags: [paper, speculative-decoding, inference]
summary: "Draft-verify paradigm for faster autoregressive generation"
source_type: "paper"
---

# Speculative Decoding

Introduced [[concepts/speculative-decoding]]: small model drafts, large model verifies. Lossless speedup for [[concepts/autoregressive-generation]] by exploiting the bandwidth-bound nature of LLM inference.
""",

"su-rope-paper": """---
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding (Su et al., 2021)"
type: source
created: 2021-04-20
updated: 2021-04-20
sources: []
tags: [paper, rope, position-encoding]
summary: "Rotary position embedding — elegant relative position via rotation"
source_type: "paper"
---

# RoPE Paper

Introduced [[concepts/rope]]: encode position by rotating queries and keys in complex space. Relative position emerges naturally from the dot product. Now standard [[concepts/positional-encoding]] in nearly all LLMs.
""",

"tillet-triton-paper": """---
title: "Triton: An Intermediate Language for Tiled Neural Network Computations (Tillet et al., 2019)"
type: source
created: 2019-04-14
updated: 2019-04-14
sources: []
tags: [paper, triton, compiler, gpu]
summary: "Python-like DSL for GPU kernels — democratizing CUDA programming"
source_type: "paper"
---

# Triton

[[entities/openai]]'s [[concepts/triton-compiler]]. A Python-like DSL that compiles to efficient GPU code. Made custom [[concepts/kernel-fusion]] accessible to ML researchers without deep CUDA expertise. [[concepts/flash-attention]] was prototyped in Triton.
""",

"gpipe-paper": """---
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
""",

"lin-awq-paper": """---
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
""",
}

# ============================================================
# SYNTHESIS (10)
# ============================================================
SYNTHESIS = {
"scaling-vs-efficiency": """---
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
""",

"alignment-landscape": """---
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
""",

"serving-stack-2026": """---
title: "LLM Serving Stack in 2026"
type: synthesis
created: 2026-03-01
updated: 2026-03-01
sources: []
tags: [synthesis, serving, inference, systems]
summary: "The modern LLM serving stack — from kernel to API"
---

# LLM Serving Stack in 2026

Bottom-up:

1. **Hardware**: [[entities/nvidia]] GPUs, [[concepts/gpu-memory-hierarchy]]
2. **Kernels**: [[concepts/flash-attention]], [[concepts/kernel-fusion]] ([[entities/tensorrt-llm]])
3. **Runtime**: [[concepts/kv-cache]] + PagedAttention ([[entities/vllm]])
4. **Algorithm**: [[concepts/speculative-decoding]], [[concepts/quantization]]
5. **API**: load balancing, continuous batching, routing

Every layer compounds. 2x kernel speedup × 2x runtime efficiency × 2x quantization = 8x total throughput improvement.

See also: [[concepts/inference-optimization]], [[concepts/long-context]]
""",

"parallelism-taxonomy": """---
title: "A Taxonomy of Parallelism Strategies"
type: synthesis
created: 2026-03-10
updated: 2026-03-10
sources: ["gpipe-paper"]
tags: [synthesis, distributed, parallelism, decision-framework]
summary: "When to use which parallelism strategy — a decision framework"
---

# Parallelism Taxonomy

| Strategy | Splits | Communication | Best For |
|----------|--------|--------------|----------|
| [[concepts/data-parallelism]] | Data | Allreduce | Model fits in 1 GPU |
| [[concepts/tensor-parallelism]] | Ops | Per-layer allreduce | Intra-node, fast interconnect |
| [[concepts/pipeline-parallelism]] | Layers | Point-to-point | Inter-node, high latency tolerance |
| FSDP/ZeRO | Optimizer+params | Allgather | Memory-constrained |

## Decision Framework

1. Model fits in 1 GPU? → [[concepts/data-parallelism]]
2. Doesn't fit? → Add FSDP/ZeRO ([[entities/deepspeed]])
3. Still doesn't fit? → [[concepts/tensor-parallelism]] within nodes ([[entities/megatron-lm]])
4. More nodes needed? → [[concepts/pipeline-parallelism]] across nodes

See also: [[concepts/distributed-training]]
""",

"diffusion-foundations": """---
title: "Diffusion Models: Mathematical Foundations"
type: synthesis
created: 2026-01-25
updated: 2026-01-25
sources: ["ho-ddpm-paper", "song-score-sde-paper", "ho-cfg-paper"]
tags: [synthesis, diffusion, math, foundations]
summary: "From Brownian motion to DALL-E — the mathematical path"
---

# Diffusion Foundations

The mathematical lineage:
1. **[[concepts/score-matching]]** — learn ∇log p(x) ([[sources/song-score-sde-paper]])
2. **[[concepts/diffusion-models]]** — reverse a noising process ([[sources/ho-ddpm-paper]])
3. **[[concepts/stochastic-differential-equations]]** — continuous-time unification
4. **[[concepts/classifier-free-guidance]]** — conditional control ([[sources/ho-cfg-paper]])

These build on each other. Understanding SDEs makes the design space clear: you're choosing a forward process (noise schedule) and learning the reverse.

See also: [[concepts/conditional-generation]], [[entities/google-brain]]
""",

"rag-architecture-patterns": """---
title: "RAG Architecture Patterns"
type: synthesis
created: 2026-03-20
updated: 2026-03-20
sources: ["lewis-rag-paper"]
tags: [synthesis, rag, architecture, patterns]
summary: "Evolution of RAG from naive to production"
---

# RAG Architecture Patterns

## Naive RAG
Embed → retrieve top-K → concatenate → generate. Simple but fragile.

## Advanced RAG
- **Hybrid search**: [[concepts/vector-databases]] (semantic) + BM25 (keyword)
- **Reranking**: cross-encoder to reorder retrieved documents
- **Chunking strategies**: overlap, semantic boundaries
- **Query rewriting**: expand/refine the query before retrieval

## Production RAG
- [[entities/pinecone]] or [[entities/chromadb]] for [[concepts/vector-databases]]
- [[concepts/embedding-models]] from [[entities/openai]] or [[entities/cohere]]
- Evaluation: precision@K, faithfulness, answer relevancy

See also: [[concepts/rag]], [[synthesis/finetuning-decision-tree]]
""",

"finetuning-decision-tree": """---
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
""",

"gpu-programming-landscape": """---
title: "GPU Programming: CUDA vs. Triton vs. Framework Kernels"
type: synthesis
created: 2026-03-15
updated: 2026-03-15
sources: ["tillet-triton-paper"]
tags: [synthesis, gpu, programming, comparison]
summary: "The tradeoff space in GPU programming — flexibility vs. productivity"
---

# GPU Programming Landscape

| Approach | Flexibility | Productivity | Performance |
|----------|:-:|:-:|:-:|
| CUDA | High | Low | Highest |
| [[concepts/triton-compiler]] | Medium | High | High |
| torch.compile ([[entities/pytorch]]) | Low | Highest | Medium |

## When to Use What

- **torch.compile**: default choice, good enough for most [[concepts/kernel-fusion]]
- **Triton** ([[sources/tillet-triton-paper]]): custom kernels, [[concepts/flash-attention]]-style work
- **CUDA**: maximum performance, [[entities/nvidia]]-specific features

See also: [[concepts/gpu-memory-hierarchy]]
""",

"ssl-to-foundation": """---
title: "From Self-Supervised Learning to Foundation Models"
type: synthesis
created: 2026-01-10
updated: 2026-01-10
sources: ["chen-simclr-paper"]
tags: [synthesis, ssl, foundation-models, evolution]
summary: "How SSL evolved into the foundation model paradigm"
---

# From SSL to Foundation Models

The evolution:
1. **word2vec** (2013) — [[concepts/self-supervised-learning]] on text
2. **SimCLR** ([[sources/chen-simclr-paper]]) — [[concepts/contrastive-learning]] matches supervised vision
3. **BERT** (2018) — masked language modeling at scale
4. **GPT-3** (2020) — [[concepts/pre-training]] + [[concepts/scaling-laws]] = few-shot learning
5. **Foundation models** — one pretrained model, many tasks

The thread: all of these use SSL. The revolution was realizing that SSL + scale = general capabilities.

Key players: [[entities/google-brain]], [[entities/openai]], [[entities/meta-ai]]
""",

"attention-evolution": """---
title: "Attention Mechanism Evolution"
type: synthesis
created: 2026-01-15
updated: 2026-01-15
sources: ["vaswani-attention-paper", "dao-flashattention-paper"]
tags: [synthesis, attention, evolution, systems]
summary: "How attention went from bottleneck to efficient — and what's next"
---

# Attention Evolution

Timeline:
1. **Vanilla attention** ([[sources/vaswani-attention-paper]]) — O(N²) memory, simple but expensive
2. **Sparse/linear attention** (2019-2021) — approximate, trade quality for speed
3. **[[concepts/flash-attention]]** ([[sources/dao-flashattention-paper]]) — exact + fast via [[concepts/gpu-memory-hierarchy]]
4. **Ring attention** — distribute across devices for ultra-long contexts

## Lesson

The winning approach wasn't mathematical cleverness (approximation) but systems insight (IO-awareness). [[entities/tri-dao]] understood the hardware better than the approximation crowd understood the math.

See also: [[concepts/attention-mechanism]], [[concepts/long-context]], [[concepts/kernel-fusion]]
""",
}

# ============================================================
# Main
# ============================================================
def main():
    counts = {"concepts": 0, "entities": 0, "sources": 0, "synthesis": 0}
    for slug, content in CONCEPTS.items():
        if write_page("concepts", slug, content):
            counts["concepts"] += 1
    for slug, content in ENTITIES.items():
        if write_page("entities", slug, content):
            counts["entities"] += 1
    for slug, content in SOURCES.items():
        if write_page("sources", slug, content):
            counts["sources"] += 1
    for slug, content in SYNTHESIS.items():
        if write_page("synthesis", slug, content):
            counts["synthesis"] += 1

    total = sum(counts.values())
    for k, v in counts.items():
        print(f"[{k}] Created: {v}")
    print(f"\n=== Total new: {total} ===")

if __name__ == "__main__":
    main()
