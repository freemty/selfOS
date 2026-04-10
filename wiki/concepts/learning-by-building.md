---
title: "Learning by Building"
type: concept
created: 2025-10-03
updated: 2026-01-20
sources: ["gem-2025-10-03-flash-attention-deep-dive", "cc-2026-01-20-why-i-chose-systems-over-theory"]
tags: [methodology, learning, systems, building]
summary: "Building tools and systems as the deepest form of understanding — you don't really know it until you've built it"
---

# Learning by Building

## Core Idea

Reading a paper gives you a map. Building the system gives you the territory. The gap between the two is where real understanding lives.

This isn't anti-intellectual — it's a claim about the **type** of knowledge that matters for systems research. Theoretical understanding tells you what should work. Implementation tells you what actually works and why the theory was subtly wrong.

## Evidence From My Own Experience

### FlashAttention Implementation

Spent 3 hours reading the paper with Gemini, then 2 days implementing in Triton (source: [[sources/gem-2025-10-03-flash-attention-deep-dive]]). The forward pass was straightforward. The backward pass revealed complexities the paper handles in one paragraph but took me 400 lines of code. That's where the real learning happened.

### KV-Cache Compression

My first systems paper came from building a naive KV-cache and noticing the memory pattern was dominated by attention sink tokens. I wouldn't have spotted this from reading alone — it required instrumenting a real system.

## Why Building Develops [[concepts/research-taste]]

When you build, you discover:
- Which parts are actually hard (vs. which parts the paper says are hard)
- Where the abstractions leak
- What the next bottleneck will be after the current one is solved

These discoveries are the raw material of taste. [[entities/tri-dao]]'s hardware intuition came from years of building systems, not from reading architecture manuals.

## Practical Protocol

1. **Read the paper** — get the map
2. **Implement from scratch** — discover the territory
3. **Break it intentionally** — find the boundaries
4. **Write about the gap** — between paper and reality

[[entities/study-group]] adopted this as our standard protocol: every other week we implement a paper, not just discuss it.

## Relationship to [[concepts/career-pivots]]

Choosing systems over theory means choosing a path where building *is* the research, not just a step toward the research (source: [[sources/cc-2026-01-20-why-i-chose-systems-over-theory]]). [[entities/alex-advisor]] encouraged this: "Your best thinking happens when your hands are on the keyboard."

## Limitations

- Building everything from scratch doesn't scale — need to be selective
- Risk of bikeshedding on implementation details rather than research questions
- Need to pair with reading to avoid reinventing wheels
