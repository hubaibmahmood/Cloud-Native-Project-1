# Changelog Examples

Real-world examples showing commit-to-changelog transformations and complete changelog structures.

## Commit → Changelog Transformations

### Example 1: Feature Addition

**Git Commits:**
```
feat(api): add task priority field
feat(api): add priority filtering to task list endpoint
feat(ui): add priority selector to task form
docs: update API docs with priority field
```

**Changelog Entry:**
```markdown
### Added
- Task priority levels (low, medium, high) with filtering support
```

**Notes:**
- Grouped 3 related feature commits
- Skipped docs commit (internal)
- Used user-facing language

---

### Example 2: Bug Fix with Context

**Git Commit:**
```
fix(auth): prevent race condition in token refresh

When multiple requests triggered token refresh simultaneously,
some requests would fail with 401 errors. Now using mutex
to ensure only one refresh happens at a time.

Fixes: #567
```

**Changelog Entry:**
```markdown
### Fixed
- Authentication errors when multiple requests occurred during token refresh [#567](https://github.com/user/repo/issues/567)
```

**Notes:**
- Simplified technical details
- Kept user-facing impact
- Linked to issue

---

### Example 3: Breaking Change

**Git Commit:**
```
feat(api)!: change response format to camelCase

BREAKING CHANGE: All API responses now use camelCase instead of snake_case.
This provides better consistency with JavaScript ecosystem conventions.

Migration: Update client code to handle camelCase keys.
Before: { user_name: "john", created_at: "2024-01-01" }
After: { userName: "john", createdAt: "2024-01-01" }

Refs: #890
ADR: 012-api-naming-conventions
Spec: 001-api-v2
```

**Changelog Entry:**
```markdown
### Breaking Changes ⚠️

- **API Response Format**: All API endpoints now return camelCase instead of snake_case

  **Migration Guide:**
  ```javascript
  // Before (v1)
  const name = response.user_name
  const date = response.created_at

  // After (v2)
  const name = response.userName
  const date = response.createdAt
  ```

  See [v2 Migration Guide](docs/v2-migration.md) for complete details.
  Architecture rationale: [ADR-012](history/adr/012-api-naming-conventions.md)
```

**Notes:**
- Prominent warning symbol
- Detailed migration guide
- Links to ADR and documentation
- Clear before/after examples

---

### Example 4: Performance Improvement

**Git Commits:**
```
perf(database): add composite index on tasks table
perf(api): implement Redis caching for task lists
test: add performance benchmarks for task endpoints
```

**Changelog Entry:**
```markdown
### Changed
- Improved task list loading speed by 85% for projects with 1000+ tasks
```

**Notes:**
- Combined multiple performance commits
- Focused on user-facing impact (speed improvement)
- Provided concrete metric (85%)
- Skipped test commit

---

### Example 5: Security Fix

**Git Commit:**
```
security(api): fix SQL injection in search endpoint

Replaced string concatenation with parameterized queries
in task search functionality. Affects all search endpoints.

Severity: HIGH
CVE: Assigned CVE-2024-12345
Discovered by: John Doe (security@example.com)
```

**Changelog Entry:**
```markdown
### Security
- Fixed SQL injection vulnerability in search functionality (CVE-2024-12345, severity: HIGH)
```

**Notes:**
- Clear security category
- Included CVE number
- Severity level for user awareness
- Didn't expose technical exploit details

---

### Example 6: Multiple Unrelated Fixes

**Git Commits:**
```
fix(ui): correct button alignment in mobile view
fix(api): handle empty array in bulk update endpoint
fix(auth): preserve redirect URL after login timeout
```

**Changelog Entry:**
```markdown
### Fixed
- Button alignment issues on mobile devices
- Bulk update errors when processing empty task lists
- Login redirect now preserves original page URL after session timeout
```

**Notes:**
- Listed separately (unrelated fixes)
- Each entry is specific
- Preserved order from most visible to least

---

## Complete Changelog Examples

### Example A: Initial Release

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-11

### Added
- Complete task management system with create, read, update, and delete operations
- User authentication with JWT tokens
- Task priority levels (low, medium, high)
- Due date reminders via email
- RESTful API with OpenAPI documentation
- Responsive web interface for desktop and mobile

### Security
- Encrypted password storage using bcrypt
- HTTPS-only API endpoints
- CSRF protection on all forms

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

---

### Example B: Feature Release (MINOR)

```markdown
## [Unreleased]

## [1.3.0] - 2026-01-11

### Added
- Task templates for creating recurring tasks quickly
- Bulk task operations (complete, delete, assign) for multiple tasks at once
- Export task lists to CSV and PDF formats
- Task activity timeline showing all changes and comments

### Changed
- Improved search to include task comments and attachments in results
- Updated mobile interface with larger touch targets and simplified navigation
- Enhanced email notifications with rich HTML formatting and direct action links

### Fixed
- Task sorting now correctly handles null due dates
- File uploads no longer fail for files with special characters in names
- Timezone conversion errors for users in GMT+12 to GMT+14 zones

[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/repo/compare/v1.2.0...v1.3.0
```

---

### Example C: Patch Release (PATCH)

