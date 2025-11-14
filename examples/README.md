# Alternative Inference Engine Examples

This directory contains production-ready implementations of three alternative inference engines for the NL-to-SQL translator, offering significant performance improvements over the baseline Ollama implementation.

## 📁 Files

- **`llama_cpp_translator.py`** - Direct llama.cpp implementation (2-3x faster)
- **`transformers_translator.py`** - HuggingFace Transformers with optimizations (1.5-2.5x faster)
- **`vllm_translator.py`** - Berkeley's vLLM for production (5-10x faster)
- **`compare_engines.py`** - Benchmark tool to compare all engines
- **`README.md`** - This file

## 🎯 Quick Start

### 1. Install Dependencies

#### Option A: Using UV (Recommended)

No installation needed! Use `uv run --with`:

```bash
# llama.cpp (easiest, good performance)
uv run --with llama-cpp-python python llama_cpp_translator.py

# Transformers (flexible, many optimizations)
uv run --with transformers --with torch --with accelerate python transformers_translator.py

# vLLM (best performance, requires GPU)
uv run --with vllm python vllm_translator.py

# Compare all (auto-installs what's needed)
uv run --with llama-cpp-python --with transformers --with vllm python compare_engines.py
```

#### Option B: Traditional pip

```bash
# llama.cpp (easiest, good performance)
pip install llama-cpp-python

# Transformers (flexible, many optimizations)
pip install transformers torch accelerate bitsandbytes

# vLLM (best performance, requires GPU)
pip install vllm
```

### 2. Download Model

#### For llama.cpp:
```bash
# Download GGUF format model
cd ~/.ollama/models
wget https://huggingface.co/microsoft/phi-4/resolve/main/phi-4-q4_k_m.gguf

# Or convert existing Ollama model to GGUF
ollama show phi4:latest --modelfile
```

#### For Transformers and vLLM:
Models are automatically downloaded from HuggingFace on first use.

### 3. Run Examples

#### llama.cpp:
```bash
cd examples
python llama_cpp_translator.py
# Will prompt for model path
```

#### Transformers:
```bash
python transformers_translator.py
# Uses microsoft/phi-2 by default
```

#### vLLM:
```bash
python vllm_translator.py
# Requires CUDA GPU
```

#### Compare All Engines:
```bash
python compare_engines.py
# Runs same queries on all available engines
```

## 📊 Expected Performance

Based on analysis in `docs/inference_engine_comparison.md`:

| Engine | Speedup | Avg Latency | Best For |
|--------|---------|-------------|----------|
| **Ollama** (baseline) | 1x | 23.8s | Easy setup, local development |
| **llama.cpp** | 2-3x | 8-12s | Quick wins, minimal migration |
| **Transformers** | 1.5-2.5x | 10-15s | Flexibility, experimentation |
| **vLLM** | 5-10x | 2-5s | Production, high throughput |

## 🔧 Configuration Examples

### llama.cpp - Balanced
```python
translator = LlamaCppTranslator(
    model_path="~/.ollama/models/phi4.gguf",
    n_gpu_layers=-1,  # Use all GPU
    n_ctx=4096,       # Context size
    n_batch=512       # Batch size
)
```

### Transformers - Optimized
```python
translator = TransformersTranslator(
    model_name="microsoft/phi-2",
    use_4bit=True,           # 4-bit quantization
    use_flash_attention=True, # FlashAttention v2
    compile_model=True       # Torch compile
)
```

### vLLM - Production
```python
translator = VLLMTranslator(
    model_name="microsoft/phi-2",
    tensor_parallel_size=2,  # Multi-GPU
    gpu_memory_utilization=0.9
)
```

## 📈 Benchmarking

To benchmark an engine against your existing setup:

```bash
# Run current benchmark (Ollama)
cd ..
python src/benchmark.py

# Run with alternative engine
cd examples
python compare_engines.py

# Results saved to ../logs/engine_comparison_*.md
```

## 🚀 Integration Steps

To integrate an alternative engine into your project:

1. **Copy translator file to `src/`**
   ```bash
   cp examples/llama_cpp_translator.py src/
   ```

2. **Update `src/cli.py`** to use new translator:
   ```python
   from llama_cpp_translator import LlamaCppTranslator
   translator = LlamaCppTranslator(model_path="...")
   ```

3. **Update `src/benchmark.py`** similarly

4. **Run benchmarks** to verify improvement

5. **Update `.env`** with new configuration

## 💡 Recommendations

### For Immediate Improvement (Week 1)
→ **Use llama.cpp**
- 2-3x speedup with minimal code changes
- Same GGUF models as Ollama
- Drop-in replacement

### For Experimentation (Week 2-3)
→ **Try Transformers**
- Most flexible
- Test different optimizations
- Easy to switch models

### For Production (Week 4+)
→ **Deploy with vLLM**
- 5-10x speedup
- Built for scale
- Best throughput

## 🔍 Troubleshooting

### llama.cpp
**Issue:** Model not found
```bash
# Check Ollama model location
ollama list
ollama show phi4:latest --modelfile

# Download GGUF separately
wget https://huggingface.co/.../model.gguf
```

### Transformers
**Issue:** Out of memory
```python
# Enable 4-bit quantization
use_4bit=True

# Reduce context size
model_kwargs['max_length'] = 2048
```

### vLLM
**Issue:** CUDA out of memory
```python
# Reduce GPU memory usage
gpu_memory_utilization=0.7

# Reduce max tokens
max_model_len=2048
```

## 📚 Additional Resources

- **Performance Analysis:** `../docs/performance_considerations.md`
- **Engine Comparison:** `../docs/inference_engine_comparison.md`
- **Current Benchmarks:** `../logs/benchmark_*.json`
- **Documentation:** `../docs/`

## 🤝 Contributing

To add a new inference engine:

1. Create `new_engine_translator.py` following the pattern
2. Implement `translate()` method returning `TranslationResponse`
3. Add to `compare_engines.py`
4. Update this README
5. Document expected performance

## ⚠️ Requirements

- **Python:** 3.11+
- **GPU:** Recommended for best performance
  - llama.cpp: Optional (CPU works, slower)
  - Transformers: Optional (CPU works, slower)
  - vLLM: Required (CUDA 11.8+ or 12.1+)
- **Memory:** 
  - 8GB+ RAM minimum
  - 16GB+ GPU memory for vLLM

## 📝 License

Same as parent project.

## 🆘 Support

For issues or questions:
1. Check `../docs/inference_engine_comparison.md`
2. Review troubleshooting section above
3. Check engine-specific documentation
4. Open an issue with benchmark results
