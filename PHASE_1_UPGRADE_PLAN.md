# Phase 1 RAG Upgrade Plan: Skeleton → Production-Ready

## Current State (Skeleton)
- ✅ Document chunking: Converts experiences.json to RAG documents
- ✅ JSON vector store: Stores documents with metadata
- ✅ Retrieval pipeline: Returns top-K results
- ❌ **Synthetic embeddings**: Hash-based, not semantic
- ❌ **No LLM integration**: No AI-powered rewriting
- ❌ **No vector DB**: JSON-based, not scalable
- ❌ **No reranking**: No quality filtering

## Feedback from Code Review

> "It's a good RAG skeleton (index → retrieve → use context), but not a full, production RAG."

### What's Missing for "Real RAG"

1. **Real embeddings** - Swap fake hash/sine vectors for actual ML embeddings
2. **A vector store** - Use FAISS/Chroma/pgvector instead of JSON
3. **LLM generation & planning** - Use LLM to rewrite bullets with evidence constraints
4. **Reranking** (optional) - Cross-encoder to improve top-K quality

---

## Upgrade Tasks

### A) Real Embeddings (sentence-transformers)

**Current**: Hash-based embeddings (deterministic but not semantic)
```python
def _generate_embedding(self, text: str) -> List[float]:
    hash_val = sum(ord(c) for c in text)
    embedding = []
    for i in range(384):
        embedding.append(math.sin((hash_val + i) * 0.1) * 0.5 + 0.5)
    return embedding
```

**Target**: Real semantic embeddings
```python
from sentence_transformers import SentenceTransformer

class RAGIndexer:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def _embed(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.encode(texts, normalize_embeddings=True).tolist()
```

**Changes**:
- [ ] Add `sentence-transformers` dependency
- [ ] Update `RAGIndexer._embed()` to use SentenceTransformer
- [ ] Update `Retriever._query_embedding()` to use SentenceTransformer
- [ ] Re-index all documents with real embeddings
- [ ] Update tests to validate semantic similarity

**Impact**: Semantic search instead of keyword matching

---

### B) Vector Database (FAISS)

**Current**: JSON file with linear search
```python
# O(n) search through all documents
for doc in self.documents:
    score = self._cosine_similarity(query_embedding, doc.embedding)
```

**Target**: FAISS for efficient similarity search
```python
import faiss
import numpy as np

class Retriever:
    def __init__(self, vector_store_path):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatIP(384)  # Inner product for cosine
        
        # Load embeddings and build index
        embeddings = np.array([d["embedding"] for d in docs], dtype="float32")
        self.index.add(embeddings)
    
    def retrieve(self, query: str, top_k: int = 10):
        q_emb = np.array([self.embedder.encode(query)], dtype="float32")
        scores, indices = self.index.search(q_emb, top_k)
        return [(self.documents[i], float(scores[0][j])) 
                for j, i in enumerate(indices[0])]
```

**Changes**:
- [ ] Add `faiss-cpu` dependency (or `faiss-gpu` for production)
- [ ] Update `RAGIndexer` to build FAISS index
- [ ] Update `Retriever` to use FAISS for search
- [ ] Save/load FAISS index alongside JSON metadata
- [ ] Update tests for FAISS integration

**Impact**: O(log n) search, scales to millions of documents

---

### C) LLM-Powered Rewriting

**Current**: No LLM integration, just retrieval
```python
# tailor.py just injects retrieved context into prompt
rag_context = retriever.retrieve(requirement)
# Context passed to LLM but no special handling
```

**Target**: Evidence-constrained LLM rewriting
```python
from openai import OpenAI

def rewrite_with_evidence(bullet: str, evidence: str, requirement: str) -> str:
    """Rewrite bullet using retrieved evidence as constraint."""
    client = OpenAI()
    
    prompt = f"""Rewrite this resume bullet to match the job requirement.
Use ONLY facts from the EVIDENCE. Do not invent metrics or skills.

REQUIREMENT: {requirement}
ORIGINAL BULLET: {bullet}
EVIDENCE: {evidence}

Rewrite the bullet to:
1. Use active voice and strong verbs
2. Include quantified impact (%, $, X%, improvement)
3. Highlight relevant skills from the requirement
4. Keep it under 150 characters

Return ONLY the rewritten bullet, no explanation."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,  # Low temperature for consistency
        max_tokens=100
    )
    
    return response.choices[0].message.content.strip()
```

**Integration in tailor.py**:
```python
def select_and_rewrite_with_rag(experience, keywords, rag_context=None):
    tailored = []
    for job in experience:
        top_bullets = score_bullets(job["bullets"], keywords)[:3]
        
        rewritten = []
        for bullet in top_bullets:
            # Get evidence for this bullet
            evidence = retrieve_evidence_for_bullet(bullet, rag_context)
            
            # Rewrite with LLM using evidence
            improved = rewrite_with_evidence(
                bullet["text"],
                evidence,
                keywords[0]  # Primary requirement
            )
            rewritten.append(improved)
        
        job_data = {**job, "selected_bullets": rewritten}
        tailored.append(job_data)
    
    return tailored
```

**Changes**:
- [ ] Create `src/rag/llm_rewriter.py` with `rewrite_with_evidence()`
- [ ] Update `tailor.py` to use LLM rewriter
- [ ] Add OpenAI API key configuration
- [ ] Implement evidence extraction from retrieved context
- [ ] Add error handling for LLM failures
- [ ] Update tests with mock LLM responses

**Impact**: AI-powered bullet rewriting with evidence constraints

---

