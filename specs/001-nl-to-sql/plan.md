# Implementation Plan: Natural Language to SQL Translation

**Branch**: `001-nl-to-sql` | **Date**: 2025-11-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-nl-to-sql/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a proof-of-concept system that accepts English language queries and translates them to SQL using a locally-hosted Phi4 model. The system uses a predefined database schema as context and returns executable SQL statements. Primary focus is on demonstrating core translation capability with minimal dependencies.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Ollama (local model hosting), ollama-python (API client)  
**Storage**: N/A (predefined schema embedded in code)  
**Testing**: pytest (minimal test coverage per constitution)  
**Target Platform**: Local laptop (Linux/WSL)
**Project Type**: Single project (CLI-based tool)  
**Performance Goals**: <5 seconds response time for 95% of queries (per SC-002)  
**Constraints**: Must run locally on laptop, minimal memory footprint, no external API calls  
**Scale/Scope**: Research spike - single predefined schema, basic SQL operations (SELECT, WHERE, simple conditions)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Research Spike Approach ✓
- Focus on proof-of-concept for NL to SQL translation
- Validate Phi4 model can perform translation task
- No production-ready requirements

### II. Code Conciseness ✓
- Single project structure
- Core functionality: accept query, call model, return SQL
- No additional features beyond basic translation

### III. Minimal Dependencies ✓
- **RESOLVED**: Using Ollama for Phi4 hosting (see research.md)
  - ollama-python: Single Python dependency for model API
  - Ollama binary: System-level installation (one-time setup)
  - Chosen over Transformers (too many deps) and vLLM (overkill)
- Python standard library for CLI
- Pytest for testing (minimal)

### IV. Explicit Validation Checkpoints ✓
- Verify Phi4 model responds before proceeding
- Test schema context is properly included in prompts
- Validate generated SQL syntax before returning

### V. Minimal Test Coverage ✓
- One test for model connectivity
- One test for basic query translation
- One test for schema context injection

### VI. No Unicode Pictures ✓
- Plain text output only
- No decorative characters in documentation or code

## Project Structure

### Documentation (this feature)

```text
specs/001-nl-to-sql/
├── plan.md              # This file
├── research.md          # Phase 0 output (Phi4 hosting comparison)
├── data-model.md        # Phase 1 output (schema structure)
├── quickstart.md        # Phase 1 output (setup instructions)
└── contracts/           # Phase 1 output (if needed for API interface)
```

### Source Code (repository root)

```text
src/
├── schema.py           # Predefined database schema definition
├── translator.py       # Core translation logic (call Phi4)
├── prompt_builder.py   # Construct prompts with schema context
└── cli.py              # Command-line interface

tests/
├── test_model_connection.py    # Verify Phi4 responds
├── test_basic_translation.py   # Test simple queries
└── test_schema_context.py      # Verify schema in prompts

README.md              # Setup and usage
requirements.txt       # Minimal dependencies
```

**Structure Decision**: Single project structure chosen because this is a standalone CLI tool with no frontend, backend separation, or mobile components. All code fits in simple src/ directory per constitution's minimal scope requirement.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification. All constitution principles satisfied.
