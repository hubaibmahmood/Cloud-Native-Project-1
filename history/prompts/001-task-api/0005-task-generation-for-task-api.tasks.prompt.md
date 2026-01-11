---
id: 0005
title: Task generation for Task API
stage: tasks
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-task-api
branch: 001-task-api
user: developer
command: /sp.tasks
labels: ["tasks", "tdd", "user-stories", "task-sizing"]
links:
  spec: specs/001-task-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-task-api/tasks.md
tests:
  - 15 test tasks generated (contract and integration tests per TDD requirement)
---

## Prompt

User invoked the `/sp.tasks` command with context: "make sure they are sized between 20 - 30 minutes"

The command workflow required:
1. Running check-prerequisites.sh to get feature directory
2. Loading design documents (spec.md, plan.md, data-model.md, contracts/, research.md, quickstart.md)
3. Extracting user stories with priorities (P1, P2, P3) from spec.md
4. Mapping entities and endpoints to user stories
5. Generating tasks organized by user story with TDD workflow (tests first, then implementation)
6. Ensuring each task is sized for 20-30 minutes of focused work
7. Creating dependency graph and parallel execution opportunities
8. Validating task completeness with strict checklist format

## Response snapshot

Successfully generated tasks.md with 47 tasks organized into 6 phases, sized for 20-30 minutes each.

**Task Organization**:

**Phase 1: Setup** (3 tasks, ~1 hour)
- T001-T003: Initialize project with UV, install production/dev dependencies

**Phase 2: Foundational** (6 tasks, ~3 hours)
- T004-T009: Database connection, logging, FastAPI app, pytest config, environment setup
- CRITICAL blocking phase - no user stories can start until complete

**Phase 3: User Story 1 - Create and Retrieve Tasks (P1)** (14 tasks, ~5 hours) 🎯 MVP
- Tests (T010-T015): 6 contract and integration tests written FIRST (Red phase)
  - Contract tests: Model creation, validation failures
  - Integration tests: POST /tasks, GET /tasks/{id}, GET /tasks list, filtering
- Implementation (T016-T023): Task model (11 fields), schemas, service, endpoints
- Fields covered: id, title, description, status, priority, due_date, tags, estimated_hours, version, created_at, updated_at
- Filtering: By status, priority, tag with pagination

**Phase 4: User Story 2 - Update Existing Tasks (P2)** (11 tasks, ~3 hours)
- Tests (T024-T028): 5 integration tests for PATCH endpoint and optimistic locking
  - Single field update, multiple field update, conflict detection (409), error cases (404/412)
- Implementation (T029-T034): Update service with version checking, PATCH endpoint, error handling, logging

**Phase 5: User Story 3 - Delete Tasks (P3)** (7 tasks, ~1.5 hours)
- Tests (T035-T037): 3 integration tests for DELETE endpoint
  - Delete success (204), verification (404 after delete), error cases
- Implementation (T038-T041): Delete service, DELETE endpoint, logging

**Phase 6: Polish & Cross-Cutting Concerns** (6 tasks, ~2 hours)
- T042-T047: Unit tests for validation/locking logic, coverage verification, acceptance validation, code quality, README

**Total**: 47 tasks, ~15.5 hours estimated for complete feature

**Task Format Validation**: All tasks follow strict checklist format:
- ✅ Checkbox: `- [ ]`
- ✅ Task ID: Sequential (T001-T047)
- ✅ [P] marker: 18 tasks marked as parallelizable
- ✅ [Story] label: US1 (14 tasks), US2 (11 tasks), US3 (7 tasks)
- ✅ File paths: Every task includes exact file path

**TDD Workflow**: Tests REQUIRED per FR-017 and SC-009
- 15 test tasks total (6 for US1, 5 for US2, 3 for US3, 2 unit tests)
- Tests written FIRST (Red phase), then implementation (Green phase)
- Explicit instructions to verify tests FAIL before implementing

**Dependencies**:
- Setup → Foundational → User Stories (parallel) → Polish
- US2 and US3 can start after US1's Task model (T016) completes
- 18 tasks marked [P] for parallel execution within phases

**MVP Scope**: Setup + Foundational + US1 = 23 tasks (~9 hours)

**Incremental Delivery Strategy**:
1. Foundation (~4 hours)
2. US1 MVP (~5 hours) - Deploy with create/retrieve
3. US2 (~3 hours) - Add update with optimistic locking
4. US3 (~1.5 hours) - Add delete
5. Polish (~2 hours) - Final validation

**Parallel Team Strategy**: 3 developers can complete in ~6-7 hours (vs 15.5 solo)

## Outcome

- ✅ Impact: Generated complete actionable task breakdown for Task Management API with 47 tasks sized 20-30 minutes each. Organized by user story (P1/P2/P3) enabling independent implementation and testing. TDD workflow enforced with tests written first. Clear MVP path (23 tasks, 9 hours) and incremental delivery strategy. 18 tasks marked for parallel execution.
- 🧪 Tests: 15 test tasks generated (6 contract/integration for US1, 5 integration for US2, 3 integration for US3, 2 unit tests for polish). Tests written FIRST per TDD requirement (FR-017, SC-009). Explicit Red-Green-Refactor cycle documented.
- 📁 Files: 1 file created - specs/001-task-api/tasks.md (47 tasks across 6 phases with dependencies, parallel opportunities, MVP scope, time estimates)
- 🔁 Next prompts: Begin implementation starting with Phase 1 Setup (T001-T003). Use `/sp.implement` or manually execute tasks following TDD workflow. Consider creating ADRs for architectural decisions before implementation.
- 🧠 Reflection: Task sizing constraint (20-30 minutes) effectively breaks down complex implementation into manageable chunks. TDD structure ensures test coverage from the start. User story organization enables true incremental delivery - each story is independently testable and deployable. Foundational phase properly identified as blocker. Parallel opportunities well-marked (18 tasks with [P]). Task format validation confirms all 47 tasks follow strict checklist format with IDs, story labels, and file paths.

## Evaluation notes (flywheel)

- Failure modes observed: None. Tasks generated successfully with proper sizing, format, and organization.
- Graders run and results (PASS/FAIL): PASS - All 47 tasks follow checklist format (checkbox, ID, [P] marker, [Story] label, file paths). PASS - Tasks sized 20-30 minutes per user requirement. PASS - TDD workflow enforced with tests first. PASS - User stories properly independent and testable. PASS - Dependencies clearly marked. PASS - MVP scope identified (US1 only).
- Prompt variant (if applicable): Standard /sp.tasks workflow with sizing constraint (20-30 minutes)
- Next experiment (smallest change to try): For future task generation, consider adding estimated complexity markers (Simple/Medium/Complex) alongside time estimates to help developers prioritize and plan. Could also experiment with grouping related tasks into "work packages" that represent a coherent unit of value (e.g., "Task Model + Tests" as one package).