### D) Reranking (Optional but Recommended)

**Current**: Top-K by similarity score only
```python
# Just return top-K by cosine similarity
top_results = sorted_docs[:top_k]
```

**Target**: Rerank with cross-encoder for better quality
```python
from sentence_transformers import CrossEncoder

class Retriever:
    def __init__(self, vector_store_path):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    def retrieve(self, query: str, top_k: int = 10):
        # Step 1: Get top-2K with FAISS
        candidates = self._faiss_search(query, top_k=20)
        
        # Step 2: Rerank with cross-encoder
        pairs = [[query, doc.content] for doc, _ in candidates]
        scores = self.reranker.predict(pairs)
        
        # Step 3: Return top-K reranked results
        reranked = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        return [(doc, float(score)) for (doc, _), score in reranked]
```

**Changes**:
- [ ] Add `sentence-transformers` cross-encoder model
- [ ] Update `Retriever.retrieve()` to use reranking
- [ ] Add reranking configuration (top_k_candidates)
- [ ] Update tests for reranking

**Impact**: Better quality top-K results, more relevant to query

---

## Implementation Order

### Phase 1A: Real Embeddings (2-3 hours)
1. Add `sentence-transformers` dependency
2. Update `RAGIndexer` to use SentenceTransformer
3. Update `Retriever` to use SentenceTransformer
4. Re-index documents
5. Update tests

### Phase 1B: FAISS Integration (2-3 hours)
1. Add `faiss-cpu` dependency
2. Update `RAGIndexer` to build FAISS index
3. Update `Retriever` to use FAISS search
4. Update tests

### Phase 1C: LLM Rewriting (3-4 hours)
1. Create `src/rag/llm_rewriter.py`
2. Update `tailor.py` to use LLM rewriter
3. Add OpenAI configuration
4. Update tests with mock responses

### Phase 1D: Reranking (1-2 hours)
1. Add cross-encoder model
2. Update `Retriever.retrieve()` for reranking
3. Update tests

### Phase 1E: Testing & Documentation (2-3 hours)
1. Update all tests
2. Update documentation
3. Run full test suite
4. Create upgrade guide

---

## Dependencies to Add

```bash
pip install sentence-transformers faiss-cpu
```

Or in `requirements.txt`:
```
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4  # or faiss-gpu for production
```

---

## Configuration Changes

### RAG Config (src/rag/config.py)
```python
RAG_CONFIG = {
    # Embedding
    'embedding_model': 'all-MiniLM-L6-v2',
    'embedding_dim': 384,
    
    # Vector Store
    'vector_store_type': 'faiss',  # Changed from 'local'
    'vector_store_path': 'data/rag/vector_store.faiss',
    'metadata_path': 'data/rag/metadata.json',
    
    # Retrieval
    'retrieval_top_k': 10,
    'retrieval_top_k_candidates': 20,  # For reranking
    'similarity_threshold': 0.35,
    
    # Reranking
    'use_reranking': True,
    'reranker_model': 'cross-encoder/ms-marco-MiniLM-L-6-v2',
    
    # LLM Rewriting
    'use_llm_rewriting': True,
    'llm_model': 'gpt-4o-mini',
    'llm_temperature': 0.2,
}
```

---

## Testing Strategy

### Unit Tests
- [ ] Test real embeddings produce semantic similarity
- [ ] Test FAISS index creation and search
- [ ] Test LLM rewriter with mock responses
- [ ] Test reranking improves quality

### Integration Tests
- [ ] End-to-end: Parse JD → Retrieve → Rerank → Rewrite
- [ ] Compare skeleton vs production RAG quality
- [ ] Benchmark performance (speed, accuracy)

### Validation
- [ ] Semantic similarity > 0.7 for relevant documents
- [ ] Reranking improves top-1 accuracy by > 10%
- [ ] LLM rewriting produces valid bullets
- [ ] All 421 existing tests still pass

---

## Success Criteria

- [ ] Real embeddings: Semantic similarity works correctly
- [ ] FAISS: Search is O(log n) and accurate
- [ ] LLM Rewriting: Produces evidence-constrained bullets
- [ ] Reranking: Improves top-K quality by > 10%
- [ ] All tests pass (421 + new tests)
- [ ] Performance: Retrieval < 100ms for 1000 documents
- [ ] Documentation: Updated with production RAG details

---

## Rollback Plan

If any component fails:
1. Keep JSON vector store as fallback
2. Keep hash-based embeddings as fallback
3. Keep regex rewriter as fallback
4. Feature flags to enable/disable each component

---

## Next Steps

1. **Decide**: Do you want to upgrade Phase 1 to production RAG?
2. **Prioritize**: Which components are most important?
   - A) Real embeddings (critical for semantic search)
   - B) FAISS (critical for scalability)
   - C) LLM rewriting (critical for quality)
   - D) Reranking (nice-to-have for quality)
3. **Timeline**: How much time do you want to spend?
4. **Resources**: Do you have OpenAI API access for LLM rewriting?

---

## Recommendation

**Implement in this order**:
1. **A + B** (Real embeddings + FAISS) - 4-6 hours
   - Enables semantic search and scalability
   - Foundation for everything else
2. **C** (LLM rewriting) - 3-4 hours
   - Enables AI-powered bullet improvement
   - Requires OpenAI API
3. **D** (Reranking) - 1-2 hours
   - Optional but recommended for quality
   - Low effort, high impact

**Total**: 8-12 hours to production-ready RAG

This would make Phase 1 a **complete, production-ready RAG system** before moving to Phase 2 (LoRA fine-tuning).

