#!/usr/bin/env python3
"""Inject the GoatCounter analytics snippet before </head> on every site page.

Idempotent: skips files that already contain the marker. Also reports any
files with no </head> so nothing is silently missed.

Usage: python3 tools/inject_analytics.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKER = 'data-goatcounter="https://aftlog.goatcounter.com/count"'
SNIPPET = (
    '<script data-goatcounter="https://aftlog.goatcounter.com/count"\n'
    '        async src="//gc.zgo.at/count.js"></script>'
)


def main() -> None:
    html_files = sorted(f for f in ROOT.rglob('*.html') if '.git' not in f.parts)
    changed, skipped = [], []
    for f in html_files:
        rel = str(f.relative_to(ROOT))
        text = f.read_text(encoding='utf-8')
        if MARKER in text:
            skipped.append(f'{rel} (already present)')
            continue
        if '</head>' not in text:
            skipped.append(f'{rel} (no </head>)')
            continue
        text = text.replace('</head>', f'{SNIPPET}\n</head>', 1)
        f.write_text(text, encoding='utf-8')
        changed.append(rel)
    print(f'injected {len(changed)} file(s):')
    for c in changed:
        print(f'  + {c}')
    print(f'skipped {len(skipped)}:')
    for s in skipped:
        print(f'  = {s}')


if __name__ == '__main__':
    main()
