# Performance Considerations for NL-to-SQL Translation

**Document Version:** 1.0  
**Date:** November 8, 2025  
**Current Performance Baseline:** ~23.8s average, 12.8s min, 84.5s max (P95: 60.9s)

---

## Executive Summary

Based on benchmark results showing an average query translation time of **23.8 seconds** with Phi4 via Ollama, there are significant opportunities for performance optimization. This document analyzes current bottlenecks and proposes actionable improvements across infrastructure, model selection, prompt optimization, and architectural patterns.

**Key Findings:**
- Current median response time: **19.8 seconds** (too slow for interactive use)
- P95 latency: **60.9 seconds** (unacceptable for production)
- High variance: 13.8s standard deviation indicates inconsistent performance
- Simple queries take 12-15s, suggesting overhead beyond model inference

---

## Current Performance Analysis

### Benchmark Results Overview

| Metric | Value | Target | Gap |
|--------|-------|--------|-----|
| Average Time | 23.8s | <2s | **11.9x slower** |
| Median (P50) | 19.8s | <1s | **19.8x slower** |
| P95 | 60.9s | <5s | **12.2x slower** |
| Min Time | 12.8s | <500ms | **25.6x slower** |

### Performance Patterns

1. **Simple queries (12-15s):** Even trivial `SELECT * FROM table` queries take >12s
2. **Complex queries (40-85s):** Queries with JOINs/GROUP BY show 3-7x slower performance
3. **First query anomaly:** Initial query (84s) vs subsequent queries (13s) suggests cold start issues
4. **Weak correlation:** Query complexity shows only moderate impact on response time

### Identified Bottlenecks

1. **Model Size:** Phi4 is a large model (~14B parameters), requiring significant compute
2. **Local Inference:** CPU-based inference on Ollama is inherently slow
3. **Cold Starts:** First inference takes 6x longer (84s vs 13s average)
4. **No Caching:** Repeated/similar queries re-compute from scratch
5. **Prompt Length:** Full schema DDL sent with every request
6. **Serial Processing:** Single-threaded execution model

---

## Optimization Strategies

### 1. Infrastructure & Hosting Alternatives

#### A. GPU Acceleration (Immediate 5-10x improvement)

**Option 1: Local GPU (NVIDIA)**
```bash
# Use Ollama with GPU support
ollama run phi4:gpu

# Or use llama.cpp with GPU
./llama.cpp --model phi4 --gpu-layers 32
```

**Benefits:**
- 5-10x faster inference
- Same model quality
- No API costs

**Costs:**
- Requires NVIDIA GPU (RTX 3060+)
- ~$300-800 hardware investment

**Implementation Effort:** Low (1-2 hours)

---

**Option 2: Cloud GPU Instances**

| Provider | Instance Type | Cost | Expected Latency |
|----------|--------------|------|------------------|
| AWS | g5.xlarge (A10G) | $1.006/hr | 1-3s |
| GCP | n1-standard-4 + T4 | $0.35/hr | 2-4s |
| RunPod | RTX 4090 | $0.34/hr | 1-2s |
| Vast.ai | RTX 3090 | $0.20/hr | 2-3s |

**Recommendation:** RunPod or Vast.ai for cost-effective GPU inference

---

#### B. API-Based Services (Immediate 10-20x improvement)

**Option 1: OpenAI GPT-4-Turbo**
```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    max_tokens=512
)
```

**Pros:**
- Sub-second response times (<500ms typical)
- Excellent SQL generation quality
- Zero infrastructure management
- Scales automatically

**Cons:**
- $0.01 per 1K input tokens (~$0.001-0.002 per query)
- Data sent to third party
- Requires API key

**Cost Estimate:** ~$0.10-0.20 per 100 queries

---

**Option 2: Anthropic Claude (Sonnet 4)**
```python
import anthropic

response = anthropic.Anthropic().messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    max_tokens=512
)
```

