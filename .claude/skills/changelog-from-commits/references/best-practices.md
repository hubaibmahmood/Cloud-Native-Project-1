# Changelog Best Practices

Compiled from Keep a Changelog, industry standards, and real-world experience.

## Core Principles

### 1. Write for Users, Not Developers

Changelogs are **user-facing documentation**, not development logs.

**Good (User-Focused):**
```markdown
### Added
- Export your task list to CSV format
- Dark mode for comfortable nighttime viewing
- Email notifications when tasks are due
```

**Bad (Developer-Focused):**
```markdown
### Added
- Implemented CSVExporter class with streaming support
- Added ThemeContext provider with dark mode state
- Created background job queue for email delivery
```

### 2. Focus on Impact, Not Implementation

Explain **what changed for users**, not **how you changed the code**.

**Good:**
```markdown
### Changed
- Task search now returns results 10x faster for large projects
```

**Bad:**
```markdown
### Changed
- Refactored search algorithm to use binary search tree with Redis caching
```

### 3. Group Related Changes

Combine related commits into single, coherent changelog entries.

**Good:**
```markdown
### Added
- Complete authentication system with login, logout, password reset, and two-factor authentication
```

**Bad:**
```markdown
### Added
- Login endpoint
- Logout endpoint
- Password reset endpoint
- 2FA endpoint
- Auth middleware
- Token validation
```

## Writing Style

### Use Present Tense, Active Voice

**Present tense** (like commit messages):
- ✅ "Add feature"
- ❌ "Added feature"
- ❌ "Feature was added"

**Active voice:**
- ✅ "Fix login timeout"
- ❌ "Login timeout was fixed"

### Be Specific and Concrete

Vague descriptions don't help users understand changes.

**Good:**
```markdown
### Fixed
- Login redirect after session timeout now preserves the original page URL
- Calculation error when applying discount codes to tax-exempt items
- Memory leak in background sync causing crashes after 6+ hours
```

**Bad:**
```markdown
### Fixed
- Login issue
- Bug in calculations
- Performance problem
```

### Keep Entries Scannable

Use consistent structure so users can quickly scan for relevant changes.

**Good format:**
```markdown
- [Action] [What] [Context/Condition]
- Fix login redirect preserving original URL after timeout
- Add CSV export for task lists over 1000 items
```

### Avoid Technical Jargon

Use terms users understand, not internal code names or technical implementation details.

**Good:**
```markdown
### Changed
- Improved dashboard loading speed by 60%
```

**Bad:**
```markdown
### Changed
- Optimized React re-renders using useMemo and React.memo HOC
```

## What to Include

### DO Include

| Change Type | Include When | Example |
|-------------|--------------|---------|
| **New features** | Users can see/use it | "Add task priority levels" |
| **Bug fixes** | Affects user experience | "Fix incorrect due date display" |
| **Breaking changes** | Requires user action | "Change API authentication method" |
| **Performance** | Noticeable to users | "Reduce page load time by 50%" |
| **Security** | Vulnerability fixed | "Fix XSS vulnerability in comments" |
| **Deprecations** | Users need to migrate | "Deprecate v1 API (removal in v3.0)" |
| **UI/UX changes** | Visual or interaction changes | "Redesigned task creation form" |

### DON'T Include

| Change Type | Reason to Exclude | Alternative |
|-------------|-------------------|-------------|
| **Refactoring** | Internal, no user impact | Mention in commit messages only |
| **Test updates** | Development concern | Keep in git history |
| **CI/CD changes** | Infrastructure concern | Document in deployment docs |
| **Code formatting** | No functional change | Skip entirely |
| **Dependency bumps** | Unless user-facing | Only if security/compatibility impact |
| **Development docs** | Internal documentation | Separate developer changelog if needed |

### Gray Areas: When to Include

**Dependency updates:**
- ❌ Skip: `chore: update jest to 29.0.0`
- ✅ Include: "Update Node.js requirement to v18+ for security patches"

**Documentation:**
- ❌ Skip: Internal API docs, code comments
- ✅ Include: User guides, API documentation users reference

**Build/deployment:**
- ❌ Skip: Webpack config changes, CI optimizations
- ✅ Include: New installation requirements, deployment steps

