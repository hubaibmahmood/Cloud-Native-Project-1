---
name: changelog-from-commits
description: |
  Generate production-quality changelogs from git commit history using Keep a Changelog format with semantic versioning.
  Links commits to specs, ADRs, and features. Categorizes changes (Added/Changed/Fixed/etc) from conventional commits.
  This skill should be used when preparing releases, documenting version history, or creating user-facing release notes.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Changelog from Commits

Generate production-quality changelogs from git commit history following Keep a Changelog format and Semantic Versioning principles.

## What This Skill Does

- Analyzes git commit history to extract meaningful changes
- Categorizes commits using conventional commit types (feat, fix, docs, etc.)
- Generates/updates CHANGELOG.md in Keep a Changelog 1.1.0 format
- Links commits to specs, ADRs, and feature documentation
- Groups changes by semantic version (MAJOR.MINOR.PATCH)
- Provides user-facing change descriptions

## What This Skill Does NOT Do

- Create git tags or releases (use git/GitHub tools)
- Modify commit history or messages
- Generate API documentation (use API doc tools)
- Deploy or publish releases

---

## Before Implementation

Gather context to ensure successful changelog generation:

| Source | Gather |
|--------|--------|
| **Git History** | Recent commits, tags, branch names, merge commits |
| **Codebase** | Existing CHANGELOG.md format, version files, specs/, ADRs |
| **Conversation** | Target version, date range, unreleased changes to include |
| **Skill References** | Keep a Changelog spec, conventional commits patterns, best practices |
| **Project Structure** | Location of specs/, history/adr/, feature documentation |

Ensure all required context is gathered before generating changelog.
Only ask user for version/range preferences (changelog expertise is in this skill).

---

## Workflow

### 1. Gather Context

**Check for existing CHANGELOG.md:**
```bash
# Check if CHANGELOG.md exists and read current format
ls -la CHANGELOG.md
```

**Get git history:**
```bash
# Get recent commits with full details
git log --oneline --decorate --graph --date=short --pretty=format:"%h|%ad|%s|%b" -n 50

# Get all version tags
git tag -l --sort=-version:refname

# Get commits since last tag (for unreleased section)
git log $(git describe --tags --abbrev=0)..HEAD --oneline --pretty=format:"%h|%ad|%s|%b" --date=short
```

**Identify project structure:**
```bash
# Find specs and ADRs
ls -la specs/
ls -la history/adr/
ls -la .specify/memory/
```

### 2. Parse and Categorize Commits

For each commit, extract:
- **Type** (feat, fix, docs, refactor, perf, test, chore, breaking)
- **Scope** (optional, e.g., api, auth, database)
- **Description** (user-facing summary)
- **Body** (details, breaking changes)
- **References** (spec links, ADR links, issue numbers)

**Categorization mapping** (see `references/conventional-commits.md`):

| Commit Type | Changelog Category | SemVer Impact |
|-------------|-------------------|---------------|
| `feat:` | Added | MINOR |
| `fix:` | Fixed | PATCH |
| `docs:` | Documentation (if user-facing) | - |
| `perf:` | Changed (performance) | PATCH |
| `refactor:` | - (internal, skip) | - |
| `test:` | - (internal, skip) | - |
| `chore:` | - (internal, skip) | - |
| `BREAKING CHANGE:` | Breaking Changes (⚠️) | MAJOR |
| `security:` | Security | PATCH |
| `deprecated:` | Deprecated | MINOR |
| `removed:` | Removed | MAJOR |

### 3. Extract Links to Specs/ADRs

**From commit messages:**
```
# Pattern 1: Explicit references
Refs: #123, spec-001
ADR: 003
Spec: 001-task-api

# Pattern 2: Co-authored or linked
Related to specs/001-task-api/spec.md
See ADR history/adr/003-database-choice.md
```

**From branch names:**
```
feature/001-task-api -> specs/001-task-api/
bugfix/auth-token -> search for "auth" in specs
```

**From PHR history:**
Match commit timestamp with PHR creation time:
```bash
# Find PHRs around commit date
ls -la history/prompts/**/*.md
grep -l "COMMIT_SHA" history/prompts/**/*.md
```

### 4. Determine Version Number

**If preparing new release:**
1. Get current version from latest tag: `git describe --tags --abbrev=0`
2. Analyze commits since last tag:
   - Any `BREAKING CHANGE:` → MAJOR bump
   - Any `feat:` → MINOR bump
   - Only `fix:`, `perf:`, `security:` → PATCH bump
3. Propose new version following SemVer
4. Ask user to confirm version number

**If documenting existing tag:**
- Use the tag version as-is
- Extract commits between tags

### 5. Generate Changelog Content

**Format** (Keep a Changelog 1.1.0):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-01-11

