# Conventional Commits

Official specification: https://www.conventionalcommits.org/en/v1.0.0/

## Overview

Conventional Commits is a lightweight convention for commit messages that provides an easy set of rules for creating an explicit commit history. It integrates seamlessly with Semantic Versioning.

## Commit Message Format

### Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Example

```
feat(api): add user authentication endpoint

Implements JWT-based authentication with refresh tokens.
Includes password hashing using bcrypt.

Refs: #123, spec-001
BREAKING CHANGE: Authorization header now required for all API calls
```

## Commit Types

### Standard Types

| Type | Description | Changelog Category | SemVer |
|------|-------------|-------------------|---------|
| `feat` | New feature | Added | MINOR |
| `fix` | Bug fix | Fixed | PATCH |
| `docs` | Documentation only | - (skip) | - |
| `style` | Code style (formatting, missing semi colons, etc.) | - (skip) | - |
| `refactor` | Code change that neither fixes a bug nor adds a feature | - (skip) | - |
| `perf` | Performance improvement | Changed | PATCH |
| `test` | Adding or correcting tests | - (skip) | - |
| `chore` | Changes to build process or auxiliary tools | - (skip) | - |
| `build` | Changes to build system or dependencies | - (skip or Changed) | PATCH |
| `ci` | Changes to CI configuration | - (skip) | - |

### Extended Types (Commonly Used)

| Type | Description | Changelog Category | SemVer |
|------|-------------|-------------------|---------|
| `security` | Security fix or improvement | Security | PATCH |
| `revert` | Reverts a previous commit | Fixed or Removed | Depends |
| `deprecated` | Mark feature as deprecated | Deprecated | MINOR |
| `removed` | Remove feature | Removed | MAJOR |

## Scopes

Optional parenthesized scope after type:

### Examples

```
feat(auth): add OAuth2 provider
fix(api): correct validation error messages
perf(database): optimize query with indexes
docs(readme): update installation instructions
```

### Scope Guidelines

- **Lowercase**: Use lowercase for scopes
- **Component-based**: `feat(api)`, `fix(ui)`, `perf(database)`
- **Feature-based**: `feat(user-profile)`, `fix(checkout)`
- **Consistent**: Use same scope names throughout project

### Special Scopes

- **No scope**: Affects multiple areas or is global
- **\***: Affects everything (e.g., `chore(*): upgrade dependencies`)

## Description

### Rules

- **Lowercase**: Start with lowercase letter
- **No period**: Don't end with period
- **Imperative mood**: "add" not "adds" or "added"
- **Concise**: 50 characters or less if possible
- **Clear**: Describe what, not how

### Good Examples

```
feat: add dark mode toggle
fix: prevent crash on invalid input
perf: reduce bundle size by 20%
docs: add API authentication guide
```

### Bad Examples

```
feat: Added Dark Mode Toggle. (capitalized, past tense, period)
fix: bug (not specific)
perf: made it faster (vague)
chore: stuff (meaningless)
```

## Body

Optional detailed explanation after blank line.

### When to Include Body

- **Complex changes**: Explain the "why"
- **Breaking changes**: Migration instructions
- **Context**: Background that helps reviewers
- **Alternatives considered**: Design decisions

### Example

```
refactor(auth): migrate from sessions to JWT

Sessions were causing scaling issues with multiple servers.
JWT tokens allow stateless authentication and better horizontal scaling.

Tokens expire after 24 hours and include user ID and roles.
Refresh tokens stored in httpOnly cookies for security.
```

## Footers

Optional metadata after body.

### Common Footers

```
Refs: #123
Closes: #456
BREAKING CHANGE: description
Co-authored-by: Name <email@example.com>
Spec: 001-task-api
ADR: 003-database-choice
```

### Breaking Changes

**Required format:**
```
BREAKING CHANGE: description of what broke and how to migrate
```

**Alternative notation:**
```
feat!: add new API endpoint

! after type indicates breaking change
```

### Issue References

```
Refs: #123
Closes: #456, #789
Fixes: #321
Related to: #111
```

### Custom Footers (Spec-Driven Development)

```
Spec: 001-task-api
ADR: 003-database-choice
Feature: user-authentication
PHR: 42
Implements: spec-001-task-api
See: history/adr/003-database-choice.md
```

## Mapping to Changelog

### Direct Mapping

```
feat(api): add user search endpoint
↓
### Added
- User search API endpoint
```

### Grouping Related Commits

```
feat(auth): add login endpoint
feat(auth): add logout endpoint
feat(auth): add token refresh
↓
### Added
- Authentication system with login, logout, and token refresh
```

### User-Facing Translation

```
refactor(ui): migrate to new component library
(skip - internal change)

perf(api): add caching layer
↓
### Changed
- Improved API response times with intelligent caching
```

## Parsing Conventional Commits

### Regex Pattern

```python
import re

pattern = r'^(?P<type>\w+)(?:\((?P<scope>[\w-]+)\))?(?P<breaking>!)?:\s+(?P<description>.+)$'

commit_message = "feat(api)!: add user endpoint"
match = re.match(pattern, commit_message)

if match:
    type = match.group('type')           # "feat"
    scope = match.group('scope')         # "api"
    breaking = match.group('breaking')    # "!"
    description = match.group('description')  # "add user endpoint"
```

