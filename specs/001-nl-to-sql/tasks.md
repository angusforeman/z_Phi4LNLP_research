# Tasks: Natural Language to SQL Translation

**Input**: Design documents from `/specs/001-nl-to-sql/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Per constitution (Minimal Test Coverage), only essential tests are included - one test per technical element.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

Single project structure at repository root:
- `src/` - Source code
- `tests/` - Test files

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per constitution's minimal approach

- [ ] T001 Create requirements.txt with ollama-python and pytest dependencies
- [ ] T002 Create README.md with project overview and setup instructions
- [ ] T003 [P] Create src/ directory structure
- [ ] T004 [P] Create tests/ directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Critical**: No user story work can begin until this phase is complete

- [ ] T005 Create predefined e-commerce schema in src/schema.py with customers, orders, products tables
- [ ] T006 Implement schema serialization to SQL DDL format in src/schema.py
- [ ] T007 Implement prompt builder to combine schema context with natural language query in src/prompt_builder.py
- [ ] T008 Verify Ollama installation and Phi4 model availability (explicit validation checkpoint)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Query Translation (Priority: P1) 🎯 MVP

**Goal**: Enable translation of simple English queries to SQL using predefined schema

**Independent Test**: Run "show all customers" and verify it returns "SELECT * FROM customers"

### Test for User Story 1

- [ ] T009 [US1] Create test_basic_translation.py in tests/ with test for simple query translation

### Implementation for User Story 1

- [ ] T010 [US1] Implement Ollama client wrapper in src/translator.py to communicate with Phi4 model
- [ ] T011 [US1] Implement translation logic in src/translator.py to send prompt and extract SQL from response
- [ ] T012 [US1] Implement basic CLI in src/cli.py to accept query argument and call translator
- [ ] T013 [US1] Add error handling for empty queries and model unavailability in src/cli.py
- [ ] T014 [US1] Add response timeout handling (10 seconds) in src/translator.py
- [ ] T015 [US1] Run test_basic_translation.py and verify it passes (validation checkpoint)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. System can translate simple queries like "show all customers" to SQL.

---

## Phase 4: User Story 2 - Complex Query Translation (Priority: P2)

**Goal**: Enable translation of complex queries with joins, aggregations, and filtering

**Independent Test**: Run "show average order value by customer" and verify SQL includes JOIN and GROUP BY

### Test for User Story 2

- [ ] T016 [US2] Create test_complex_queries.py in tests/ with test for aggregation and join queries

### Implementation for User Story 2

- [ ] T017 [US2] Enhance prompt template in src/prompt_builder.py to include relationship information for JOIN context
- [ ] T018 [US2] Add examples of complex queries to prompt template to guide model in src/prompt_builder.py
- [ ] T019 [US2] Test complex query translation with joins and verify accuracy (validation checkpoint)
- [ ] T020 [US2] Test aggregation queries and verify GROUP BY/COUNT/AVG functions generated correctly (validation checkpoint)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. System handles both simple and complex queries.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validation and documentation per constitution requirements

- [ ] T021 [P] Create test_model_connection.py in tests/ to verify Phi4 model responds
- [ ] T022 [P] Create test_schema_context.py in tests/ to verify schema is included in prompts
- [ ] T023 Run all tests with pytest and verify 3 tests pass (validation checkpoint)
- [ ] T024 Test CLI with example queries from quickstart.md and document actual performance
- [ ] T025 Verify response times meet 5-second requirement for 95% of queries (validation checkpoint)
- [ ] T026 Update README.md with actual findings and limitations discovered during testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run parallel to US1 if staffed, but US1 is MVP)
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: MVP - Must complete first. No dependencies on other stories
- **User Story 2 (P2)**: Independent of US1 but builds on same foundation. Can start after Foundational phase

### Within Each User Story

**User Story 1**:
1. Write test first (T009)
2. Implement translator (T010, T011)
3. Implement CLI (T012, T013, T014)
4. Run test and verify (T015)

**User Story 2**:
1. Write test first (T016)
2. Enhance prompt builder (T017, T018)
3. Validate with checkpoints (T019, T020)

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003 and T004 can run in parallel (different directories)

**Phase 2 (Foundational)**:
- All tasks sequential - each builds on previous

**Phase 3 (User Story 1)**:
- All tasks sequential within story

**Phase 4 (User Story 2)**:
- Could run parallel to US1 if team capacity allows (different priority)
- Tasks within US2 are sequential

**Phase 5 (Polish)**:
- T021 and T022 can run in parallel (different test files)

---

## Parallel Example: Setup Phase

```bash
# Launch directory creation together:
Task: "Create src/ directory structure"
Task: "Create tests/ directory structure"
```

## Parallel Example: Polish Phase

```bash
# Launch test file creation together:
Task: "Create test_model_connection.py in tests/"
Task: "Create test_schema_context.py in tests/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T008) - CRITICAL
3. Complete Phase 3: User Story 1 (T009-T015)
4. **STOP and VALIDATE**: Test independently with queries like:
   - "show all customers"
   - "list products"
   - "count orders"
5. Demo/Document findings

**MVP Delivers**: Basic natural language to SQL translation proving the concept works

### Full Implementation

1. Complete MVP (Phases 1-3)
2. Add User Story 2 (Phase 4: T016-T020)
3. **VALIDATE**: Test complex queries like:
   - "show customers with order counts"
   - "average order value by customer"
4. Complete Polish phase (Phase 5: T021-T026)
5. Final validation with all tests passing

### Incremental Delivery

- **Checkpoint 1** (After Phase 2): Foundation ready - schema defined, prompt builder works
- **Checkpoint 2** (After Phase 3): MVP complete - basic translation functional
- **Checkpoint 3** (After Phase 4): Complex queries working - full feature set
- **Checkpoint 4** (After Phase 5): All tests pass - ready for evaluation

---

## Constitution Compliance

### Research Spike Approach ✓
- Focus on proving concept works
- No over-engineering
- MVP delivers core value

### Code Conciseness ✓
- 4 source files (schema.py, prompt_builder.py, translator.py, cli.py)
- 3 test files (per constitution: one per technical element)
- No unnecessary abstraction

### Minimal Dependencies ✓
- Only ollama-python and pytest
- Python standard library for rest

### Explicit Validation Checkpoints ✓
- T008: Verify Ollama and Phi4 available
- T015: Verify basic translation works
- T019, T020: Verify complex queries work
- T023: Verify all tests pass
- T025: Verify performance requirements met

### Minimal Test Coverage ✓
- 3 tests total (one per technical element):
  - Model connectivity
  - Basic translation
  - Schema context injection

### No Unicode Pictures ✓
- Plain text only throughout

---

## Task Summary

- **Total Tasks**: 26
- **Setup**: 4 tasks
- **Foundational**: 4 tasks
- **User Story 1 (MVP)**: 7 tasks
- **User Story 2**: 5 tasks
- **Polish**: 6 tasks
- **Parallel Opportunities**: 4 tasks can run in parallel (marked with [P])
- **MVP Scope**: Phases 1-3 (15 tasks total)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently testable
- Stop at any checkpoint to validate before proceeding
- Document actual performance vs. targets (research spike)
- All file paths are explicit and ready for implementation
