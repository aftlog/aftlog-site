#!/usr/bin/env python3
"""Generate sitemap.xml covering EVERY public site page.

Idempotent: always rewrites sitemap.xml from the current file tree. URL
mapping mirrors site_check.py's expectations:
    index.html         -> https://aftlog.com/
    <dir>/index.html   -> https://aftlog.com/<dir>/   (only updates/, blog/)
    everything else    -> https://aftlog.com/<path>
Excludes components/ (partials), .git, .github.

Usage: python3 tools/generate_sitemap.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'sitemap.xml'
BASE = 'https://aftlog.com'

# Subdirectories whose index renders at the trailing-slash URL.
SLASH_INDEX = {'updates', 'blog'}


def public_pages(root: pathlib.Path):
    for f in sorted(root.rglob('*.html')):
        rel = f.relative_to(root).as_posix()
        if any(part in ('.git', '.github', 'components') for part in f.parts):
            continue
        yield rel


def url_for(rel: str) -> str:
    if rel == 'index.html':
        return f'{BASE}/'
    if rel.endswith('/index.html'):
        parent = rel[: -len('index.html')].rstrip('/')
        if parent in SLASH_INDEX:
            return f'{BASE}/{parent}/'
    return f'{BASE}/{rel}'


def main() -> None:
    urls = sorted({url_for(rel) for rel in public_pages(ROOT)})
    body = '\n'.join(f'  <url><loc>{u}</loc></url>' for u in urls)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{body}\n'
        '</urlset>\n'
    )
    OUT.write_text(xml, encoding='utf-8')
    print(f'wrote {OUT.name}: {len(urls)} URLs')


if __name__ == '__main__':
    main()
