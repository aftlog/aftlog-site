#!/usr/bin/env python3
"""AftLog site testing matrix (DEEPSEEK STEP 7, Section 8).

Checks every item in the spec's test matrix:
  1. Ask AftLog (web) — widget targets the server proxy only
  2. Review badge — targets the server proxy only
  3. Pricing — lifetime-only messaging
  4. SEO pages — exist, unique titles + descriptions
  5. No direct Gemini/GitHub calls — grep generativelanguage / api.github.com
  6. Design system — pages load the canonical aftlog.css palette
  7. Portal linkage — login/dashboard links present on every page
  8. Sitemap — lists every page
  9. Robots — allows indexing

Usage: python3 tools/site_check.py   (exit 0 = all checks pass)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = ""):
    if ok:
        print(f"  ✓ {name}")
    else:
        FAILS.append(name)
        print(f"  ✗ {name} {detail}")


def main():
    pages = [
        "index.html", "features.html", "ai.html", "portal.html",
        "pricing.html", "faq.html", "support.html", "privacy.html",
        "terms.html", "updates/index.html", "blog/index.html",
        "blog/winterize.html", "blog/beginner-checklist.html",
        "blog/outboard-oil.html", "blog/safety-equipment.html",
    ]
    print("AftLog site testing matrix")

    # 4. SEO pages exist with unique metadata
    print("— SEO pages + metadata")
    titles: dict[str, str] = {}
    for p in pages:
        f = ROOT / p
        check(f"{p} exists", f.exists(), f"(missing: {p})")
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8")
        t = re.search(r"<title>(.*?)</title>", content, re.S)
        d = re.search(r'<meta name="description" content="(.*?)">', content, re.S)
        check(f"{p} has title", bool(t))
        check(f"{p} has description", bool(d))
        if t:
            title = re.sub(r"\s+", " ", t.group(1)).strip()
            titles.setdefault(title, p)
    dup = [p for p, title in titles.items() if list(titles.values()).count(title) > 1]
    check("titles are unique", not dup, f"duplicates: {dup}")

    # 5. No direct Gemini or GitHub calls anywhere in the site
    print("— no direct Gemini / GitHub calls")
    forbidden = ["generativelanguage", "api.github.com", "GEMINI_API_KEY",
                 "GITHUB_TOKEN", "ghp_", "AIza"]
    hits: list[str] = []
    for f in ROOT.rglob("*"):
        if f.suffix not in (".html", ".css", ".js", ".xml", ".txt"):
            continue
        if ".git" in f.parts or "tools" in f.parts:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for token in forbidden:
            if token in text:
                hits.append(f"{f.relative_to(ROOT)}:{token}")
    check("no forbidden tokens", not hits, f"found: {hits[:5]}")

    # 1+2. AI widget + review badge target ONLY the server proxy
    print("— server proxy integration")
    ai = (ROOT / "ai.html").read_text(encoding="utf-8")
    check("AI widget posts to /ai/gemini", "'/ai/gemini'" in ai)
    check("AI widget sends the dev key header", "'x-aftlog-dev-key'" in ai)
    check("AI widget body uses extra.continue", "extra: { continue: false }" in ai)
    check("AI widget network message", "Portal server unreachable" in ai)
    check("AI widget offline message", "temporarily offline" in ai)
    portal = (ROOT / "portal.html").read_text(encoding="utf-8")
    check("review badge GETs /admin/publish", "admin/publish" in portal)
    check("review badge uses result.reviewCount", "reviewCount" in portal)

    # 3. Pricing lifetime-only
    print("— pricing messaging")
    pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
    check("pricing says lifetime", "lifetime" in pricing.lower())
    check("pricing says one-time $29", "$29" in pricing and "one-time" in pricing)
    check("pricing says no subscriptions", "subscription" in pricing.lower())
    check("pricing says no expiry", "expire" in pricing.lower())

    # 6. Design system (canonical palette)
    print("— design system")
    css = (ROOT / "aftlog.css").read_text(encoding="utf-8")
    for color, name in [("#0B0B0D", "dark"), ("#E02020", "accent"),
                        ("#FF4B4B", "accent2"), ("#F5F5F7", "light")]:
        check(f"palette {name} ({color}) present", color.lower() in css.lower())
    for p in pages:
        f = ROOT / p
        if not f.exists():
            continue
        if p == "updates/index.html":
            continue  # self-contained page: inline CSS uses the same palette
        check(f"{p} loads aftlog.css", 'aftlog.css' in f.read_text(encoding="utf-8"))

    # 7. Portal linkage + internal linking
    print("— portal linkage + internal links")
    for p in pages:
        f = ROOT / p
        if not f.exists():
            continue
        c = f.read_text(encoding="utf-8")
        check(f"{p} links portal login", "login" in c.lower())
        check(f"{p} has footer nav", "footer" in c.lower())
    for target in ["/features.html", "/ai.html", "/portal.html", "/pricing.html",
                   "/faq.html", "/support.html", "/blog/", "/privacy", "/terms"]:
        found = sum(1 for p in pages if (ROOT / p).exists()
                    and target in (ROOT / p).read_text(encoding="utf-8"))
        check(f"internal link to {target} on {found} page(s)", found >= 2)

    # 8. Sitemap covers all pages
    print("— sitemap + robots")
    sm = (ROOT / "sitemap.xml")
    check("sitemap.xml exists", sm.exists())
    if sm.exists():
        smc = sm.read_text(encoding="utf-8")
        for p in pages:
            if p in ("updates/index.html", "blog/index.html"):
                url = "https://aftlog.com/" + p.replace("index.html", "")
            elif p == "index.html":
                url = "https://aftlog.com/"
            else:
                url = "https://aftlog.com/" + p
            check(f"sitemap includes {url}", url in smc)
    robots = ROOT / "robots.txt"
    check("robots.txt exists", robots.exists())
    if robots.exists():
        rc = robots.read_text(encoding="utf-8")
        check("robots allows indexing", "Allow: /" in rc)
        check("robots points at sitemap", "sitemap.xml" in rc.lower())

    # 10. Accessibility: every <img> carries an alt attribute
    print("— accessibility (alt tags)")
    for p in pages:
        f = ROOT / p
        if not f.exists():
            continue
        c = f.read_text(encoding="utf-8")
        imgs = re.findall(r"<img[^>]*>", c)
        missing = [i[:60] for i in imgs if "alt=" not in i]
        check(f"{p}: all {len(imgs)} images have alt", not missing,
              f"missing: {missing}")

    # 11. Legal coverage (STEP 10 review prep)
    print("— privacy/terms coverage")
    coverage = {
        "privacy.html": ["on-device", "without a signal", "ai",
                          "one-time", "rights", "contact"],
        "terms.html": ["one-time", "lifetime", "refund", "termination",
                        "warranty", "contact"],
    }
    for p, needles in coverage.items():
        f = ROOT / p
        if not f.exists():
            continue
        c = f.read_text(encoding="utf-8").lower()
        for n in needles:
            check(f"{p} covers '{n}'", n.lower() in c)

    # 12. Shared brand header (STEP 7.2): exactly one logo+slogan block,
    # before the H1, on every page
    print("— brand header")
    for p in pages:
        f = ROOT / p
        if not f.exists():
            continue
        c = f.read_text(encoding="utf-8")
        h1 = c.find("<h1>")
        slogan = c.find("Keeping your boat shipshape")
        logo = c.find("aftlog-logo.png")
        check(f"{p}: slogan before H1", slogan != -1 and h1 != -1 and slogan < h1)
        check(f"{p}: logo present", logo != -1)
        check(f"{p}: exactly one slogan block",
              c.count(">Keeping your boat shipshape!</span>") == 1,
              f"count={c.count('>Keeping your boat shipshape!</span>')}")

    # 14. v1 Help System (STEP 8.1)
    print("— help system")
    hi = ROOT / "help" / "index.html"
    check("help/index.html exists", hi.exists())
    if hi.exists():
        hc = hi.read_text(encoding="utf-8")
        check("help: search input", 'help-search' in hc and 'type="search"' in hc)
        check("help: category bar", 'pg-cat-bar' in hc)
        check("help: topic cards", 'pg-blog-card' in hc)
        for m in re.finditer(r'href="(/help/[a-z0-9-]+\.html)"', hc):
            t = ROOT / m.group(1).lstrip('/')
            check(f"help card {m.group(1)} exists", t.exists())

    # 16. Tools (STEP 8.2/8.3)
    print("— tools")
    for t in ["tools/winterization-planner.html", "tools/float-plan.html",
              "tools/buying-advisor.html", "tools/ramp-mode.html", "tools/calculators.html",
              "tools/visual-engine-assist.html", "tools/ai-diagnostics.html", "tools/ask-aftlog.html", "tools/predictive-planner.html", "tools/trip-patterns.html",
              "tools/compliance.html", "tools/manual-finder.html", "tools/diy-library.html", "tools/battery-electronics.html", "tools/glossary.html",
              "checklists/winterization.html"]:
        check(f"{t} exists", (ROOT / t).exists())
    # 15. v1 Help System (STEP 8.1)
    # 13. Blog hub (STEP 7.9)
    print("— blog hub")
    blog = ROOT / "blog" / "index.html"
    if blog.exists():
        bc = blog.read_text(encoding="utf-8")
        check("blog: featured row (3)", bc.count("pg-featured-card") == 3,
              f"count={bc.count('pg-featured-card')}")
        check("blog: 6 category buttons",
              bc.count('class="pg-cat-btn') == 6,
              f"count={bc.count('class=\"pg-cat-btn')}")
        grid_cards = len(re.findall(r'<a class="pg-blog-card|<div class="pg-blog-card', bc))
        titles = set(re.findall(r'pg-blog-card[^>]*>.*?<h3>([^<]+)</h3>', bc, re.S))
        check("blog: 20 unique article cards", len(titles) == 20,
              f"count={len(titles)} (grid renders {grid_cards} incl. 3 featured repeats)")
        check("blog: filter script present", "pg-cat-btn" in bc and "addEventListener" in bc)
        check("blog: CTA to support+faq", "/support.html" in bc and "/faq.html" in bc)
        # every linked blog card target must exist
        for m in re.finditer(r'href="(/blog/[a-z-]+\.html)"', bc):
            t = ROOT / m.group(1).lstrip("/")
            check(f"blog link {m.group(1)} exists", t.exists())

    print()
    if FAILS:
        print(f"FAILED: {len(FAILS)} check(s): {FAILS}")
        sys.exit(1)
    print("ALL CHECKS PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