## Handling Breaking Changes

Breaking changes deserve special treatment.

### Mark Clearly

Use warning symbols and dedicated sections:

```markdown
## [2.0.0] - 2026-01-11

### Breaking Changes ⚠️

- **API Authentication**: All API endpoints now require JWT tokens in Authorization header

### Removed
- Deprecated `/v1/users` endpoint (use `/v2/users` instead)
```

### Provide Migration Guides

Always explain **how to upgrade**:

```markdown
### Breaking Changes ⚠️

- **API Response Format**: All responses now use camelCase instead of snake_case

  **Migration:**
  ```javascript
  // Before
  const userName = response.user_name
  const createdAt = response.created_at

  // After
  const userName = response.userName
  const createdAt = response.createdAt
  ```

  See [v2 Migration Guide](docs/v2-migration.md) for full details.
```

### Give Advance Notice

Deprecate before removing:

```markdown
## [1.5.0] - 2025-11-01

### Deprecated
- `/v1/users` endpoint will be removed in v2.0.0 (est. Jan 2026). Use `/v2/users` instead.

## [2.0.0] - 2026-01-11

### Removed
- `/v1/users` endpoint (deprecated in v1.5.0)
```

## Linking and References

### Link to External Resources

Help users find more information:

```markdown
### Added
- OAuth2 authentication for third-party integrations. See [OAuth2 guide](https://docs.example.com/oauth2).

### Fixed
- Memory leak in WebSocket connections [#456](https://github.com/user/repo/issues/456)

### Changed
- Database migration system. See [ADR-003](history/adr/003-migration-strategy.md) for rationale.
```

### Link Types

| Link Target | When to Link | Format |
|-------------|--------------|--------|
| **Issues** | User-reported bugs | `[#123](url)` |
| **Pull Requests** | Complex changes | `[PR #456](url)` |
| **Documentation** | New features, breaking changes | `[Guide](url)` |
| **Specs** | Feature implementation | `[spec-001](specs/001/spec.md)` |
| **ADRs** | Architectural decisions | `[ADR-003](history/adr/003.md)` |
| **CVEs** | Security fixes | `CVE-2024-12345` |

## Versioning and Releases

### Keep Versions in Descending Order

Newest releases first:

```markdown
## [Unreleased]

## [1.3.0] - 2026-01-11
## [1.2.5] - 2026-01-05
## [1.2.4] - 2025-12-20
```

### Always Include Dates

Use ISO 8601 format (YYYY-MM-DD):

```markdown
## [1.3.0] - 2026-01-11

✅ Clear, sortable, unambiguous

## [1.3.0] - Jan 11, 2026
## [1.3.0] - 01/11/2026

❌ Verbose or ambiguous
```

### Maintain Comparison Links

At bottom of changelog:

```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/repo/compare/v1.2.5...v1.3.0
[1.2.5]: https://github.com/user/repo/compare/v1.2.4...v1.2.5
```

Benefits:
- Users can see **exactly** what changed
- Easy code review between versions
- Helps with debugging version-specific issues

## Maintenance Workflow

### Continuous Updates (Recommended)

Update changelog **as you work**:

1. **During development**: Add entries to `[Unreleased]` section
2. **On release**: Move unreleased entries to new version section
3. **Add date**: Use release date
4. **Update links**: Update comparison URLs

**Benefits:**
- Always up-to-date
- Less work at release time
- Team stays informed

### Release-Time Generation

Generate changelog **when releasing**:

1. **Analyze commits** since last release
2. **Categorize** by conventional commit types
3. **Transform** to user-facing descriptions
4. **Review and edit** before publishing

**Benefits:**
- No maintenance during development
- Can group related commits
- Consistent quality review

**Drawbacks:**
- Requires good commit messages
- More work at release time
- May miss context from weeks ago

### Hybrid Approach

**For major changes**: Add to changelog immediately
**For minor changes**: Generate from commits at release

```markdown
## [Unreleased]

### Added
- Complete redesign of dashboard with customizable widgets
  (Major feature, added during development)

<!-- Minor changes will be added from commits at release -->
```

## Common Antipatterns