### Extracting Footer References

```python
def extract_footer_references(body):
    """Extract spec, ADR, and issue references from commit body."""
    refs = {
        'specs': [],
        'adrs': [],
        'issues': [],
        'breaking': None
    }

    for line in body.split('\n'):
        # Spec references
        if line.startswith('Spec:'):
            refs['specs'].extend([s.strip() for s in line[5:].split(',')])

        # ADR references
        if line.startswith('ADR:'):
            refs['adrs'].extend([a.strip() for a in line[4:].split(',')])

        # Issue references
        if line.startswith(('Refs:', 'Closes:', 'Fixes:')):
            issues = re.findall(r'#(\d+)', line)
            refs['issues'].extend(issues)

        # Breaking change
        if line.startswith('BREAKING CHANGE:'):
            refs['breaking'] = line[16:].strip()

    return refs
```

## Semantic Versioning Integration

### Version Bump Rules

```
Given version 1.2.3:

Any BREAKING CHANGE → 2.0.0 (MAJOR)
Any feat: → 1.3.0 (MINOR)
Only fix:, perf:, security: → 1.2.4 (PATCH)
Only docs:, test:, chore: → no version change
```

### Analyzing Commits Since Last Tag

```bash
# Get all commit types since last tag
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%s" | \
  grep -E '^(feat|fix|perf|security|BREAKING)' | \
  cut -d: -f1

# Check for breaking changes
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%B" | \
  grep -q "BREAKING CHANGE:" && echo "MAJOR" || echo "MINOR or PATCH"
```

## Examples

### Feature Addition

```
feat(tasks): add priority field to tasks

Tasks can now be marked as low, medium, or high priority.
Priority affects sorting in the task list view.

Refs: #234
Spec: 001-task-api
```

### Bug Fix

```
fix(auth): prevent token expiry race condition

Fixed issue where tokens could expire during request processing,
causing intermittent 401 errors for long-running requests.

Closes: #567
```

### Breaking Change

```
feat(api)!: change response format to camelCase

BREAKING CHANGE: All API responses now use camelCase instead of snake_case.

Migration: Update your client code to handle camelCase keys.
Before: { user_name: "john" }
After: { userName: "john" }

See docs/v2-migration.md for full migration guide.

Refs: #890
ADR: 012-api-naming-conventions
```

### Performance Improvement

```
perf(database): add indexes to frequently queried columns

Added composite index on (user_id, created_at) for tasks table.
Reduces query time from 2.3s to 45ms for user task lists.

Refs: #456
```

### Security Fix

```
security(auth): fix SQL injection in login endpoint

Replaced string concatenation with parameterized queries.
Affects all endpoints using raw SQL queries.

CVE: Assigned CVE-2024-12345
Severity: HIGH
```

### Documentation

```
docs(api): add authentication examples

Added examples for OAuth2, JWT, and API key authentication.
Includes code samples in Python, JavaScript, and curl.

Closes: #123
```

### Refactoring (Skip in Changelog)

```
refactor(services): extract common validation logic

Created shared ValidationService to reduce code duplication.
No functional changes, pure refactoring.

No spec/issue reference - internal improvement
```

## Best Practices

### DO

- **Be consistent**: Follow convention throughout project
- **Be specific**: Detailed descriptions help reviewers
- **Reference issues**: Link commits to work tracking
- **Explain breaking changes**: Include migration guide
- **Use imperative mood**: "add" not "added"
- **Keep first line short**: 50-72 characters

### DON'T

- **Mix types**: One commit = one type
- **Be vague**: "fix stuff" or "update things"
- **Skip breaking change notation**: Always mark breaking changes
- **Use past tense**: "added feature" → "add feature"
- **Include ticket numbers in description**: Use footer instead

### Commit Atomicity

Each commit should be:
- **Focused**: One logical change
- **Complete**: All related changes included
- **Testable**: Can be tested independently
- **Revertible**: Can be reverted without breaking others

## Tools

### Commit Message Validation

**commitlint**: Lint commit messages
```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

**commitizen**: Interactive commit message builder
```bash
npm install --save-dev commitizen cz-conventional-changelog
```

### Changelog Generation

**standard-version**: Automate versioning and changelog
```bash
npm install --save-dev standard-version
npx standard-version
```

**conventional-changelog**: Generate changelog from commits
```bash
npm install --save-dev conventional-changelog-cli
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

## Git Hooks

### Pre-commit Hook (validate message)

`.git/hooks/commit-msg`:
```bash
#!/bin/sh
commit_msg=$(cat "$1")

if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|build|ci)(\(.+\))?!?: .+"; then
    echo "ERROR: Commit message doesn't follow Conventional Commits format"
    echo "Format: <type>[optional scope]: <description>"
    echo "Example: feat(api): add user endpoint"
    exit 1
fi
```

## References

- Conventional Commits: https://www.conventionalcommits.org/
- Semantic Versioning: https://semver.org/
- Angular Commit Guidelines: https://github.com/angular/angular/blob/main/CONTRIBUTING.md
- Commitizen: https://commitizen-tools.github.io/commitizen/
- Commitlint: https://commitlint.js.org/
