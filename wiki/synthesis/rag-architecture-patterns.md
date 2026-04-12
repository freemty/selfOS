---
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