### 1. Git Log Dumps

**Bad:**
```markdown
## [1.2.0]

- a3c2f1b: feat(api): add endpoint
- 9d8e7f6: fix(ui): button color
- 1b2c3d4: chore: update deps
- 7e8f9g0: refactor: move files
```

**Good:**
```markdown
## [1.2.0] - 2026-01-11

### Added
- User search API endpoint for finding users by email or name

### Fixed
- Primary button now uses correct brand color (#007bff)
```

### 2. Vague Entries

**Bad:**
```markdown
### Fixed
- Various bugs
- Performance issues
- Some UI problems
```

**Good:**
```markdown
### Fixed
- Login timeout on slow connections over 5 seconds
- Task list loading delay for projects with 1000+ tasks
- Overlapping text in mobile navigation menu
```

### 3. Developer Jargon

**Bad:**
```markdown
### Changed
- Refactored UserService to use Repository pattern
- Migrated from Redux to Zustand for state management
- Optimized re-renders with React.memo and useMemo
```

**Good:**
```markdown
### Changed
- Improved application responsiveness and reduced memory usage
```

(Internal refactoring details belong in commit messages, not changelog)

### 4. Missing Context

**Bad:**
```markdown
### Changed
- Updated validation
```

**Good:**
```markdown
### Changed
- Email validation now accepts international domain names (e.g., user@münchen.de)
```

### 5. Inconsistent Formatting

**Bad:**
```markdown
### Added
- Dark mode
- added: CSV export
* User can now see task history
```

**Good:**
```markdown
### Added
- Dark mode toggle in settings
- CSV export for task reports
- Task history timeline showing all changes
```

## Examples

### Excellent Changelog Entry

```markdown
## [2.1.0] - 2026-01-11

### Added
- **Task Templates**: Create reusable task templates for common workflows. Save time by pre-filling task details, checklists, and assignees. [Learn more](https://docs.example.com/templates)
- Keyboard shortcuts for quick task creation (Ctrl+N) and search (Ctrl+K)
- Email digest option for weekly task summaries

### Changed
- Task search now includes comments and attachments in results
- Improved mobile layout for task details on small screens
- Updated notification preferences UI with clearer grouping

### Fixed
- Task due dates now respect user's timezone setting [#234](https://github.com/user/repo/issues/234)
- File attachments over 10MB no longer cause upload failures [#456](https://github.com/user/repo/issues/456)
- Resolved flickering in task list during real-time updates

### Security
- Updated authentication library to patch session fixation vulnerability (CVE-2026-12345)

[2.1.0]: https://github.com/user/repo/compare/v2.0.0...v2.1.0
```

**Why it's good:**
- User-focused descriptions
- Specific, concrete changes
- Links to docs and issues
- Consistent formatting
- Proper categorization
- Security update noted

### Poor Changelog Entry

```markdown
## [2.1.0]

### Changes
- Added templates feature
- Fixed bugs
- Updated some dependencies
- Improved performance
- Refactored codebase
- Updated tests
```

**Why it's poor:**
- No date
- Vague descriptions
- Mixes internal/external changes
- Wrong category names
- No links or context
- Includes developer-only changes

## Changelog Maintenance Checklist

Before publishing a new release:

- [ ] All user-facing changes included
- [ ] Changes categorized correctly (Added, Changed, Fixed, etc.)
- [ ] Entries are specific and clear
- [ ] User-focused language (not developer jargon)
- [ ] Version number follows semantic versioning
- [ ] Date in ISO 8601 format (YYYY-MM-DD)
- [ ] Breaking changes clearly marked with ⚠️
- [ ] Migration guides for breaking changes
- [ ] Links to issues, PRs, docs included
- [ ] Comparison links updated at bottom
- [ ] No internal/development-only changes
- [ ] Spelling and grammar checked
- [ ] Versions in descending order
- [ ] Unreleased section cleared (if releasing)

## References

- Keep a Changelog: https://keepachangelog.com/
- Changelog Best Practices: https://userguiding.com/blog/changelog-best-practices
- Semantic Versioning: https://semver.org/
- How to Write a Changelog: https://amoeboids.com/blog/changelog-how-to-write-good-one/