**Pros:**
- Fast response times (500-1000ms)
- Strong reasoning for complex SQL
- Better at following instructions

**Cons:**
- Similar costs to OpenAI (~$0.003 per query)
- Requires API key

---

**Option 3: Groq (Ultra-Fast Inference)**
```python
from groq import Groq

response = Groq().chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1
)
```

**Pros:**
- **Blazing fast: 200-500ms response times**
- Free tier available (30 requests/min)
- Open-source models
- No cold starts

**Cons:**
- Model quality slightly lower than GPT-4
- Rate limits on free tier

**Recommendation:** **Groq is ideal for this use case** - fast, affordable, good enough quality

---

#### C. Quantized Models (3-5x improvement)

Use smaller, quantized versions of Phi4:

```bash
# 4-bit quantization (4x smaller, 2-3x faster)
ollama run phi4:q4_0

# 8-bit quantization (2x smaller, 1.5-2x faster)
ollama run phi4:q8_0
```

**Trade-offs:**
- Slight quality degradation (usually acceptable for SQL)
- Faster inference: **5-10 seconds** vs 20s
- Lower memory requirements

**Test Recommendation:** Benchmark `phi4:q4_0` to compare quality vs speed

---

### 2. Model Selection Alternatives

#### Specialized SQL Models

**Option 1: SQLCoder-7B**
- Purpose-built for text-to-SQL
- Smaller (7B parameters vs 14B)
- **Expected performance: 3-8 seconds**

```bash
ollama pull sqlcoder:7b
```

---

**Option 2: CodeLlama-7B-Instruct**
- Strong at structured outputs
- Faster than Phi4
- **Expected performance: 4-10 seconds**

```bash
ollama pull codellama:7b-instruct
```

---

**Option 3: Mistral-7B-Instruct**
- Excellent instruction following
- Very fast inference
- **Expected performance: 3-7 seconds**

```bash
ollama pull mistral:7b-instruct
```

---

**Recommendation:** Test SQLCoder-7B first (purpose-built), then Mistral-7B

---

### 3. Caching Strategies

#### A. Query Result Caching

Cache recent translations to avoid re-computation:

```python
from functools import lru_cache
import hashlib

class CachedTranslator(Translator):
    def __init__(self, *args, cache_size=1000, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}
        self.cache_size = cache_size
    
    def translate(self, prompt: str) -> TranslationResponse:
        # Generate cache key
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        
        # Check cache
        if cache_key in self.cache:
            logger.info("Cache hit - returning cached result")
            cached = self.cache[cache_key]
            cached.response_time = 0.001  # Near-instant
            return cached
        
        # Compute and cache
        result = super().translate(prompt)
        if result.success:
            self.cache[cache_key] = result
            
            # Evict oldest if cache full
            if len(self.cache) > self.cache_size:
                self.cache.pop(next(iter(self.cache)))
        
        return result
```

**Expected Impact:**
- Cache hit rate: 30-50% for typical usage
- Cache hit latency: <1ms
- Overall average improvement: **2-3x faster**

---

#### B. Semantic Similarity Caching

Cache similar queries using embeddings:

```python
from sentence_transformers import SentenceTransformer

class SemanticCachedTranslator(Translator):
    def __init__(self, *args, similarity_threshold=0.95, **kwargs):
        super().__init__(*args, **kwargs)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.query_cache = []
        self.similarity_threshold = similarity_threshold
    
    def find_similar(self, query: str):
        query_emb = self.embedder.encode(query)
        for cached_query, cached_result, cached_emb in self.query_cache:
            similarity = cosine_similarity(query_emb, cached_emb)
            if similarity > self.similarity_threshold:
                return cached_result
        return None
```

**Examples:**
- "show all customers" ≈ "list all customers" (98% similar)
- "count orders" ≈ "how many orders" (94% similar)

**Expected Impact:** 40-60% cache hit rate, **3-4x faster overall**

---

### 4. Prompt Optimization

#### A. Reduce Prompt Size