### Added
- New feature description [#123](link-to-pr) ([spec-001](specs/001-task-api/spec.md))
- Another feature description

### Changed
- Modified behavior description ([ADR-003](history/adr/003-decision.md))

### Fixed
- Bug fix description [#456](link-to-issue)

### Breaking Changes ⚠️
- Breaking change with migration guide

### Deprecated
- Feature marked for removal in v2.0.0

### Removed
- Removed feature (breaking)

### Security
- Security fix description (CVE-XXXX-YYYY)

## [1.1.0] - 2025-12-15
...

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

### 6. Write or Update CHANGELOG.md

**If CHANGELOG.md exists:**
1. Read current content
2. Insert new version section after "## [Unreleased]"
3. Move unreleased changes to new version
4. Update comparison links at bottom

**If creating new CHANGELOG.md:**
1. Use template from `assets/changelog-template.md`
2. Insert all versions from git history
3. Add comparison links

**Always:**
- Preserve existing manual edits
- Keep user-facing language (avoid technical jargon)
- Add links to specs, ADRs, PRs, issues
- Use ISO 8601 date format (YYYY-MM-DD)

### 7. Validate and Review

Run validation checks:

- [ ] Follows Keep a Changelog format
- [ ] Dates in ISO 8601 format (YYYY-MM-DD)
- [ ] Versions in descending order (newest first)
- [ ] All categories used correctly (Added, Changed, Fixed, etc.)
- [ ] User-facing language (not git commit technical details)
- [ ] Links work (specs, ADRs, PRs, issues)
- [ ] Breaking changes clearly marked with ⚠️
- [ ] Comparison links at bottom are correct
- [ ] No internal/development-only changes included

Present changelog to user for review and edits before finalizing.

---

## Decision Trees

### Should a commit be included?

```
Is commit type in [feat, fix, perf, security, deprecated, removed, breaking]?
├─ YES → Include in changelog
└─ NO → Check scope
   ├─ docs: with user-facing scope (e.g., docs(api):) → Include
   ├─ refactor/test/chore → Skip (internal)
   └─ Unsure? → Ask user if commit impacts users
```

### Which category?

```
Check commit message:
├─ Contains "BREAKING CHANGE:" → Breaking Changes section
├─ Starts with "feat:" → Added
├─ Starts with "fix:" → Fixed
├─ Starts with "perf:" → Changed (performance improvement)
├─ Starts with "security:" → Security
├─ Contains "deprecated" → Deprecated
├─ Contains "removed" → Removed
├─ Starts with "docs:" and user-facing → Documentation
└─ Multiple categories possible → Ask user
```

### How to extract spec/ADR links?

```
1. Parse commit message body for:
   - "Refs:", "Spec:", "ADR:", "Related:", "See:"
   - Spec IDs: spec-001, 001-task-api
   - ADR IDs: adr-003, 003-database

2. Extract from branch name:
   - feature/001-task-api → specs/001-task-api/
   - Validate path exists before linking

3. Search PHR history:
   - Find PHRs with matching commit timestamp (±1 hour)
   - Extract SPEC_LINK and ADR_LINK from PHR frontmatter
   - Validate links before using

4. If no links found:
   - For significant changes (feat, breaking) → Ask user
   - For minor changes (fix, perf) → Skip linking
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No git history | Not a git repo | Inform user, suggest `git init` |
| No commits found | Empty repo or invalid range | Check git log, adjust date range |
| No tags found | First release | Create initial version (suggest 0.1.0 or 1.0.0) |
| Malformed commit message | Non-conventional format | Parse best-effort, categorize as "Changed" |
| Existing CHANGELOG.md corrupted | Invalid format | Backup existing, create fresh from template |
| Conflicting versions | Manual edits vs git tags | Show conflict, ask user preference |
| Missing spec/ADR links | Files moved or deleted | Use commit reference, note link is broken |

---

## Best Practices

From `references/best-practices.md`:

### DO

- **Write for users, not developers**: "Added dark mode toggle" not "Implemented theme context provider"
- **Group related changes**: Combine related commits into one changelog entry
- **Add migration guides**: For breaking changes, explain upgrade path
- **Link to documentation**: Specs, ADRs, guides for complex changes
- **Keep it updated**: Add to changelog during development, not after
- **Use present tense**: "Add feature" not "Added feature"
- **Be specific**: "Fix login timeout on slow connections" not "Fix bug"

### DON'T

- **Include internal changes**: Refactors, test improvements, CI changes
- **Use git commit SHAs**: Use version tags and comparison links instead
- **Be vague**: "Improve performance" without specifying what improved
- **Skip dates**: Every version needs ISO 8601 date
- **Rewrite history**: Don't remove or edit past version entries
- **Use passive voice**: "Feature was added" → "Add feature"

---

## Output

Generate and present:

1. **CHANGELOG.md** (created or updated)
2. **Summary** of changes included
3. **Suggested version number** with rationale (if new release)
4. **Links validation report** (which links work, which are broken)
5. **Commits excluded** and why (for transparency)

Confirm with user before writing final CHANGELOG.md.

---

## Examples

See `references/changelog-examples.md` for:
- Complete CHANGELOG.md examples
- Commit message → changelog entry transformations
- Version numbering scenarios
- Linking patterns

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/keep-a-changelog-spec.md` | Official Keep a Changelog 1.1.0 specification |
| `references/conventional-commits.md` | Conventional Commits patterns and parsing rules |
| `references/best-practices.md` | Changelog best practices and anti-patterns |
| `references/changelog-examples.md` | Real-world examples and transformations |
| `scripts/generate_changelog.py` | Python script for automated changelog generation |
| `assets/changelog-template.md` | Keep a Changelog template boilerplate |

---

## Quick Start

```bash
# Generate changelog for unreleased changes
/changelog-from-commits

# Generate changelog for specific version
/changelog-from-commits --version 1.2.0

# Generate changelog between tags
/changelog-from-commits --from v1.0.0 --to v1.2.0

# Update existing CHANGELOG.md
/changelog-from-commits --update
```

---

## Integration with Spec-Driven Development

This skill integrates with your SDD workflow:

- **After /sp.implement**: Generate changelog from implementation commits
- **Before /sp.git.commit_pr**: Update CHANGELOG.md as part of release prep
- **After feature completion**: Document feature in changelog with spec links
- **Release workflow**: Generate changelog → create tag → create PR → merge

Changelog entries link back to:
- `specs/<feature>/spec.md` for feature documentation
- `history/adr/<id>-decision.md` for architectural rationale
- `history/prompts/<feature>/` for implementation context
