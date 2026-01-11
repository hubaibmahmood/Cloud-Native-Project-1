#!/usr/bin/env python3
"""
Generate changelog from git commits following Keep a Changelog format.

Usage:
    python generate_changelog.py [options]

Options:
    --version VERSION    Version number for the release (e.g., 1.2.0)
    --from TAG           Start tag for commit range
    --to TAG             End tag for commit range (default: HEAD)
    --output FILE        Output file path (default: CHANGELOG.md)
    --update             Update existing CHANGELOG.md (insert new version)
    --unreleased         Generate only unreleased section
    --dry-run            Preview changelog without writing
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Commit:
    """Represents a parsed git commit."""
    sha: str
    date: str
    type: str
    scope: Optional[str]
    description: str
    body: str
    breaking: bool = False
    refs: Dict[str, List[str]] = field(default_factory=lambda: {
        'specs': [],
        'adrs': [],
        'issues': [],
        'prs': []
    })


class ChangelogGenerator:
    """Generate changelog from git commit history."""

    # Commit type to changelog category mapping
    TYPE_MAPPING = {
        'feat': 'Added',
        'fix': 'Fixed',
        'perf': 'Changed',
        'security': 'Security',
        'deprecated': 'Deprecated',
        'removed': 'Removed',
        'docs': None,  # Skip unless user-facing
        'style': None,  # Skip
        'refactor': None,  # Skip
        'test': None,  # Skip
        'chore': None,  # Skip
        'build': None,  # Skip
        'ci': None,  # Skip
    }

    # SemVer impact mapping
    SEMVER_IMPACT = {
        'feat': 'MINOR',
        'fix': 'PATCH',
        'perf': 'PATCH',
        'security': 'PATCH',
        'deprecated': 'MINOR',
        'removed': 'MAJOR',
    }

    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path)
        self.commits: List[Commit] = []

    def run_git_command(self, *args) -> str:
        """Execute git command and return output."""
        try:
            result = subprocess.run(
                ['git', *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e.stderr}", file=sys.stderr)
            sys.exit(1)

    def get_commit_range(self, from_tag: Optional[str], to_tag: str = 'HEAD') -> str:
        """Determine commit range for changelog generation."""
        if from_tag:
            return f"{from_tag}..{to_tag}"

        # Find last tag
        try:
            last_tag = self.run_git_command('describe', '--tags', '--abbrev=0')
            return f"{last_tag}..{to_tag}"
        except:
            # No tags found, use all history
            return to_tag

    def parse_commits(self, commit_range: str) -> List[Commit]:
        """Parse git commits in the given range."""
        # Get commit log with custom format
        log_format = '%H|%ad|%s|%b'
        log_output = self.run_git_command(
            'log',
            commit_range,
            '--date=short',
            f'--pretty=format:{log_format}',
            '--no-merges'
        )

        if not log_output:
            return []

        commits = []
        current_commit = None

        for line in log_output.split('\n'):
            if '|' in line and len(line.split('|')) >= 3:
                # New commit line
                if current_commit:
                    commits.append(current_commit)

                parts = line.split('|', 3)
                sha, date, subject = parts[0], parts[1], parts[2]
                body = parts[3] if len(parts) > 3 else ''

                commit = self._parse_commit_message(sha, date, subject, body)
                current_commit = commit
            elif current_commit:
                # Continuation of body
                current_commit.body += '\n' + line

        if current_commit:
            commits.append(current_commit)

        return commits

    def _parse_commit_message(self, sha: str, date: str, subject: str, body: str) -> Commit:
        """Parse conventional commit message."""
        # Pattern: type(scope)!: description
        pattern = r'^(?P<type>\w+)(?:\((?P<scope>[\w-]+)\))?(?P<breaking>!)?: (?P<description>.+)$'
        match = re.match(pattern, subject)

        if match:
            commit = Commit(
                sha=sha[:7],
                date=date,
                type=match.group('type'),
                scope=match.group('scope'),
                description=match.group('description'),
                body=body,
                breaking=bool(match.group('breaking'))
            )
        else:
            # Non-conventional commit, treat as chore
            commit = Commit(
                sha=sha[:7],
                date=date,
                type='chore',
                scope=None,
                description=subject,
                body=body
            )

        # Extract references from body
        self._extract_references(commit)

        return commit

    def _extract_references(self, commit: Commit):
        """Extract spec, ADR, issue, and PR references from commit body."""
        if not commit.body:
            return

        for line in commit.body.split('\n'):
            line = line.strip()

            # Spec references (Spec: 001-task-api)
            if line.startswith('Spec:'):
                specs = [s.strip() for s in line[5:].split(',')]
                commit.refs['specs'].extend(specs)

            # ADR references (ADR: 003)
            if line.startswith('ADR:'):
                adrs = [a.strip() for a in line[4:].split(',')]
                commit.refs['adrs'].extend(adrs)

            # Issue references (Refs: #123, Closes: #456, Fixes: #789)
            if any(line.startswith(prefix) for prefix in ['Refs:', 'Closes:', 'Fixes:', 'Related:']):
                issues = re.findall(r'#(\d+)', line)
                commit.refs['issues'].extend(issues)

            # PR references (PR: #123)
            if line.startswith('PR:'):
                prs = re.findall(r'#(\d+)', line)
                commit.refs['prs'].extend(prs)

            # Breaking change
            if line.startswith('BREAKING CHANGE:'):
                commit.breaking = True

    def categorize_commits(self) -> Dict[str, List[Commit]]:
        """Categorize commits by changelog category."""
        categories = defaultdict(list)

        for commit in self.commits:
            category = self.TYPE_MAPPING.get(commit.type)

            if category is None:
                # Skip internal commits
                continue

            if commit.breaking:
                categories['Breaking Changes'].append(commit)
            else:
                categories[category].append(commit)

        return dict(categories)

    def suggest_version(self, current_version: str) -> str:
        """Suggest next version based on commits and SemVer."""
        # Parse current version
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', current_version)
        if not match:
            return current_version

        major, minor, patch = map(int, match.groups())

        # Determine version bump
        has_breaking = any(c.breaking for c in self.commits)
        has_feat = any(c.type == 'feat' for c in self.commits)
        has_fix = any(c.type in ['fix', 'perf', 'security'] for c in self.commits)

        if has_breaking:
            major += 1
            minor = 0
            patch = 0
        elif has_feat:
            minor += 1
            patch = 0
        elif has_fix:
            patch += 1

        return f"{major}.{minor}.{patch}"

    def format_commit_entry(self, commit: Commit, repo_url: Optional[str] = None) -> str:
        """Format a single commit as a changelog entry."""
        entry = f"- {commit.description}"

        # Add links
        links = []

        # Issue links
        if commit.refs['issues'] and repo_url:
            for issue in commit.refs['issues']:
                links.append(f"[#{issue}]({repo_url}/issues/{issue})")

        # PR links
        if commit.refs['prs'] and repo_url:
            for pr in commit.refs['prs']:
                links.append(f"[PR #{pr}]({repo_url}/pull/{pr})")

        # Spec links
        if commit.refs['specs']:
            for spec in commit.refs['specs']:
                links.append(f"([spec-{spec}](specs/{spec}/spec.md))")

        # ADR links
        if commit.refs['adrs']:
            for adr in commit.refs['adrs']:
                links.append(f"([ADR-{adr}](history/adr/{adr}.md))")

        if links:
            entry += " " + " ".join(links)

        return entry

    def generate_version_section(
        self,
        version: str,
        date: Optional[str] = None,
        repo_url: Optional[str] = None
    ) -> str:
        """Generate a version section for the changelog."""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        lines = [f"## [{version}] - {date}\n"]

        # Categorize commits
        categorized = self.categorize_commits()

        # Category order
        category_order = [
            'Breaking Changes',
            'Added',
            'Changed',
            'Deprecated',
            'Removed',
            'Fixed',
            'Security'
        ]

        for category in category_order:
            if category not in categorized:
                continue

            commits = categorized[category]
            if not commits:
                continue

            # Add category header
            if category == 'Breaking Changes':
                lines.append(f"\n### {category} ⚠️\n")
            else:
                lines.append(f"\n### {category}\n")

            # Add commits
            for commit in commits:
                entry = self.format_commit_entry(commit, repo_url)
                lines.append(entry)

            lines.append("")  # Blank line after category

        return "\n".join(lines)

    def get_repo_url(self) -> Optional[str]:
        """Extract repository URL from git remote."""
        try:
            remote_url = self.run_git_command('remote', 'get-url', 'origin')

            # Convert SSH to HTTPS
            if remote_url.startswith('git@'):
                remote_url = remote_url.replace('git@', 'https://').replace('.com:', '.com/')

            # Remove .git suffix
            remote_url = remote_url.rstrip('.git')

            return remote_url
        except:
            return None

    def update_changelog(
        self,
        output_file: Path,
        version: str,
        date: Optional[str] = None
    ):
        """Update existing CHANGELOG.md with new version section."""
        if not output_file.exists():
            # Create new changelog
            self.create_changelog(output_file, version, date)
            return

        # Read existing content
        content = output_file.read_text()

        # Generate new version section
        repo_url = self.get_repo_url()
        new_section = self.generate_version_section(version, date, repo_url)

        # Find insertion point (after [Unreleased])
        unreleased_pattern = r'(## \[Unreleased\]\s*\n)'
        match = re.search(unreleased_pattern, content)

        if match:
            # Insert after [Unreleased] section
            insertion_point = match.end()
            updated_content = (
                content[:insertion_point] +
                "\n" + new_section + "\n" +
                content[insertion_point:]
            )
        else:
            # No [Unreleased] section, insert at top after header
            header_end = content.find('\n## ')
            if header_end > 0:
                updated_content = (
                    content[:header_end] +
                    "\n" + new_section + "\n" +
                    content[header_end:]
                )
            else:
                updated_content = new_section + "\n\n" + content

        # Update comparison links
        updated_content = self._update_comparison_links(updated_content, version)

        output_file.write_text(updated_content)

    def _update_comparison_links(self, content: str, new_version: str) -> str:
        """Update version comparison links at bottom of changelog."""
        repo_url = self.get_repo_url()
        if not repo_url:
            return content

        # Find existing links section
        links_pattern = r'\[Unreleased\]:.*?\n'
        match = re.search(links_pattern, content)

        if match:
            # Update unreleased link
            new_unreleased = f"[Unreleased]: {repo_url}/compare/v{new_version}...HEAD\n"
            content = re.sub(links_pattern, new_unreleased, content)

            # Add new version link
            # Find previous version from unreleased link
            prev_version_match = re.search(r'/compare/v([\d.]+)\.\.\.HEAD', match.group())
            if prev_version_match:
                prev_version = prev_version_match.group(1)
                new_link = f"[{new_version}]: {repo_url}/compare/v{prev_version}...v{new_version}\n"

                # Insert after unreleased link
                content = re.sub(
                    r'(\[Unreleased\]:.*?\n)',
                    r'\1' + new_link,
                    content
                )

        return content

    def create_changelog(
        self,
        output_file: Path,
        version: str,
        date: Optional[str] = None
    ):
        """Create new CHANGELOG.md file."""
        repo_url = self.get_repo_url()
        version_section = self.generate_version_section(version, date, repo_url)

        # Header
        header = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

"""

        # Comparison links
        if repo_url:
            links = f"\n[Unreleased]: {repo_url}/compare/v{version}...HEAD\n"
            links += f"[{version}]: {repo_url}/releases/tag/v{version}\n"
        else:
            links = ""

        content = header + version_section + links

        output_file.write_text(content)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate changelog from git commits'
    )
    parser.add_argument('--version', help='Version number (e.g., 1.2.0)')
    parser.add_argument('--from', dest='from_tag', help='Start tag')
    parser.add_argument('--to', default='HEAD', help='End tag (default: HEAD)')
    parser.add_argument('--output', default='CHANGELOG.md', help='Output file')
    parser.add_argument('--update', action='store_true', help='Update existing CHANGELOG.md')
    parser.add_argument('--unreleased', action='store_true', help='Generate unreleased section')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')

    args = parser.parse_args()

    # Initialize generator
    generator = ChangelogGenerator()

    # Get commit range
    commit_range = generator.get_commit_range(args.from_tag, args.to)
    print(f"Analyzing commits: {commit_range}")

    # Parse commits
    generator.commits = generator.parse_commits(commit_range)
    print(f"Found {len(generator.commits)} commits")

    if not generator.commits:
        print("No commits found in range")
        return

    # Determine version
    if args.version:
        version = args.version
    else:
        # Suggest version based on commits
        try:
            current_tag = generator.run_git_command('describe', '--tags', '--abbrev=0')
            version = generator.suggest_version(current_tag.lstrip('v'))
            print(f"Suggested version: {version}")
        except:
            version = '0.1.0'
            print(f"No tags found, using: {version}")

    # Generate changelog
    output_path = Path(args.output)

    if args.dry_run:
        # Preview mode
        repo_url = generator.get_repo_url()
        section = generator.generate_version_section(version, None, repo_url)
        print("\n" + "="*50)
        print("PREVIEW")
        print("="*50 + "\n")
        print(section)
    elif args.update:
        # Update existing file
        generator.update_changelog(output_path, version)
        print(f"Updated {output_path}")
    else:
        # Create new file
        generator.create_changelog(output_path, version)
        print(f"Created {output_path}")


if __name__ == '__main__':
    main()