```markdown
## [Unreleased]

## [1.2.3] - 2026-01-11

### Fixed
- Memory leak in WebSocket connections causing high CPU usage after 6+ hours [#456](https://github.com/user/repo/issues/456)
- Task notifications not being sent for users with special characters in email addresses [#478](https://github.com/user/repo/issues/478)
- Incorrect task count displayed in sidebar after bulk operations [#489](https://github.com/user/repo/issues/489)

### Security
- Updated authentication library to patch session fixation vulnerability (CVE-2026-1001)

[Unreleased]: https://github.com/user/repo/compare/v1.2.3...HEAD
[1.2.3]: https://github.com/user/repo/compare/v1.2.2...v1.2.3
```

---

### Example D: Major Release with Breaking Changes

```markdown
## [Unreleased]

## [2.0.0] - 2026-01-11

### Breaking Changes ⚠️

- **API Authentication**: All API endpoints now require authentication via JWT tokens in the Authorization header. Previously, some endpoints were publicly accessible.

  **Migration:**
  ```bash
  # Before (v1)
  curl https://api.example.com/tasks

  # After (v2)
  curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/tasks
  ```

- **Minimum Node.js Version**: Now requires Node.js 18.0.0 or higher (previously 14.0.0)

- **Database Schema**: Tasks table structure changed. Run migration script before upgrading.
  ```bash
  npm run migrate:v2
  ```

### Added
- Role-based access control (RBAC) with admin, manager, and user roles
- Team collaboration features with shared task lists
- Real-time updates using WebSockets (no polling needed)
- Advanced task filtering with saved filter presets

### Changed
- Completely redesigned user interface with improved accessibility (WCAG 2.1 AA compliant)
- Task search now uses full-text search for better results
- API rate limiting increased to 1000 requests/hour (previously 100/hour)

### Removed
- Deprecated `/v1/tasks/legacy` endpoint (use `/v2/tasks` instead)
- Removed support for Internet Explorer 11

### Fixed
- All issues from 1.x branch addressed in this release

### Security
- Implemented Content Security Policy (CSP) headers
- Added rate limiting on authentication endpoints to prevent brute force attacks

See [v2 Migration Guide](docs/v2-migration.md) for complete upgrade instructions.

[Unreleased]: https://github.com/user/repo/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/user/repo/compare/v1.9.5...v2.0.0
```

---

### Example E: Pre-release Version

```markdown
## [Unreleased]

## [2.0.0-beta.2] - 2026-01-11

### Added
- Beta: Team collaboration features (feedback welcome via #890)
- Beta: Real-time WebSocket updates (may have stability issues)

### Changed
- Improved performance of beta RBAC implementation
- Updated WebSocket connection handling based on beta.1 feedback

### Fixed
- Beta.1 issue: WebSocket disconnection after 5 minutes [#901](https://github.com/user/repo/issues/901)
- Beta.1 issue: Team member permissions not persisting correctly [#905](https://github.com/user/repo/issues/905)

### Known Issues
- Real-time updates may occasionally duplicate (tracking in #912)
- Team invitation emails sometimes delayed (tracking in #915)

**Note**: This is a beta release. Do not use in production. Database migrations may change before stable 2.0.0 release.

[Unreleased]: https://github.com/user/repo/compare/v2.0.0-beta.2...HEAD
[2.0.0-beta.2]: https://github.com/user/repo/compare/v2.0.0-beta.1...v2.0.0-beta.2
```

---

### Example F: Hotfix Release

```markdown
## [1.2.4] - 2026-01-11

### Fixed
- **CRITICAL**: Authentication bypass vulnerability allowing unauthorized task access (CVE-2026-2001, severity: CRITICAL)

### Security
- Immediate update recommended for all users
- No data breach detected in production systems
- Audit logs available for investigation if needed

**Upgrade Priority**: IMMEDIATE

[1.2.4]: https://github.com/user/repo/compare/v1.2.3...v1.2.4
```

---

## Changelog with Spec/ADR Links

Example showing integration with spec-driven development:

```markdown
## [1.5.0] - 2026-01-11

### Added
- Task automation rules with triggers and actions ([spec-003](specs/003-task-automation/spec.md))
  - Trigger tasks based on due dates, status changes, or custom events
  - Actions include assigning users, sending notifications, or updating fields
  - Visual rule builder in web interface

### Changed
- Migrated to PostgreSQL for better query performance ([ADR-008](history/adr/008-database-migration.md))
  - 5x faster complex queries
  - Better support for full-text search
  - Improved concurrency handling
  - **Note**: Automatic migration from SQLite on first startup

### Fixed
- Task reminder emails now respect user's timezone preference ([#678](https://github.com/user/repo/issues/678))

### Documentation
- Added task automation guide with 15+ example rules ([docs](https://docs.example.com/automation))
- Updated API documentation for new automation endpoints

**Implementation Context:**
- Automation feature: [PHR #42](history/prompts/003-task-automation/042-implementation.md)
- Database decision: [ADR-008](history/adr/008-database-migration.md)
- Performance benchmarks: [Performance Report](docs/performance/2026-01-benchmark.md)

[1.5.0]: https://github.com/user/repo/compare/v1.4.0...v1.5.0
```

