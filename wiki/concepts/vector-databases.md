---
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
