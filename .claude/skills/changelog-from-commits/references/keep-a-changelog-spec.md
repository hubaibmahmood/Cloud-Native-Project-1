# Keep a Changelog Specification

Official specification: https://keepachangelog.com/en/1.1.0/

## Overview

Keep a Changelog is a format specification for maintaining a human-readable changelog. It follows these principles:

- **For Humans**: Written by humans, for humans
- **Consistency**: Predictable format for easy scanning
- **Automation-Friendly**: Structured to enable tooling
- **Semantic Versioning**: Works with SemVer version numbers

## Core Principles

### Guiding Principles

1. Changelogs are for humans, not machines
2. There should be an entry for every single version
3. The same types of changes should be grouped
4. Versions and sections should be linkable
5. The latest version comes first
6. The release date of each version is displayed
7. Mention whether you follow Semantic Versioning

### Why Keep a Changelog?

- To make it easier for users and contributors to see precisely what notable changes have been made between each release
- To reduce the effort required to maintain a changelog
- To provide a consistent format that tools can parse

## Format Structure

### Basic Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-01-15

### Added
- New feature description

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

## Change Categories

Use these categories in this order:

### Added
For new features.

**Examples:**
- New API endpoint for user management
- Dark mode theme option
- Export to CSV functionality

### Changed
For changes in existing functionality.

**Examples:**
- Updated authentication flow for better security
- Improved performance of search queries
- Modified API response format (if not breaking)

### Deprecated
For soon-to-be removed features.

**Format:** Include deprecation notice and timeline.

**Examples:**
- `/v1/old-endpoint` deprecated, use `/v2/new-endpoint` instead (removal in v3.0.0)
- Legacy authentication method (OAuth 1.0) will be removed in next major version

### Removed
For now removed features (breaking change).

**Examples:**
- Removed deprecated `/v1/old-endpoint` API
- Removed support for Node.js 12

### Fixed
For any bug fixes.

**Examples:**
- Fixed login timeout on slow connections
- Corrected calculation error in tax totals
- Resolved memory leak in background worker

### Security
For security vulnerability fixes.

**Format:** Reference CVE if applicable, explain impact.

**Examples:**
- Fixed SQL injection vulnerability in search (CVE-2024-12345)
- Updated dependencies to patch security issues
- Improved input validation to prevent XSS attacks

## Version Format

### Version Header

```markdown
## [VERSION] - YYYY-MM-DD
```

**Rules:**
- Version number in [square brackets]
- Space, dash, space
- ISO 8601 date format (YYYY-MM-DD)

**Examples:**
```markdown
## [1.2.3] - 2026-01-11
## [2.0.0-beta.1] - 2025-12-15
## [0.1.0] - 2025-01-01
```

### Unreleased Section

Always maintain an `## [Unreleased]` section at the top for in-progress changes.

```markdown
## [Unreleased]

### Added
- Work in progress features
```

When releasing, move unreleased content to new version section.

### Version Links

At the bottom of the changelog, include comparison links:

```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.2.3...HEAD
[1.2.3]: https://github.com/user/repo/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/user/repo/compare/v1.2.1...v1.2.2
```

**For first release:**
```markdown
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

## Date Format

**Always use ISO 8601 format:** YYYY-MM-DD

**Why?**
- Internationally unambiguous
- Sorts naturally (largest to smallest units)
- ISO standard
- Used by many programming languages

**Examples:**
- ✅ 2026-01-11
- ✅ 2025-12-25
- ❌ 01/11/2026 (ambiguous)
- ❌ 11 Jan 2026 (not sortable)
- ❌ Jan 11, 2026 (verbose)

## Writing Style

### Be Concise but Clear

**Good:**
```markdown
### Fixed
- Login timeout on slow network connections
- Incorrect tax calculation for Canadian provinces
```

**Bad:**
```markdown
### Fixed
- There was an issue where the login would timeout
- Tax calculations were wrong in some cases
```

### Use Present Tense

**Good:**
```markdown
### Added
- Add user profile customization
```

**Bad:**
```markdown
### Added
- Added user profile customization
```

### Write for Users, Not Developers

**Good:**
```markdown
### Added
- Export your data to CSV format
- Dark mode for better nighttime viewing
```

**Bad:**
```markdown
### Added
- Implemented CSVExporter class
- Added theme context provider with dark mode support
```

### Be Specific

**Good:**
```markdown
### Fixed
- Login redirect after session timeout now preserves original URL
```

**Bad:**
```markdown
### Fixed
- Fixed login bug
```

## What to Include

### DO Include

- New features users can see/use
- Changes to existing features
- Bug fixes that affect users
- Security patches
- Breaking changes
- Deprecation notices
- Dependency updates that affect users

### DON'T Include

- Internal refactoring
- Code style changes
- Test additions/modifications
- CI/CD changes
- Documentation updates (unless user-facing)
- Development-only dependency updates

## Special Cases

### Breaking Changes

Mark clearly with warning symbol and migration guide:

```markdown
## [2.0.0] - 2026-01-11

### Breaking Changes ⚠️

- **API Response Format Changed**: All API responses now use camelCase instead of snake_case.
  Migration: Update your client code to handle camelCase keys. See [migration guide](docs/v2-migration.md).

### Removed
- Removed deprecated `/v1/users` endpoint (use `/v2/users` instead)
```

### Pre-release Versions

```markdown
## [2.0.0-beta.1] - 2026-01-10

### Added
- Beta: New dashboard interface (feedback welcome)
```

### Yanked Releases

If a release is pulled/yanked:

```markdown
## [1.2.3] - 2026-01-11 [YANKED]

Critical security vulnerability discovered. Use 1.2.4 instead.
```

## Maintenance

### On Each Release

1. Move `[Unreleased]` content to new version section
2. Update version number and date
3. Update comparison links at bottom
4. Clear `[Unreleased]` section (keep header)

### Continuous Updates

**Option A: Update during development**
- Add entries to `[Unreleased]` as work is completed
- Move to version section on release

**Option B: Generate on release**
- Parse git commits
- Categorize and format
- Review and edit before publishing

## Semantic Versioning Integration

Changelog categories map to SemVer:

| Category | Version Impact |
|----------|----------------|
| Added | MINOR (new features) |
| Changed | MINOR (non-breaking changes) or MAJOR (breaking) |
| Deprecated | MINOR (warning for future) |
| Removed | MAJOR (breaking change) |
| Fixed | PATCH (bug fix) |
| Security | PATCH (security fix) |

## Validation Checklist

- [ ] Follows basic template structure
- [ ] Versions in descending order (newest first)
- [ ] All dates in ISO 8601 format (YYYY-MM-DD)
- [ ] Categories used correctly (Added, Changed, etc.)
- [ ] Each version has a date
- [ ] Comparison links are correct
- [ ] Entries are user-facing, not developer-focused
- [ ] Specific, not vague descriptions
- [ ] Breaking changes clearly marked
- [ ] Links to issues/PRs where relevant

## Tools and Automation

### Compatible Tools

- **git-cliff**: Generate from git commits
- **standard-version**: Automate versioning and CHANGELOG
- **conventional-changelog**: From conventional commits
- **Keep a Changelog CLI**: Parser and validator

### GitHub Integration

GitHub automatically links `CHANGELOG.md` in releases:
- Place at repository root
- Name exactly: `CHANGELOG.md` (not `changelog.md`)
- Keep format consistent for automatic parsing

## References

- Official Site: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/
- ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
- Common Changelog (stricter subset): https://common-changelog.org/
