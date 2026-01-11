---
id: 0001
title: Establish Project Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-task-api
user: mac
command: /sp.constitution
labels: ["constitution", "governance", "tdd", "code-quality", "testing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Template consistency validation
---

## Prompt

TDD is mandatory for all code:
- Tests MUST be written before implementation
- Tests MUST fail before code is written to make them pass
- Red-Green-Refactor cycle MUST be strictly followed
- No code may be committed without accompanying tests
- Integration tests required for user-facing workflows

Code quality and maintainability standards:
- MUST follow PEP 8 style guidelines
- MUST use type hints for all function signatures
- MUST keep functions focused and single-purpose (max 20 lines preferred)
- MUST use descriptive variable and function names
- MUST avoid premature optimization or over-engineering
- YAGNI (You Aren't Gonna Need It) principle applies: only implement requested features
- MUST use modern Python APIs and avoid deprecated functions:
  - **DateTime**: ALWAYS use `datetime.now(UTC)` instead of deprecated `datetime.utcnow()`
  - Import: `from datetime import datetime, UTC`
  - Rationale: `datetime.utcnow()` is deprecated in Python 3.12+ and will be removed in future versions

**Rationale**: Clean code reduces cognitive load, eases maintenance, and prevents technical debt. Simplicity enables faster iteration and reduces bugs. Using modern, non-deprecated APIs ensures long-term code compatibility and follows current Python best practices.

Code organization requirements:
- Source code in `src/` directory
- Tests in `tests/` directory with subdirectories for contract/integration/unit
- Clear separation of concerns: models, services, CLI interface
- Each module MUST have a single, clear responsibility
- Dependencies MUST be explicitly declared in project configuration

Tooling and dependency management:
- MUST use UV for package management and virtual environment
- MUST initialize projects with `uv init --package .` command
- MUST specify Python 3.12+ requirement
- MUST declare all dependencies explicitly
- MUST include development dependencies (pytest, linters)
- Project MUST be runnable via UV commands

### Red-Green-Refactor Cycle

For every feature or fix:
1. **Red**: Write a failing test that defines desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests green
4. Commit only when tests pass

### Code Review Standards

All code changes MUST:
- Include tests that verify the change
- Pass all existing tests
- Follow style guidelines (verified by linters)
- Have clear commit messages describing the change
- Reference the user story or requirement being addressed

### Testing Requirements

Minimum test coverage expectations:
- **Contract Tests**: Core data model operations (Task creation, updates, deletion)
- **Integration Tests**: End-to-end user workflows (add task → view → mark complete)
- **Unit Tests**: Business logic and validation functions
- All tests MUST be runnable via `uv run pytest`
- Tests MUST be deterministic and isolated (no shared state)

The coding should be done keeping in mind that the app should be scalable and reliable

## Response snapshot

Created comprehensive Task Management API Constitution v1.0.0 with:

**7 Core Principles**:
1. Test-Driven Development (NON-NEGOTIABLE) - Red-Green-Refactor cycle mandatory
2. Code Quality and Maintainability - PEP 8, type hints, YAGNI, modern APIs (datetime.now(UTC))
3. Red-Green-Refactor Cycle - Disciplined development workflow
4. Testing Requirements - Contract/Integration/Unit test organization
5. Code Organization - src/, tests/ structure with clear separation of concerns
6. Tooling and Dependency Management - UV, Python 3.12+, explicit dependencies
7. Scalability and Reliability - Concurrent access, error handling, edge cases

**Additional Sections**:
- Code Organization Standards: Directory structure and module responsibilities
- Development Workflow: Code review standards, testing gates, commit standards
- Governance: Amendment process, complexity justification, enforcement rules

**Template Consistency**: Validated compatibility with plan-template.md, tasks-template.md, and spec-template.md

## Outcome

- ✅ Impact: Established constitutional foundation for all project development - defines non-negotiable principles for TDD, code quality, testing, and governance
- 🧪 Tests: Template consistency validated - all templates align with constitutional principles
- 📁 Files: constitution.md (208 lines) with sync impact report
- 🔁 Next prompts: /sp.plan to create implementation architecture adhering to constitution
- 🧠 Reflection: Successfully created comprehensive constitution from detailed user input with no placeholders - all principles actionable and testable

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution complete on first pass
- Graders run and results (PASS/FAIL): Template consistency PASS - all templates compatible
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Apply constitution principles during planning phase to validate effectiveness
