#!/usr/bin/env python3
"""Release-note language validator (RULE — user-facing language, 2026-08-16).

Scans user-facing files for developer terminology. Exits 1 (CI failure)
when a forbidden pattern is found. Internal developer docs and source
comments are NOT scanned — this targets release notes, What's New, help
topics, landing page and changelog copy.

NEVER scan FEATURES.md (explicit Louis decision, 2026-08-16): it is an
internal developer document (feature list / version source of truth) and
is permanently exempt from this lint.

Usage:
    python3 tools/lint_release_notes.py <file...>
"""
import re
import sys

FORBIDDEN = [
    (r'\bgating\b', 'gating'),
    (r'\bflags?\b', 'flags'),
    (r'\bmigration\b', 'migration'),
    (r'\bDB\s?v[0-9]+\b', 'DB vX'),
    (r'\bscaffold\b', 'scaffold'),
    (r'\brefactor\b', 'refactor'),
    (r'\bservice\s?layer\b', 'service layer'),
    (r'\bintegration\s?hooks?\b', 'integration hooks'),
    (r'\bsidecar\b', 'sidecar'),
    (r'\bpipeline\b', 'pipeline'),
    (r'\bembeddings?\b', 'embeddings'),
    (r'\bconfidence\s?score\b', 'confidence score'),
    (r'\bfallback\b', 'fallback'),
    (r'\boffline-first\b', 'offline-first (allowed only in technical docs)'),
    (r'\bUI\b(?!\s(?:screen|page|button))', 'UI (unless referring to a visible screen)'),
]

# Lines that match a forbidden pattern but are legitimate (false
# positives). Matches are reported as-is but any line containing an
# excluded pattern is skipped. Add entries with a reason.
EXCLUDED = [
    # Font name, not the developer term "UI".
    (r'\bSegoe\s+UI\b', 'Segoe UI is a font name'),
]


def lint(path: str) -> int:
    try:
        text = open(path, encoding='utf-8').read()
    except OSError as e:
        print(f'  ✗ cannot read {path}: {e}')
        return 1
    hits = 0
    for i, line in enumerate(text.splitlines(), 1):
        # Source comments (/// or //) are developer-facing — not release copy.
        if line.strip().startswith(('///', '//')):
            continue
        if any(re.search(ex, line, re.IGNORECASE) for ex, _ in EXCLUDED):
            continue
        for pattern, label in FORBIDDEN:
            if re.search(pattern, line, re.IGNORECASE):
                print(f'  {path}:{i}: "{label}" — {line.strip()[:90]}')
                hits += 1
    return 1 if hits else 0


def main(argv: list[str]) -> int:
    if not argv:
        print('usage: python3 tools/lint_release_notes.py <file...>')
        return 2
    failed = 0
    for f in argv:
        failed += lint(f)
    if failed:
        print()
        print('Release notes contain developer terminology. '
              'Please rewrite using user-facing language.')
        return 1
    print(f'✓ release-note lint clean ({len(argv)} file(s))')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
