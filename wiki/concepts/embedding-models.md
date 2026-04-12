---
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