---

## Versioning Scenarios

### Scenario 1: Multiple Features + Bug Fixes

**Commits:**
```
feat: add CSV export
feat: add task templates
fix: correct timezone handling
fix: resolve mobile layout issue
```

**Version Bump:** 1.2.0 → 1.3.0 (MINOR - new features present)

---

### Scenario 2: Only Bug Fixes

**Commits:**
```
fix: authentication timeout issue
fix: task sorting with null dates
fix: mobile navigation overlap
```

**Version Bump:** 1.2.0 → 1.2.1 (PATCH - only fixes)

---

### Scenario 3: Breaking Change

**Commits:**
```
feat!: change API response format
feat: add new authentication system
fix: security vulnerability
```

**Version Bump:** 1.2.0 → 2.0.0 (MAJOR - breaking change present)

---

### Scenario 4: Deprecation (No Breaking Yet)

**Commits:**
```
feat: add v2 API endpoints
deprecated: mark v1 endpoints as deprecated
docs: add v1 to v2 migration guide
```

**Version Bump:** 1.9.0 → 1.10.0 (MINOR - deprecation is not breaking)

**Changelog:**
```markdown
## [1.10.0] - 2026-01-11

### Added
- New v2 API endpoints with improved performance and consistency

### Deprecated
- v1 API endpoints will be removed in v2.0.0 (estimated Q2 2026)
  - Use v2 endpoints instead: see [migration guide](docs/v1-to-v2.md)
  - v1 endpoints will continue to work until removal
```

---

## Real Project Examples

### Example: FastAPI Project

```markdown
## [0.2.0] - 2026-01-11

### Added
- Complete task management API with CRUD operations ([spec-001](specs/001-task-api/spec.md))
  - RESTful endpoints for tasks, users, and projects
  - Input validation using Pydantic v2
  - Automatic OpenAPI documentation
- SQLModel integration with Neon PostgreSQL ([ADR-003](history/adr/003-database-choice.md))
  - Async database operations with asyncpg
  - Automatic schema migrations with Alembic
- Environment-aware configuration system
  - Development mode disables prepared statement caching for easier iteration
  - Production mode enables caching for better performance

### Changed
- Database URL validation automatically handles Neon PostgreSQL connection strings
  - Converts `sslmode=` to `ssl=` for asyncpg compatibility
  - Removes unsupported `channel_binding` parameter

### Fixed
- Invalid cached statement errors after schema migrations in development

### Documentation
- Added API authentication guide
- Created development setup instructions for Neon PostgreSQL

[0.2.0]: https://github.com/user/repo/compare/v0.1.0...v0.2.0
```

---

## Templates for Common Scenarios

### Template: Security Update

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Security
- Fixed [vulnerability type] in [component] (CVE-XXXX-YYYY, severity: [LOW|MEDIUM|HIGH|CRITICAL])
  - Impact: [brief description]
  - Affected versions: [version range]
  - **Action Required**: Update immediately

[X.Y.Z]: https://github.com/user/repo/compare/vPREV...vX.Y.Z
```

### Template: Feature Release

```markdown
## [X.Y.0] - YYYY-MM-DD

### Added
- [Feature name] with [key capabilities] ([spec-XXX](specs/XXX/spec.md))
  - [Sub-feature 1]
  - [Sub-feature 2]
  - [Learn more](docs/features/feature-name.md)

### Changed
- [Improvement description] resulting in [measurable benefit]

### Fixed
- [Specific bug fix] [#issue](link)

[X.Y.0]: https://github.com/user/repo/compare/vPREV...vX.Y.0
```

### Template: Breaking Change Release

```markdown
## [X.0.0] - YYYY-MM-DD

### Breaking Changes ⚠️

- **[Change title]**: [What changed]

  **Migration:**
  ```[language]
  // Before
  [old code]

  // After
  [new code]
  ```

  See [migration guide](docs/vX-migration.md) for details.

### Removed
- [Removed feature] (deprecated in vX.Y.Z)

[X.0.0]: https://github.com/user/repo/compare/vPREV...vX.0.0
```

---

## Notes on Transformation

### Key Principles

1. **Group related commits** into coherent changelog entries
2. **Translate technical → user-facing** language
3. **Skip internal changes** (tests, refactoring, docs)
4. **Add context** that's missing from commit messages
5. **Link to resources** (specs, ADRs, issues, docs)
6. **Be specific** about impact and changes

### Common Transformations

| Commit | Changelog |
|--------|-----------|
| `feat(api): implement JWT auth` | "User authentication with secure token-based login" |
| `fix(db): handle race condition` | "Database errors under high concurrent load" |
| `perf: add caching layer` | "Improved response times by 70%" |
| `refactor: extract validation` | *(skip - internal)* |
| `docs: update API guide` | *(skip - unless user-facing)* |
| `test: add integration tests` | *(skip - internal)* |

---

## References

- Keep a Changelog Examples: https://keepachangelog.com/en/1.1.0/#examples
- Conventional Commits: https://www.conventionalcommits.org/
- Semantic Versioning: https://semver.org/
