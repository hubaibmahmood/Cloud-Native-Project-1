<!--
Sync Impact Report:
- Version change: Initial → 1.0.0
- Modified principles: N/A (initial constitution)
- Added sections:
  * Core Principles (7 principles)
  * Code Organization Standards
  * Development Workflow
  * Governance
- Removed sections: N/A (initial constitution)
- Templates requiring updates:
  ✅ plan-template.md - Constitution Check section already references this file
  ✅ tasks-template.md - Red-Green-Refactor cycle and test structure align with principles
  ✅ spec-template.md - No changes needed (specification is technology-agnostic)
- Follow-up TODOs: None
-->

# Task Management API Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)

TDD is MANDATORY for all code development:

- Tests MUST be written before implementation code
- Tests MUST fail before implementation code is written to make them pass
- Red-Green-Refactor cycle MUST be strictly followed for every feature and fix
- No code may be committed without accompanying tests that verify the change
- Integration tests are REQUIRED for all user-facing workflows

**Rationale**: TDD ensures code correctness from the outset, creates living documentation of system behavior, enables confident refactoring, and prevents regression. The discipline of writing failing tests first forces clear thinking about requirements before implementation.

### II. Code Quality and Maintainability

All code MUST adhere to quality and maintainability standards:

- MUST follow PEP 8 style guidelines for Python code
- MUST use type hints for all function signatures
- MUST keep functions focused and single-purpose (maximum 20 lines preferred)
- MUST use descriptive variable and function names that convey intent
- MUST avoid premature optimization or over-engineering
- YAGNI (You Aren't Gonna Need It) principle applies: implement only requested features
- MUST use modern Python APIs and avoid deprecated functions

**Modern API Requirements**:
- **DateTime**: ALWAYS use `datetime.now(UTC)` instead of deprecated `datetime.utcnow()`
- Import pattern: `from datetime import datetime, UTC`
- Rationale: `datetime.utcnow()` is deprecated in Python 3.12+ and will be removed

**Rationale**: Clean code reduces cognitive load, eases maintenance, and prevents technical debt. Simplicity enables faster iteration and reduces bugs. Using modern, non-deprecated APIs ensures long-term code compatibility and follows current Python best practices.

### III. Red-Green-Refactor Cycle

For every feature or fix, the following cycle MUST be followed:

1. **Red**: Write a failing test that defines the desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests green
4. **Commit**: Only commit when all tests pass

**Rationale**: This cycle ensures disciplined development, prevents scope creep in individual changes, and maintains a consistently working codebase.

### IV. Testing Requirements

Minimum test coverage expectations MUST be met:

- **Contract Tests**: Core data model operations (Task creation, updates, deletion)
- **Integration Tests**: End-to-end user workflows (add task → view → mark complete)
- **Unit Tests**: Business logic and validation functions
- All tests MUST be runnable via `uv run pytest`
- Tests MUST be deterministic and isolated (no shared state between tests)
- Tests MUST be organized in `tests/` with subdirectories: `contract/`, `integration/`, `unit/`

**Rationale**: Comprehensive testing at multiple levels ensures correctness of individual components, their interactions, and complete user journeys. Deterministic and isolated tests prevent flaky failures and enable parallel execution.

### V. Code Organization

Code MUST be organized with clear separation of concerns:

- Source code in `src/` directory
- Tests in `tests/` directory with subdirectories for contract/integration/unit
- Clear separation: models, services, API/CLI interface layers
- Each module MUST have a single, clear responsibility
- Dependencies MUST be explicitly declared in project configuration

**Rationale**: Organized code structure enables developers to quickly locate relevant code, understand system architecture, and make changes confidently. Clear separation of concerns prevents tangled dependencies and enables independent testing.

### VI. Tooling and Dependency Management

Project dependencies and environment MUST be managed consistently:

- MUST use UV for package management and virtual environment
- MUST initialize projects with `uv init --package .` command
- MUST specify Python 3.12+ as minimum requirement
- MUST declare all dependencies explicitly in project configuration
- MUST include development dependencies (pytest, linters, formatters)
- Project MUST be runnable via UV commands (`uv run`, `uv sync`)

**Rationale**: UV provides fast, deterministic dependency resolution and reproducible environments. Explicit dependency declaration prevents "works on my machine" issues and ensures consistent behavior across development, testing, and production.

### VII. Scalability and Reliability

Code MUST be designed with scalability and reliability in mind:

- Design for concurrent access and thread safety where applicable
- Implement proper error handling with meaningful error messages
- Use appropriate HTTP status codes for API responses
- Handle edge cases explicitly (validation failures, missing data, race conditions)
- Consider performance implications of design decisions
- Plan for data growth and increased load

**Rationale**: Building scalability and reliability from the start is far easier than retrofitting later. Proper error handling and edge case management create robust systems that degrade gracefully under stress.

## Code Organization Standards

### Directory Structure

```
task-management/
├── src/               # Source code
│   ├── models/       # Data models and entities
│   ├── services/     # Business logic layer
│   ├── api/          # API endpoints and routing
│   └── utils/        # Shared utilities
├── tests/            # Test suite
│   ├── contract/     # Contract tests for data models
│   ├── integration/  # End-to-end workflow tests
│   └── unit/         # Unit tests for functions/methods
├── specs/            # Feature specifications and plans
└── history/          # Prompt history and ADRs
```

### Module Responsibilities

- **models/**: Data structures, validation, and persistence logic
- **services/**: Business logic, orchestration, and domain rules
- **api/**: HTTP request/response handling, routing, serialization
- **utils/**: Shared functionality with no business logic

## Development Workflow

### Code Review Standards

All code changes MUST meet these criteria before merge:

- Include tests that verify the change (failing before implementation, passing after)
- Pass all existing tests without modification (unless fixing test bugs)
- Follow style guidelines verified by linters (`ruff`, `black`, `mypy`)
- Have clear commit messages describing the change and its rationale
- Reference the user story, functional requirement, or bug being addressed
- Demonstrate adherence to constitution principles

### Testing Gates

Before any commit:

1. All tests MUST pass (`uv run pytest`)
2. Type checking MUST pass (`uv run mypy src/`)
3. Linting MUST pass (`uv run ruff check src/`)
4. Formatting MUST be applied (`uv run black src/ tests/`)

### Commit Standards

Commit messages MUST follow this format:

```
<type>: <short description>

<detailed explanation if needed>

Refs: <user story or requirement ID>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## Governance

This constitution supersedes all other development practices and preferences. All code reviews, pull requests, and architectural decisions MUST verify compliance with these principles.

### Amendment Process

1. Proposed amendments MUST be documented with rationale
2. Amendments require explicit approval and consensus
3. Constitution version MUST be incremented using semantic versioning:
   - MAJOR: Backward incompatible principle removals or redefinitions
   - MINOR: New principles added or material expansion of guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements
4. All affected templates and documentation MUST be updated to maintain consistency
5. Migration plan MUST be provided for breaking changes

### Complexity Justification

Any violation of constitutional principles MUST be explicitly justified in the implementation plan (`plan.md`) under the "Complexity Tracking" section:

- What principle is being violated
- Why the violation is necessary
- What simpler alternative was rejected and why

### Enforcement

- All pull requests MUST pass constitution compliance review
- Automated gates enforce testing, typing, and style requirements
- Unjustified complexity or principle violations MUST be rejected
- Regular audits ensure ongoing compliance across the codebase

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