Current prompt includes full schema DDL (~500 tokens). Optimize:

**Before:**
```
Schema: [Full DDL with CREATE TABLE statements]
Query: show all customers
```

**After:**
```
Tables: customers(id, name, email, created_at), orders(id, customer_id, ...), products(...)
Query: show all customers
```

**Reduction:** 500 tokens → 100 tokens (**5x smaller**)  
**Expected Speedup:** 15-20% faster inference

---

#### B. Few-Shot Examples

Add 2-3 examples to improve quality and reduce tokens needed:

```python
prompt = f"""Convert natural language to SQL.

Examples:
- "show all customers" → SELECT * FROM customers;
- "count orders" → SELECT COUNT(*) FROM orders;

Schema: {schema_compact}
Query: {natural_language_query}
SQL:"""
```

**Expected Impact:**
- Better first-token latency
- More consistent outputs
- Potentially shorter responses

---

#### C. Streaming Responses

For API-based solutions, use streaming to show results faster:

```python
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)

for chunk in response:
    sql_chunk = chunk.choices[0].delta.content
    print(sql_chunk, end='', flush=True)
```

**User Experience:** Feels **3-5x faster** even if total time is similar

---

### 5. Architectural Optimizations

#### A. Keep-Alive / Model Warm-Up

Keep Ollama model loaded in memory:

```bash
# Keep model loaded for 1 hour
ollama run phi4 --keep-alive 60m
```

**Impact:** Eliminates cold starts (**eliminates 84s → 13s jumps**)

---

#### B. Batch Processing

For multiple queries, process in parallel:

```python
from concurrent.futures import ThreadPoolExecutor

def translate_batch(queries: List[str], max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(translator.translate, queries))
    return results
```

**Impact:** 3-4x throughput for batch workloads

---

#### C. Speculative Decoding

Use a smaller "draft" model + larger "verifier":

1. Fast small model generates SQL candidate (2s)
2. Larger model verifies/refines if needed (5s)
3. Accept if confident, else use large model result

**Expected:** **30-40% faster** on average

---

### 6. Hardware Optimizations

#### System Configuration

```bash
# Optimize Ollama for performance
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_FLASH_ATTENTION=1

# CPU optimizations
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
```

#### Metal (macOS) / CUDA (Linux) Acceleration

```bash
# Verify GPU is being used
ollama run phi4 --verbose

# Should show: "Using CUDA" or "Using Metal"
```

---

## Recommended Implementation Roadmap

### Phase 1: Quick Wins (1-2 days, 5-10x improvement)

1. **Switch to Groq API**
   - Free tier, 200-500ms latency
   - Change ~10 lines of code
   - **Expected: 23s → 0.5s (46x faster)**

2. **Implement basic caching**
   - LRU cache for exact matches
   - **Expected: 30% cache hit rate = 1.4x faster**

3. **Enable model keep-alive**
   - Eliminate cold starts
   - **Expected: Eliminate 84s outliers**

**Combined Impact:** **20-30s → 0.5-2s average** ✅

---

### Phase 2: Infrastructure (1 week, production-ready)

1. **Deploy on GPU instance**
   - RunPod or Vast.ai with RTX 3090
   - **Cost:** $0.20/hr = $144/month
   - **Expected: 23s → 2-3s with Phi4**

2. **Implement semantic caching**
   - 50% hit rate expected
   - **Expected: 2-3s → 1-1.5s average**

3. **Optimize prompts**
   - Reduce token count
   - **Expected: 10-15% faster**

**Combined Impact:** **20-30s → 1-2s average** ✅

---

### Phase 3: Production Hardening (2-3 weeks)

1. **Hybrid architecture**
   - Groq for <30 char queries (200ms)
   - GPU Ollama for complex queries (2s)
   - Redis for caching

2. **Failover strategy**
   - Primary: Groq
   - Fallback: Local Ollama
   - Cache: Redis

