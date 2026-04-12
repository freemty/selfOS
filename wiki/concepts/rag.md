---
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
