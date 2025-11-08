# Research: Phi4 Local Hosting Options

**Created**: 2025-11-07  
**Purpose**: Evaluate options for running Microsoft Phi4 model locally on laptop for NL-to-SQL translation

## Research Questions

1. What are the available options for hosting Phi4 locally?
2. Which option best aligns with the research spike constitution (minimal dependencies, simple setup)?
3. What are the memory and performance characteristics of each option?
4. Which option provides the fastest path to validating the concept?

## Option 1: Ollama

### Description
Ollama is a lightweight tool designed to run LLMs locally with minimal setup. It provides a simple API and handles model management automatically.

### Decision Factors

**Pros:**
- Simplest installation (single binary)
- Minimal code required (REST API or Python client)
- Automatic model management and optimization
- Built-in model serving with low memory overhead
- Active community and good documentation
- Python library available: `ollama-python` (single dependency)

**Cons:**
- Additional system service to manage
- Less control over model parameters
- Phi4 may need to be in Ollama's model registry or imported manually

**Memory Requirements**: ~4-8GB for Phi4 (14B parameters)

**Code Complexity**: Minimal
```python
import ollama
response = ollama.generate(model='phi4', prompt=prompt_text)
```

**Setup Steps**:
1. Install Ollama binary
2. Pull/import Phi4 model: `ollama pull phi4`
3. Install Python client: `pip install ollama`
4. Start using (Ollama service auto-starts)

### Constitution Alignment
- ✓ Minimal dependencies (1 Python package)
- ✓ Simple setup (single command install)
- ✓ Fast validation path
- ✓ Minimal code

## Option 2: llama.cpp with Python Bindings

### Description
llama.cpp is a C++ implementation optimized for CPU inference. Python bindings (`llama-cpp-python`) provide access.

### Decision Factors

**Pros:**
- Good CPU performance
- Control over model parameters
- Single Python dependency
- Works with GGUF format models (quantized, smaller memory)
- No separate service needed

**Cons:**
- Manual model file management (download .gguf file)
- Compilation may be needed for optimal performance
- More complex prompt formatting
- Slightly more code than Ollama

**Memory Requirements**: ~3-6GB for Phi4 quantized (Q4/Q5)

**Code Complexity**: Low-Medium
```python
from llama_cpp import Llama
llm = Llama(model_path="./models/phi4-q4.gguf")
output = llm(prompt_text, max_tokens=512)
```

**Setup Steps**:
1. Install Python package: `pip install llama-cpp-python`
2. Download Phi4 GGUF model file manually
3. Point code to model file path

### Constitution Alignment
- ✓ Minimal dependencies (1 Python package)
- ⚠️ Manual model management adds complexity
- ✓ No separate service
- ⚠️ Medium validation path (model download, path config)

## Option 3: Transformers (Hugging Face)

### Description
Hugging Face Transformers library provides direct access to models with auto-downloading.

### Decision Factors

**Pros:**
- Official Phi4 support from Microsoft
- Automatic model downloading from Hugging Face Hub
- Most flexible control over generation
- Familiar API for ML practitioners

**Cons:**
- **Heavy dependencies** (torch, transformers, accelerate, etc.)
- Higher memory usage (full precision by default)
- Slower CPU inference without optimization
- More complex setup and code

**Memory Requirements**: ~8-16GB for full precision, ~4-8GB with quantization

**Code Complexity**: Medium
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-4")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-4")
inputs = tokenizer(prompt_text, return_tensors="pt")
outputs = model.generate(**inputs)
```

**Setup Steps**:
1. Install packages: `pip install transformers torch accelerate`
2. First run auto-downloads model (multi-GB download)
3. Configure generation parameters

### Constitution Alignment
- ✗ **Violates minimal dependencies** (many heavy packages)
- ✗ Complex setup with large downloads
- ✗ Slower validation path
- ⚠️ More code required

## Option 4: vLLM

### Description
High-performance inference server optimized for throughput and latency.

### Decision Factors

**Pros:**
- Best performance for repeated queries
- Advanced batching and caching
- Production-ready features

**Cons:**
- **Overkill for research spike**
- Heavy dependencies
- Complex setup
- GPU-optimized (may not benefit laptop CPU)
- Server architecture adds complexity

**Memory Requirements**: ~8-12GB

**Code Complexity**: High

### Constitution Alignment
- ✗ **Violates research spike principle** (over-engineered)
- ✗ Heavy dependencies
- ✗ Unnecessary complexity
- ✗ Slow validation path

## Decision Matrix

| Criterion | Ollama | llama.cpp | Transformers | vLLM |
|-----------|--------|-----------|--------------|------|
| Setup Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| Minimal Dependencies | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| Code Conciseness | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Validation Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Memory Efficiency | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Constitution Fit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ |

## RECOMMENDATION: Ollama

### Decision
Use **Ollama** for hosting Phi4 locally.

### Rationale
1. **Best constitution alignment**: Minimal dependencies (single Python package), simplest setup, most concise code
2. **Fastest validation path**: Install → Pull model → Test (minutes, not hours)
3. **Research spike appropriate**: No need for Transformers' flexibility or vLLM's performance optimizations
4. **Explicit validation friendly**: Easy to check if model is running (`ollama list`)
5. **Memory efficient**: Optimized serving with reasonable memory footprint
6. **Production path exists**: If spike succeeds, can migrate to other solutions if needed

### Alternatives Considered

**llama.cpp (close second)**:
- Similar simplicity but requires manual model management
- Better if we needed more control over inference parameters
- Rejected because Ollama's automatic model management better fits research spike speed requirement

**Transformers**:
- Too many dependencies for research spike
- Slower setup and validation
- Valuable for production ML work, but overkill here
- Rejected due to constitution violation (minimal dependencies)

**vLLM**:
- Massive over-engineering for a proof-of-concept
- Server architecture adds unnecessary complexity
- Rejected as clearly inappropriate for research spike

## Implementation Details

### Dependencies (Approved)
```
ollama-python==0.3.1  # Single dependency for Ollama API access
pytest==7.4.3         # Testing framework
```

### Environment Verification Steps
Before proceeding with implementation:

1. **Check Ollama installation**:
   ```bash
   ollama --version
   ```

2. **Verify Phi4 model availability**:
   ```bash
   ollama list | grep phi4
   ```
   If not present:
   ```bash
   ollama pull phi4
   ```

3. **Test model response**:
   ```bash
   ollama run phi4 "Test prompt"
   ```

4. **Verify Python client**:
   ```python
   import ollama
   print(ollama.__version__)
   ```

### Performance Expectations
- Cold start: ~2-5 seconds (first query after model load)
- Warm queries: ~1-3 seconds (within 5-second requirement)
- Memory: ~4-8GB RAM usage
- CPU: Will use available cores, may spike to 100% during inference

### Risk Mitigation
- **Risk**: Phi4 not available in Ollama registry
  - **Mitigation**: Can import GGUF model manually with `ollama create`
- **Risk**: Laptop resources insufficient
  - **Mitigation**: Document memory requirements in quickstart, use quantized model if needed
- **Risk**: Response time exceeds 5 seconds
  - **Mitigation**: Acceptable for research spike, document actual performance

## Next Steps

With hosting decision made:
1. Proceed to Phase 1: Design data model for schema representation
2. Create quickstart.md with Ollama setup instructions
3. Design prompt structure for schema context injection