3. **Load balancing**
   - Multiple Ollama instances
   - Request queuing

**Target:** **<500ms P50, <2s P95** ✅

---

## Cost Comparison

### Monthly Costs (assuming 10,000 queries/month)

| Solution | Setup Cost | Monthly Cost | Avg Latency | Quality |
|----------|------------|--------------|-------------|---------|
| **Current (Ollama CPU)** | $0 | $0 | 23s | Good |
| **Ollama + GPU (Local)** | $500 | $0 | 2-3s | Good |
| **Ollama + Cloud GPU** | $0 | $150 | 2-3s | Good |
| **Groq API** | $0 | $0-5 | 0.3s | Good |
| **OpenAI GPT-4** | $0 | $20 | 0.5s | Excellent |
| **Claude Sonnet** | $0 | $30 | 0.7s | Excellent |
| **Hybrid (Groq + Cache)** | $0 | $0-2 | 0.2s | Good |

**Recommendation:** **Groq API with caching** for best cost/performance ratio

---

## Testing Protocol

Before production deployment, benchmark each optimization:

```bash
# Baseline
./scripts/run_benchmark.sh > baseline.log

# Test Groq
export USE_GROQ=1
./scripts/run_benchmark.sh > groq.log

# Test smaller model
ollama pull mistral:7b-instruct
./scripts/run_benchmark.sh > mistral.log

# Compare
./scripts/analyze_benchmark.sh logs/benchmark_results_baseline.json \
                              logs/benchmark_results_groq.json
```

---

## Monitoring & Metrics

Track these KPIs post-optimization:

1. **P50 latency** (target: <500ms)
2. **P95 latency** (target: <2s)
3. **Cache hit rate** (target: >40%)
4. **Cost per query** (target: <$0.001)
5. **Quality score** (SQL correctness)

---

## Conclusion

**Current state:** 23.8s average latency is **too slow for production**

**Immediate recommendation:** 
1. Switch to **Groq API** (46x faster, free tier available)
2. Add **query caching** (1.4x additional improvement)
3. Enable **model keep-alive** (eliminate cold starts)

**Expected result:** **23s → 0.5s (46x improvement)** with minimal code changes

**Next steps:**
1. Implement Groq integration (2 hours)
2. Add caching layer (4 hours)
3. Run comparative benchmark (1 hour)
4. Deploy to production (2 hours)

**Total implementation time: 1-2 days for 46x performance improvement**

---

## Appendix: Code Examples

### A. Groq Integration

```python
# src/groq_translator.py
from groq import Groq
import os

class GroqTranslator(Translator):
    def __init__(self, model_name="llama-3.1-70b-versatile", timeout=10):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name
        self.timeout = timeout
    
    def translate(self, prompt: str) -> TranslationResponse:
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=512,
                timeout=self.timeout
            )
            
            response_time = time.time() - start_time
            sql_query = response.choices[0].message.content.strip()
            
            # Cleanup markdown
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return TranslationResponse(
                sql_query=sql_query,
                success=True,
                response_time=response_time
            )
        except Exception as e:
            response_time = time.time() - start_time
            return TranslationResponse(
                sql_query="",
                success=False,
                error_message=str(e),
                response_time=response_time
            )
```

### B. Caching Layer

```python
# src/cache.py
import json
import hashlib
from pathlib import Path

class TranslationCache:
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache = {}
    
    def get(self, prompt: str):
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        
        # Check memory
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        
        # Check disk
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                result = json.load(f)
                self.memory_cache[cache_key] = result
                return result
        
        return None
    
    def set(self, prompt: str, result: dict):
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        
        # Save to memory
        self.memory_cache[cache_key] = result
        
        # Save to disk
        cache_file = self.cache_dir / f"{cache_key}.json"
        with open(cache_file, 'w') as f:
            json.dump(result, f)
```

---

**Document Status:** Ready for Review  
**Next Review Date:** After implementing Phase 1 optimizations  
**Owner:** Engineering Team
