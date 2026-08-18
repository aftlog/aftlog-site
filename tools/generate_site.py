#!/usr/bin/env python3
"""AftLog static site generator (DEEPSEEK STEP 7).

Generates the multi-page SEO site from shared layout + content registry:
  /features  /ai  /portal  /pricing  /faq  /support
  /blog/ (index + 4 articles)  /privacy  /terms
  /sitemap.xml  /robots.txt

Design system: reuses the existing aftlog.css palette (dark #0B0B0D, red
#E02020/#FF4B4B, light #F5F5F7 — the canonical brand, never redesigned)
plus aftlog-pages.css for page-only patterns. No keys, no tokens: the AI
widget and review badge talk ONLY to the portal server proxy
(PORTAL_BASE env, default https://portal.aftlog.com).

Usage:  PORTAL_BASE=https://portal.aftlog.com AFTLOG_DEV_KEY=aftlog-dev \
        python3 tools/generate_site.py
"""
import html
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORTAL = os.environ.get("PORTAL_BASE", "https://portal.aftlog.com").rstrip("/")
DEV_KEY = os.environ.get("AFTLOG_DEV_KEY", "aftlog-dev")


def esc(s):
    return html.escape(s)

# ── Shared navigation ──────────────────────────────────────────────────
NAV = [
    ("/", "Home"),
    ("/features.html", "Features"),
    ("/ai.html", "AI"),
    ("/portal.html", "Portal"),
    ("/pricing.html", "Pricing"),
    ("/faq.html", "FAQ"),
    ("/support.html", "Support"),
    ("/blog/", "Blog"),
    ("/updates/", "Updates"),
]


def header(active: str) -> str:
    links = []
    for href, label in NAV:
        on = ' class="on"' if (active == href or (active == "/blog/" and href == "/blog/")) else ""
        links.append(f'<a href="{href}"{on}>{label}</a>')
    links.append('<a href="/#waitlist" class="btn btn-primary">Join the waitlist</a>')
    return f"""<header class="site-header site-header--dark">
  <div class="container header-inner">
    <div class="logo"><a href="/"><img src="/images/aftlog-badge.png" alt="AftLog"></a></div>
    <nav class="nav" aria-label="Main">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer() -> str:
    return """<footer class="site-footer site-footer--dark">
  <div class="pg-marine-strip"><div class="container pg-marine-strip-inner">
    <div class="pg-marine-strip-text">Fish on your next trip? CatchTales keeps the details.</div>
    <a class="btn btn-secondary btn-sm" href="/catchtales.html">CatchTales</a>
  </div></div>
  <div class="container footer-grid">
    <div class="footer-col">
      <div class="logo"><img src="/images/aftlog-badge.png" alt="AftLog"></div>
      <p>Keeping your boat shipshape. Works without a signal. Boat maintenance &amp; logbook app for Canada &amp; USA.</p>
    </div>
    <div class="footer-col">
      <h4>Product</h4>
      <a href="/features.html">Features</a>
      <a href="/ai.html">AftLog AI</a>
      <a href="/pricing.html">Pricing — lifetime Pro</a>
      <a href="/faq.html">FAQ</a>
    </div>
    <div class="footer-col">
      <h4>Resources</h4>
      <a href="/tools/">Tools</a>
      <a href="/blog/">Blog</a>
      <a href="/support.html">Support</a>
      <a href="/updates/">Updates</a>
      <a href="/#waitlist">Waitlist</a>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <a href="/privacy">Privacy</a>
      <a href="/terms">Terms</a>
      <a href="/sitemap.xml">Sitemap</a>
    </div>
    <div class="footer-col">
      <h4>Marine Suite: AftLog + CatchTales</h4>
      <p class="pg-muted">Tools for your boat. Tools for your fishing.</p>
      <a href="/catchtales.html">CatchTales</a>
    </div>
    <div class="footer-col">
      <h4>Portal</h4>
      <a href="%PORTAL%/login">Portal login</a>
      <a href="%PORTAL%/portal/">Portal dashboard</a>
      <a href="%PORTAL%/portal/year-in-review">Year in Review</a>
      <a href="%PORTAL%/portal/boats">Boat analytics</a>
    </div>
  </div>
  <div class="container footer-note">AftLog — keeping your boat shipshape. Designed for pleasure craft and fishing boats in Canada + USA. · Platform v1.111</div>
</footer>""".replace("%PORTAL%", PORTAL)


def meta(title: str, desc: str, path: str) -> str:
    return f"""<meta charset="UTF-8">
<title>{html.escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/images/favicon-192.png">
<link rel="apple-touch-icon" href="/images/favicon-180.png">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://aftlog.com/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://aftlog.com{path}">
<link rel="stylesheet" href="/aftlog.css">
<link rel="stylesheet" href="/aftlog-pages.css">"""


def page(slug: str, title: str, desc: str, body: str, active: str | None = None) -> str:
    path = f"/{slug}" if slug != "blog/index" else "/blog/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{meta(title, desc, path)}
<script>
  (function(){{ if (location.hash) history.replaceState(null, '', location.pathname + location.search); }})();
</script>
</head>
<body>
{header(active or f"/{slug.split('/')[0]}")}
<main class="pg-main">
{body}
</main>
{footer()}
</body>
</html>
"""


def hero(title: str, sub: str) -> str:
    # Shared brand header (STEP 7.2): the same logo + slogan block the
    # homepage hero uses, injected BEFORE the page H1 — top-left, same
    # sizes/spacing. The component source of truth lives in
    # components/header_brand.html.
    brand = (
        '<div class="brand-block">'
        '<img class="hero-logo brand-logo" src="/images/aftlog-logo.png" '
        'alt="AftLog logo">'
        '<span class="kicker brand-slogan">Keeping your boat shipshape!</span>'
        '</div>'
    )
    return f"""<section class="hero hero--dark pg-hero">
  <div class="container hero-inner pg-hero-inner">
    <div class="hero-text">
      {brand}
      <h1>{title}</h1>
      <p>{sub}</p>
    </div>
  </div>
</section>"""


def section(title: str, inner: str, extra: str = "") -> str:
    return f"""<section class="section section--light {extra}">
  <div class="container">
    <h2>{title}</h2>
    {inner}
  </div>
</section>"""


# ── The AI widget (server proxy only — no keys) ─────────────────────────
AI_WIDGET = f"""<div class="ai-widget" id="aftlog-ai-widget">
  <label for="ai-q">Ask AftLog about your boat</label>
  <textarea id="ai-q" rows="3" placeholder="e.g. My outboard won't start — where do I start?"></textarea>
  <div class="ai-widget-row">
    <button class="btn btn-primary" id="ai-ask" type="button">Ask AftLog</button>
    <span class="ai-status" id="ai-status"></span>
  </div>
  <div class="ai-answer" id="ai-answer" hidden></div>
</div>
<script>
  (function () {{
    var PORTAL = "{PORTAL}";
    var DEV_KEY = "{DEV_KEY}";
    var btn = document.getElementById('ai-ask');
    var q = document.getElementById('ai-q');
    var out = document.getElementById('ai-answer');
    var status = document.getElementById('ai-status');
    btn.addEventListener('click', async function () {{
      var text = (q.value || '').trim();
      if (!text) return;
      btn.disabled = true;
      status.textContent = 'Thinking…';
      out.hidden = true;
      try {{
        var res = await fetch(PORTAL + '/ai/gemini', {{
          method: 'POST',
          headers: {{ 'content-type': 'application/json', 'x-aftlog-dev-key': DEV_KEY }},
          body: JSON.stringify({{ prompt: text, mode: 'ask', extra: {{ continue: false }} }})
        }});
        var d = await res.json();
        if (d.ok) {{
          out.textContent = d.answer;
          status.textContent = '';
        }} else {{
          out.textContent = 'Ask AftLog is temporarily offline — portal server or AI service unavailable.';
          status.textContent = '';
        }}
      }} catch (e) {{
        out.textContent = 'Portal server unreachable — check server status.';
        status.textContent = '';
      }}
      out.hidden = false;
      btn.disabled = false;
    }});
  }})();
</script>"""

# The review count badge (server proxy only)
def review_badge(container_id: str) -> str:
    return f"""<script>
  (function () {{
    var el = document.getElementById('{container_id}');
    if (!el) return;
    fetch('{PORTAL}/admin/publish', {{ headers: {{ 'x-aftlog-dev-key': '{DEV_KEY}' }} }})
      .then(function (r) {{ return r.json(); }})
      .then(function (d) {{ if (d && d.ok && typeof d.result.reviewCount === 'number') el.textContent = d.result.reviewCount; }})
      .catch(function () {{}});
  }})();
</script>"""


def review_badge_note() -> str:
    return f"""<section class="section section--light"><div class="container">
  <h2>Loved by boaters</h2>
  <p><strong id="live-review-count" class="pg-count">—</strong> reviews published on aftlog.com.</p>
  {review_badge('live-review-count')}
  <p class="pg-muted">Count comes live from the AftLog portal server.</p>
</div></section>"""


def faq_block(items):
    return "".join(
        f'<details class="pg-faq"><summary>{html.escape(q)}</summary><p>{a}</p></details>'
        for q, a in items)


# ── Content registry ────────────────────────────────────────────────────
PAGES = []


def register(slug, title, desc, body, active=None):
    PAGES.append({"slug": slug, "title": title, "desc": desc, "body": body, "active": active})


# /features
def feature_section(title: str, text: str, bullets: list, shot: str | None = None, alt: bool = False):
    cls = "section section--alt" if alt else "section section--light"
    bl = "".join(f"<li>{b}</li>" for b in bullets)
    body = (
        f"<div class=\"pg-feature-col\">"
        f"<h2>{title}</h2>"
        f"<p>{text}</p>"
        f"<ul class=\"pg-list pg-feature-bullets\">{bl}</ul>"
        f"</div>"
    )
    if shot:
        body += (
            f"<div class=\"pg-feature-shot\"><img src=\"{shot}\" "
            f"alt=\"{title} screenshot\" loading=\"lazy\"></div>"
        )
    return f"<section class=\"{cls}\"><div class=\"container pg-feature-grid\">{body}</div></section>"


def feature_cards(cards: list, title: str = "Every tool, in one place") -> str:
    items = "".join(
        f'<div class="pg-feature-card"><div class="pg-feature-icon">{icon}</div>'
        f'<h3>{title}</h3><ul class="pg-list">' +
        "".join(f"<li>{b}</li>" for b in bullets) + "</ul></div>"
        for icon, title, bullets in cards
    )
    return (f"<section class=\"section section--light\"><div class=\"container\">"
            f"<h2>{title}</h2>"
            f"<div class=\"pg-card-grid\">{items}</div></div></section>")


register(
    "features",
    "AftLog Features — Checklists, Logs, Wizards, Safety Tools",
    "Explore all AftLog features for boat owners: maintenance logging, checklists, wizards, safety tools, and a no-signal-required design.",
    hero("Features",
         "Everything AftLog does for your boat — logging, planning, checklists, and safety, built to work even with zero signal.")
    + feature_section("Maintenance Logging",
        "Track every service, part, and interval for each boat. AftLog learns your engine's real hours and tells you what's due — spark plugs at 200 hours, impellers on schedule, lower-unit oil when it's time.",
        ["Real engine-hour learning", "Smart interval tracking", "Due-soon notifications", "Multi-boat support"],
        shot="/images/screen-app-dashboard.png", alt=True)
    + feature_section("Fuel & Range Intelligence",
        "Log fills and trips and AftLog learns your real km/L and km/hr, then shows how far and how long you can run before the tank is low.",
        ["Real fuel efficiency learning", "Range prediction", "Time-to-empty estimates", "Trip history"])
    + feature_section("Checklists",
        "Launch, retrieve, towing, winterization, spring prep, and used-boat inspection — step-by-step checklists that teach as you go. Beginner Mode explains each item instead of just checking it.",
        ["Step-by-step guidance", "Beginner Mode explanations", "Seasonal workflows", "Inspection checklists"],
        shot="/images/screen-app-checklists.png", alt=True)
    + feature_section("Wizards",
        "Planner Pro, symptom decoder, buying advisor, winterization planner, float plan, compliance, manual finder, and DIY library — guided flows that turn questions into answers.",
        ["Planner Pro", "Symptom decoder", "Buying advisor", "Winterization planner", "Float plan generator"],
        shot="/images/screen-smp-plan.png")
    + feature_section("Safety Tools",
        "Emergency 'What to do if…' with GPS share, float plans, due-soon notifications, and a Boat Health Score that catches problems before they strand you.",
        ["Emergency guidance", "GPS share", "Boat Health Score", "Safety notifications"],
        shot="/images/screen-portal-health.png", alt=True)
    + feature_section("Works Without a Signal",
        "Every feature works with zero signal — your data lives on your device, no cloud required. The <a href=\"/ai.html\">AftLog AI assistant</a> reaches the server when you're connected and uses on-device guidance when you're not.",
        ["Works without a signal", "On-device storage", "On-device guidance when offline", "Zero cloud dependency"])
    + feature_cards([
        ("🧾", "Maintenance History", ["Every service recorded", "Cost insights over time"]),
        ("🚤", "Trip Log", ["GPS or odometer trips", "Season stats"]),
        ("⛽", "Fuel Log", ["Fills + odometer", "Real km/L learning"]),
        ("🚢", "Boat Profiles", ["Multiple boats", "Per-boat records"]),
        ("🔩", "Parts & Intervals", ["Parts per boat", "Interval reminders"]),
        ("🗓️", "Smart Planner", ["Prioritized plan", "Seasonal readiness"]),
        ("🩺", "Diagnostics", ["Symptom decoder", "Likely causes in order"]),
        ("📖", "Manual Extraction", ["Attach your manual", "Page-cited guidance"]),
        ("📷", "Photo Assist", ["Point at the engine", "Visual Engine Assist"]),
        ("🧭", "Float Plans", ["Share your plan", "GPS share"]),
        ("✅", "Compliance", ["Required gear", "Local rules"]),
        ("🛠️", "DIY Library", ["Step-by-step jobs", "Safety first"]),
        ("🌱", "Beginner Mode", ["Simplified dashboard", "Teaches as you go"]),
        ("📴", "Offline Mode", ["Zero signal needed", "On-device guidance"]),
        ("💬", "Ask AftLog (AI)", ["Plain-language answers", "Grounded in your boat"]),
    ])
    + (f"<section class=\"section section--light\"><div class=\"container\" style=\"text-align:center\">"
       f"<h2>Try the free web tools now</h2>"
       f"<p class=\"sec-intro\" style=\"margin-left:auto;margin-right:auto\">No install, no account — 20 boating tools that work right in your browser, offline.</p>"
       f"<p><a class=\"btn btn-secondary\" href=\"/tools/\">Browse all tools</a></p></div></section>")
    + (f"<section class=\"section section--alt pg-cta\"><div class=\"container\" style=\"text-align:center\">"
       f"<h2>Free to start. Pro for life.</h2>"
       f"<p class=\"sec-intro\" style=\"margin-left:auto;margin-right:auto\">One-time $29 lifetime Pro unlocks everything — no subscription, no ads.</p>"
       f"<p><a class=\"btn btn-primary\" href=\"/pricing.html\">See Pricing</a></p></div></section>"),
)

# /ai
register(
    "ai",
    "AftLog AI — Smart Planner, Diagnostics, Ask AftLog",
    "AI-powered maintenance planning and diagnostics for boat owners: Ask AftLog, Smart Planner, symptom diagnostics, photo analysis, manual extraction, and predictive alerts.",
    hero("AI Features",
         "A marine assistant that knows your boat — ask questions, plan maintenance, analyze photos, and diagnose problems.")
    + feature_section("Ask AftLog",
        "Ask anything about your boat in plain language. Answers are grounded in your actual boat, engine hours, and overdue services — concise, safety-first, no fluff.",
        ["Boat-aware answers", "Safety-first guidance", "No fluff", "Works on web + app"],
        alt=True)
    + f"""<section class="section section--alt" id="ai-widget"><div class="container">
      <h2>Ask AftLog — try it now</h2>
      <p>Ask AftLog anything about your boat. Questions are answered by the AftLog server — no keys in your browser.</p>
      {AI_WIDGET}
    </div></section>"""
    + feature_section("Smart Planner",
        "The maintenance planner turns intervals, usage, and season into a prioritized plan — what's due now, what's coming up, and what to do before the season starts.",
        ["Interval-based planning", "Usage-aware adjustments", "Seasonal priorities", "Pro-level insights"],
        shot="/images/screen-smp-plan.png")
    + feature_section("Diagnostics",
        "Describe a symptom — weak tell-tale, hard starting, overheating — and get the likely causes in order, with what to check first and when a mechanic is the right call.",
        ["Symptom decoding", "Ranked causes", "Step-by-step checks", "Mechanic escalation guidance"],
        alt=True)
    + feature_section("Manual Extraction",
        "Attach your engine manual: AftLog indexes it fully offline and can pull service intervals and guidance from it, citing the exact pages.",
        ["Full offline indexing", "Interval extraction", "Page citations", "Multi-manual support"])
    + feature_section("Predictive Alerts",
        "Based on your usage patterns and logged services, AftLog predicts what will need attention next — before it strands you.",
        ["Usage-based predictions", "Early warnings", "Boat Health Score integration", "Seasonal forecasting"],
        alt=True)
    + feature_section("AI Photo Analysis",
        "Take a photo of a part, a symptom, or a problem — AftLog analyzes it and tells you what it is, what's wrong, and what to do next. Works for engines, rigging, electrical, pumps, steering, and more.",
        ["Identify parts from photos", "Spot wear, corrosion, leaks, cracks", "Diagnose visual symptoms", "Suggest next steps", "Works offline (queued until connected)"],
        shot="/images/screen-vea-result.png")
    + feature_cards([
        ("⚙️", "Engine parts", ["Identify components", "Spot wear"]),
        ("⛽", "Fuel system", ["Lines & fittings", "Primer bulb, filters"]),
        ("❄️", "Cooling system", ["Impeller, thermostat", "Inlets & tell-tale"]),
        ("🔌", "Electrical system", ["Batteries, fuses", "Corrosion checks"]),
        ("🎛️", "Steering & controls", ["Cables, helm", "Fluid levels"]),
        ("💧", "Pumps & bilge", ["Pump condition", "Clogs & leaks"]),
        ("🌀", "Prop & lower unit", ["Damage, fishing line", "Anode wear"]),
        ("🧷", "Rigging & hardware", ["Clamps, bolts", "Rust & movement"]),
        ("📟", "Gauges & instruments", ["Reading issues", "Wiring signs"]),
        ("🦺", "Safety gear", ["Condition checks", "Expiry dates"]),
        ("🚤", "Hull & fittings", ["Gelcoat, thru-hulls", "Seal condition"]),
        ("🧴", "Fluids & filters", ["Oil, fuel, coolant", "Change intervals"]),
    ], title="What AftLog Can Analyze")
    + section("How It Works", """<p>The AI features run through the AftLog portal server — no keys in your app or this website. Questions and photos are processed server-side and answered back. If the service is offline, the app uses on-device guidance so you're never stuck.</p>
      <ul class="pg-list">
        <li>Server-side AI processing</li>
        <li>No keys in app or website</li>
        <li>Secure proxy architecture</li>
        <li>On-device guidance when offline</li>
      </ul>""")
    + section("Privacy & Offline Mode", """<p>AftLog works without a signal. Your logs, photos, manuals, and boat data stay on your device. AI features only reach the server when you choose to ask a question or upload a photo.</p>
      <ul class="pg-list">
        <li>Works without a signal</li>
        <li>On-device storage</li>
        <li>No cloud dependency</li>
        <li>Explicit, user-triggered AI calls</li>
      </ul>""")
    + (f"<section class=\"section section--alt pg-cta\"><div class=\"container\" style=\"text-align:center\">"
       f"<h2>Curious? Ask AftLog a question about your boat.</h2>"
       f"<p><a class=\"btn btn-primary\" href=\"/ai.html#ai-widget\">Try Ask AftLog</a></p></div></section>"),
)

# /portal
register(
    "portal",
    "AftLog Portal — Analytics & Boat Health Dashboard",
    "Web dashboard for AftLog analytics: year-in-review, planner, trip patterns, boat health, imports, and planning.",
    hero("Your boat's data, on the web",
         "Trips, maintenance, fuel, and health — visualized in the AftLog Portal.")
    + section("What's in the Portal", """<ul class="pg-list">
      <li><strong>Year in Review</strong> — your season at a glance: trips, hours, fuel, and milestones.</li>
      <li><strong>Planner</strong> — maintenance windows at 30 / 90 / 365 days.</li>
      <li><strong>Boat Health</strong> — score and breakdown across your fleet.</li>
      <li><strong>Trip patterns, heatmaps, clustering &amp; forecasts</strong> — where and when you boat, and what's next.</li>
      <li><strong>Imports</strong> — bring your AftLog data in as a bundle.</li>
    </ul>""")
    + section("Sign in and explore", """<div class="pg-actions">
      <a class="btn btn-primary" href="%PORTAL%/login">Portal login</a>
      <a class="btn btn-secondary" href="%PORTAL%/signup">Create an account</a>
      <a class="btn btn-secondary" href="%PORTAL%/portal/">Open dashboard</a>
    </div>
    <p class="pg-muted">Link the app to your portal account with a one-time code from <em>More → Link to Portal</em>.</p>
    <p>Lifetime Pro users unlock the full dashboard. See <a href="/pricing.html">pricing</a>.</p>""".replace("%PORTAL%", PORTAL))
    + review_badge_note(),
)

register(
    "pricing",
    "AftLog Pricing — Free & Lifetime Pro",
    "AftLog Pro is a one-time lifetime purchase — no subscriptions, no ads. Free tier for one boat; Pro unlocks the full toolkit.",
    hero("Pricing",
         "Free to start. Pro for life. One-time $29 — no subscription, no ads, your data stays yours.")
    + section("The two tiers", """<div class="cards cards--two pg-price-grid">
      <article class="card pg-price-card">
        <h3>Free</h3>
        <div class="pg-price">$0 <span>one-time, forever</span></div>
        <ul class="pg-list">
          <li>One boat</li>
          <li>Logbook, fuel &amp; service tracking</li>
          <li>Core checklists</li>
          <li>Works without a signal</li>
        </ul>
        <p style="margin-top:auto"><a class="btn btn-primary" href="/#waitlist">Get Started Free</a></p>
      </article>
      <article class="card pg-price-card pg-price-card--pro">
        <div class="review-badge">Lifetime</div>
        <h3>AftLog Pro</h3>
        <div class="pg-price">$29 <span>one-time, lifetime</span></div>
        <ul class="pg-list">
          <li>Unlimited boats</li>
          <li>AI assistant, Smart Planner, diagnostics</li>
          <li>Full checklists &amp; wizards</li>
          <li>Boat Health Score &amp; predictive alerts</li>
          <li>Portal analytics &amp; Year in Review</li>
        </ul>
        <p style="margin-top:auto"><a class="btn btn-primary" href="%PORTAL%/pro" target="_blank" rel="noopener">Unlock Pro — $29 Lifetime</a></p>
      </article>
    </div>""".replace("%PORTAL%", PORTAL))
    + section("One-time, lifetime — no subscriptions", """<p>AftLog Pro is a <strong>one-time $29 purchase</strong>. Licenses never expire, there are no renewals, and there is no subscription tier. You pay once and the full toolkit is yours.</p>
      <ul class="pg-list">
        <li>No subscription</li>
        <li>No renewal fees</li>
        <li>No upsells</li>
        <li>Lifetime access</li>
      </ul>
      <p>Pro codes are issued as lifetime licenses through the AftLog portal server. <a href="/faq.html">Have a question about pricing?</a></p>""")
    + section("30-day money-back guarantee", """<p>If AftLog isn't for you, request a refund within 30 days. No forms, no hoops — just contact <a href="/support.html">support</a>.</p>""")
    + section("Pricing questions", """<details class="pg-faq"><summary>Is Pro really lifetime?</summary><p>Yes — one payment, never expires, no renewals.</p></details>
      <details class="pg-faq"><summary>Does Pro work offline?</summary><p>Yes — every feature works without a signal. Only the AI assistant needs the server, and it uses on-device guidance when offline.</p></details>
      <details class="pg-faq"><summary>Can I use Pro on multiple devices?</summary><p>Yes — your license follows your AftLog portal account.</p></details>
      <details class="pg-faq"><summary>Is there a subscription version?</summary><p>No. There is no subscription tier, now or planned.</p></details>""")
    + (f"<section class=\"section section--alt pg-cta\"><div class=\"container\" style=\"text-align:center\">"
       f"<h2>Ready when you are.</h2>"
       f"<p><a class=\"btn btn-primary\" href=\"{PORTAL}/pro\" target=\"_blank\" rel=\"noopener\">Unlock Pro — $29 Lifetime</a></p>"
       f"<p class=\"pg-muted\" style=\"margin-top:10px\">30-day money-back guarantee · no subscription, ever.</p></div></section>"),
)

# /faq
register(
    "faq",
    "AftLog FAQ — Common Questions",
    "Answers to common questions about AftLog: no-signal use, safety tools, AI features, the Web Portal, pricing, and support.",
    hero("FAQ", "Straight answers to the most common questions about AftLog.")
    + section("Getting started", faq_block([
        ("What is AftLog?", "AftLog is a boat maintenance and logbook app for Canada and the USA. It tracks maintenance, fuel, trips, and costs — then turns them into clear, simple insights. It's built to teach new boaters and keep seasoned owners on schedule."),
        ("Which boats does AftLog support?", "Pleasure craft and fishing boats — outboard, inboard, and jet drives, from small runabouts to cabin cruisers."),
        ("Is there a free version?", "Yes. The free tier covers one boat with the core logbook, fuel and service tracking, and checklists."),
    ]))
    + section("Offline & privacy", faq_block([
        ("Does AftLog work without internet?", "Yes. AftLog works without a signal: your data lives on your device and every core feature works offline. The AI assistant uses the server when you're connected and uses on-device guidance when you're not."),
        ("Is my data private?", "Your data stays on your device. There's no forced account, no cloud dependency, and optional portal sync only sends what you choose."),
        ("Do you sell my email or data?", "No. The waitlist email is only used to tell you when AftLog is ready, and we never sell personal data or run ads."),
    ]))
    + section("AI features", faq_block([
        ("What does the AI assistant do?", "Ask AftLog answers maintenance questions grounded in your boat, the Smart Planner schedules what's due, and diagnostics walk symptoms to likely causes. Photo analysis identifies parts and visible issues. Everything goes through the AftLog server — the app never holds AI keys."),
        ("Does the AI work offline?", "The AI needs the AftLog server for answers. Offline, the app uses on-device guidance so you're never stuck on the water."),
        ("Is my photo or question sent anywhere?", "Only when you choose to ask: questions and photos go to the AftLog server to produce an answer, then the interaction is done."),
    ]))
    + section("Web Portal", faq_block([
        ("What is the Web Portal?", "A free companion dashboard on the web: Year in Review, planner windows, boat health, and trip analytics. Link your app with a one-time code from More → Link to Portal."),
        ("Is the Portal free?", "The portal is included with the app. Lifetime Pro users unlock the full dashboard including planner windows and boat health."),
    ]))
    + section("Pricing & license", faq_block([
        ("Is AftLog really a one-time purchase?", "Yes. AftLog Pro is $29 one-time for a lifetime license — no subscriptions, no renewals, no ads."),
        ("Can I use Pro on multiple devices?", "Yes — your lifetime license follows your AftLog portal account."),
        ("Is there a money-back guarantee?", "Yes — 30 days, no forms. Email support for a refund."),
    ]))
    + section("Support", faq_block([
        ("How do I get help?", "See the support page for troubleshooting and contact, or email aftlog@yahoo.com — we usually reply within a day."),
    ]))
    + section("Still have questions?", '<div class="pg-actions"><a class="btn btn-primary" href="/support.html">Contact support</a><a class="btn btn-secondary" href="/help/index.html">Browse Help</a></div>'),
)


# /support
register(
    "support",
    "AftLog Support — Contact & Help",
    "Get help with AftLog: troubleshooting guides, contact form, and links to the FAQ.",
    hero("Support",
         "Troubleshooting first, then a human — in that order.")
    + section("Troubleshooting", faq_block([
        ("App won't install or update?", "Make sure you're installing the signed AftLog APK and that 'Install unknown apps' is allowed for your file manager."),
        ("GPS not tracking?", "Grant location permission when the app asks — AftLog uses it only for trip tracking you start yourself."),
        ("Reminders not firing?", "Check notification permission and ensure the app isn't force-stopped by your battery saver."),
        ("AI assistant offline?", "The assistant needs a connection to the AftLog server; without one it uses on-device guidance."),
        ("Backup / restore?", "Use More → Backup to export a JSON file — keep it somewhere safe."),
    ]))
    + section("Contact", """<p>For anything else, email aftlog@yahoo.com or use the form on the landing page. We usually reply within a day.</p>
      <p><a class="btn btn-primary" href="mailto:aftlog@yahoo.com?subject=AftLog%20support">Email Support</a></p>""")
    + section("New to the app?", """<p>Start with the blog — the beginner checklist and winterization guide cover the essentials.</p>
      <div class="pg-actions">
        <a class="btn btn-secondary" href="/blog/beginner-checklist.html">Beginner Checklist</a>
        <a class="btn btn-secondary" href="/blog/winterize.html">Winterization Guide</a>
      </div>"""),
)

# Blog
def article_card(slug, title, desc):
    return f'<article class="card"><h3><a href="/blog/{slug}.html">{html.escape(title)}</a></h3><p>{html.escape(desc)}</p></article>'


def article(slug, title, desc, category, body_html, related):
    brand = (
        '<div class="brand-block">'
        '<img class="hero-logo brand-logo" src="/images/aftlog-logo.png" '
        'alt="AftLog logo">'
        '<span class="kicker brand-slogan">Keeping your boat shipshape!</span>'
        '</div>'
    )
    return f"""<section class="hero hero--dark pg-hero"><div class="container hero-inner pg-hero-inner"><div class="hero-text">
      {brand}
      <span class="kicker">{category} · AftLog Blog</span>
      <h1>{title}</h1>
      <p>{desc}</p>
    </div></div></section>
    <section class="section section--light"><div class="container pg-article">
      {body_html}
      <p class="pg-muted">Track these on your boat with <a href="/features.html">AftLog</a> — <a href="/pricing.html">free to start, $29 lifetime Pro</a>.</p>
      <h3>Related</h3><ul class="pg-list">{related}</ul>
    </div></section>"""

register("blog/lower-unit-service", "Lower-Unit Service Guide — When to Change Gear Oil and Why It Matters", "Learn when to service your outboard's lower unit, how often to change gear oil, symptoms of trouble, and how proper maintenance prevents costly failures.",
         article("lower-unit-service", "Lower-Unit Service: When and Why",
                 "Your outboard's lower unit is one of the hardest-working parts of the engine — and one of the easiest to maintain. Here's when to service it, why it matters, and how to avoid expensive failures.",
                 "Maintenance", """<img class="blog-hero" src="/images/screen-lower-unit.png" alt="Lower unit (gearcase) diagram showing the drain and vent screws" loading="lazy">
      <p>Your outboard's lower unit — the gearcase at the bottom of the engine — is a compact, sealed system that transfers power from the driveshaft to the propeller. Inside it are gears, bearings, seals, and oil. It's simple, rugged, and designed to survive thousands of hours on the water. But it has one vulnerability: water intrusion.</p>
      <p>Lower-unit service is one of the most important maintenance tasks for any boat owner. It's inexpensive, quick, and prevents catastrophic failures. Yet many owners overlook it until something goes wrong — usually when the prop stops turning, the engine revs freely, and the day is over.</p>
      <h2>Why Lower-Unit Service Matters</h2>
      <p>The lower unit is a sealed gearbox filled with specialized gear oil. That oil:</p>
      <ul class="pg-list"><li>Lubricates gears and bearings</li><li>Reduces friction</li><li>Prevents corrosion</li><li>Carries away heat</li><li>Protects against wear</li></ul>
      <p>If water enters the gearcase — through a worn seal, fishing line wrapped around the prop shaft, or a damaged gasket — the oil becomes milky, thin, and ineffective. Once that happens, the gears grind themselves apart.</p>
      <p>A lower-unit rebuild can cost <strong>$800–$2,500</strong>, depending on the engine. A replacement gearcase can cost <strong>$1,500–$4,000</strong>. A bottle of gear oil costs <strong>$10–$15</strong>. That's why lower-unit service is one of the highest-value maintenance tasks you can perform.</p>
      <h2>When to Service the Lower Unit</h2>
      <p>Manufacturers generally recommend <strong>every 100 hours or once per season</strong> — whichever comes first. For most recreational boaters, that means once in fall (during winterization) and once in spring (during de-winterization). But there are additional times you should check or change the oil:</p>
      <ul class="pg-list"><li><strong>After hitting bottom or striking debris</strong> — a hard impact can damage seals.</li><li><strong>After running through heavy weeds or fishing line</strong> — line around the prop shaft can cut the seal.</li><li><strong>If you notice milky oil during a mid-season check</strong> — milky means water intrusion, an immediate service.</li><li><strong>If the prop feels loose or wobbly</strong> — this can indicate bearing wear.</li><li><strong>If you hear grinding or whining at low speeds</strong> — gear wear often starts quietly.</li><li><strong>If the engine sat unused for more than a year</strong> — oil degrades over long storage.</li></ul>
      <p>AftLog's maintenance tracker uses the manufacturer's interval (100 hours) and your logged trips to remind you automatically.</p>
      <h2>How Lower-Unit Service Works</h2>
      <p>Lower-unit service is simple and takes 10–20 minutes.</p>
      <ol class="pg-list"><li><strong>Remove the drain screw</strong> — located at the bottom of the gearcase.</li><li><strong>Remove the vent screw</strong> — located above the drain screw, so the oil flows out quickly.</li><li><strong>Inspect the oil</strong> — the most important step. Look for milky oil (water intrusion), metal flakes (gear wear), a burnt smell (overheating), or very dark oil (overdue service).</li><li><strong>Replace the crush washers</strong> — these small gaskets prevent leaks.</li><li><strong>Pump in fresh gear oil</strong> — fill from the bottom until oil flows out the top vent.</li><li><strong>Reinstall screws</strong> — tighten to manufacturer torque specs.</li></ol>
      <p>That's it — one of the simplest services on the engine.</p>
      <h2>What Happens If You Ignore Lower-Unit Service</h2>
      <p>Skipping lower-unit service doesn't cause immediate failure. Instead, damage builds slowly and silently:</p>
      <ol class="pg-list"><li><strong>Water intrusion begins</strong> — a seal wears out or fishing line cuts the prop-shaft seal.</li><li><strong>Oil becomes milky</strong> — lubrication drops dramatically.</li><li><strong>Bearings begin to wear</strong> — you may hear faint whining at idle.</li><li><strong>Gears begin to pit</strong> — metal flakes appear in the oil.</li><li><strong>Gear teeth strip</strong> — the prop stops turning; the engine revs but the boat doesn't move.</li><li><strong>Complete failure</strong> — the lower unit must be rebuilt or replaced.</li></ol>
      <p>This entire chain of events can be prevented by changing the oil twice a year.</p>
      <h2>Common Symptoms of Lower-Unit Problems</h2>
      <p>If you notice any of these, service the lower unit immediately:</p>
      <ul class="pg-list"><li>Milky oil</li><li>Metal flakes in oil</li><li>Grinding or whining noises</li><li>Prop shaft wobble</li><li>Oil leaking around the prop</li><li>Difficulty shifting into gear</li><li>Vibration at low speeds</li></ul>
      <p>AftLog's symptom decoder can help identify these issues and recommend next steps.</p>
      <h2>How to Prevent Lower-Unit Damage</h2>
      <p>Lower-unit failures are almost always preventable:</p>
      <ol class="pg-list"><li><strong>Change gear oil twice a year</strong> — spring and fall.</li><li><strong>Inspect the prop shaft regularly</strong> — remove the prop and check for fishing line.</li><li><strong>Replace seals proactively</strong> — especially in weedy or debris-heavy areas.</li><li><strong>Avoid shifting aggressively</strong> — slamming into gear stresses the clutch dog and gears.</li><li><strong>Don't run aground</strong> — even soft sand can damage seals.</li><li><strong>Store the engine upright</strong> — keeps water from settling in the gearcase.</li><li><strong>Use manufacturer-approved gear oil</strong> — engines differ in viscosity and additives.</li></ol>
      <h2>DIY vs. Professional Service</h2>
      <p>Lower-unit service is one of the easiest DIY tasks — you need a screwdriver, a gear-oil pump, two bottles of gear oil, and new crush washers. But consider professional service if the oil is milky, metal flakes are present, seals are damaged, the prop shaft wobbles, shifting feels rough, or you suspect internal wear. A technician can pressure-test the gearcase to find leaks.</p>
      <h2>Checklist: Lower-Unit Service</h2>
      <ul class="pg-list"><li>Remove the prop and inspect for fishing line</li><li>Check the prop shaft for wobble</li><li>Remove the drain and vent screws</li><li>Inspect oil for color, smell, and metal</li><li>Replace crush washers</li><li>Pump fresh oil from the bottom until full</li><li>Reinstall screws to proper torque</li><li>Clean the exterior of the gearcase</li><li>Log the service in AftLog</li></ul>
      <h2>Summary</h2>
      <p>Lower-unit service is simple, inexpensive, and essential. Changing gear oil twice a year prevents water intrusion, protects gears and bearings, and saves you from costly repairs. Whether you do it yourself or have a shop handle it, staying ahead of lower-unit maintenance is one of the smartest things you can do for your boat.</p>
      <p>AftLog tracks your hours, logs your trips, and reminds you when service is due — so your lower unit stays healthy season after season.</p>""",
                 '<li><a href="outboard-oil.html">How often to change outboard oil</a></li><li><a href="winterize.html">How to winterize your boat</a></li><li><a href="beginner-checklist.html">Boat maintenance checklist for beginners</a></li>'),
         active="/blog/")


register("blog/spark-plug-intervals", "Outboard Spark Plug Intervals — When to Replace Them and Why It Matters", "Learn when to change outboard spark plugs, the symptoms of worn plugs, how intervals differ by engine type, and how AftLog tracks replacement schedules automatically.",
         article("spark-plug-intervals", "Spark Plug Intervals Explained",
                 "Spark plugs are small, inexpensive, and critical. Replacing them on schedule keeps your outboard starting easily, idling smoothly, and running at full power. Here's how often to change them — and how to spot trouble early.",
                 "Maintenance", """<img class="blog-hero" src="/images/screen-spark-plugs.png" alt="Outboard ignition system diagram — spark plugs are part of the ignition system, which the guide covers" loading="lazy">
      <p>Spark plugs are the unsung heroes of your outboard engine. They ignite the air-fuel mixture thousands of times per minute, under heat, pressure, vibration, and moisture. They're small, inexpensive, and easy to replace — yet they have a massive impact on how your engine starts, idles, accelerates, and performs under load.</p>
      <p>Replacing spark plugs on schedule is one of the simplest ways to keep your outboard reliable. But many boat owners aren't sure how often to change them, what symptoms to watch for, or how plug wear affects engine performance. This guide explains when to replace spark plugs, why the interval matters, how to identify worn plugs, and what happens if you push them too far.</p>
      <h2>Why Spark Plug Intervals Matter</h2>
      <p>Spark plugs degrade over time due to heat cycles, carbon buildup, fuel quality, moisture exposure, electrode wear, oil fouling, and ethanol-related deposits. As plugs wear, they produce a weaker spark, which leads to:</p>
      <ul class="pg-list"><li>Hard starting</li><li>Rough idle</li><li>Misfires</li><li>Poor acceleration</li><li>Reduced fuel economy</li><li>Lower top-end power</li><li>Increased emissions</li><li>Unburned fuel washing down the cylinder walls</li></ul>
      <p>A $6 spark plug can prevent a $600 repair. That's why manufacturers specify strict replacement intervals — and why AftLog tracks them automatically based on your engine model and logged hours.</p>
      <h2>Recommended Spark Plug Intervals</h2>
      <p>Most outboard manufacturers follow similar guidelines: <strong>every 100 hours or once per season</strong>, whichever comes first. This applies to Mercury, Yamaha, Honda, Suzuki, Evinrude (legacy), and Tohatsu. But there are exceptions based on engine type.</p>
      <h3>Two-Stroke vs. Four-Stroke Intervals</h3>
      <p><strong>Two-stroke outboards</strong> burn oil with fuel, which creates more deposits — expect <strong>every 50–100 hours</strong>, and foul sooner if you troll a lot or idle at low RPM. <strong>Four-stroke outboards</strong> burn cleaner — <strong>every 100 hours</strong>. Some modern EFI engines can stretch to 200 hours, but only with perfect fuel quality and ideal running conditions.</p>
      <h3>EFI vs. Carbureted Engines</h3>
      <p><strong>Carbureted engines</strong> are more prone to rich mixtures, uneven fuel distribution, and carbon buildup — <strong>every 50–75 hours</strong>. <strong>EFI engines</strong> have more precise fuel control — <strong>every 100 hours</strong>.</p>
      <h3>High-Performance or High-Load Use</h3>
      <p>If you run long distances at WOT, tow tubes or skiers, carry heavy loads, run offshore, or operate in extreme heat, plugs wear faster — <strong>every 75 hours</strong>.</p>
      <h2>Symptoms of Worn Spark Plugs</h2>
      <p>Spark plug wear is gradual, but the symptoms are easy to spot once you know them:</p>
      <ol class="pg-list"><li><strong>Hard starting</strong> — the engine cranks longer than usual or needs throttle to start.</li><li><strong>Rough idle</strong> — vibration, sputtering, or inconsistent RPM at idle.</li><li><strong>Misfires</strong> — a momentary stumble or hesitation when accelerating.</li><li><strong>Poor fuel economy</strong> — you burn more fuel to hold the same speed.</li><li><strong>Reduced power</strong> — the engine feels sluggish or struggles to reach top RPM.</li><li><strong>Black, sooty, or wet plugs</strong> — indicates fouling or a rich mixture.</li><li><strong>White or burned electrodes</strong> — indicates overheating or a lean mixture.</li><li><strong>Fuel smell at idle</strong> — unburned fuel from a weak spark.</li></ol>
      <p>If you notice any of these, replace the plugs immediately — even if you haven't reached the hour interval.</p>
      <h2>How to Inspect Spark Plugs</h2>
      <p>Spark plug inspection is simple and takes 10 minutes.</p>
      <ol class="pg-list"><li><strong>Remove one plug at a time</strong> — prevents mixing up the wires.</li><li><strong>Check color</strong> — healthy plugs are light tan, dry, and clean around the electrode.</li><li><strong>Check deposits</strong> — black soot means a rich mixture; wet or oily means fouling; white crust means overheating; metallic specks mean internal wear.</li><li><strong>Check the gap</strong> — with a feeler gauge; a widened gap means the plug is worn.</li><li><strong>Check threads and insulator</strong> — cracks or damage mean immediate replacement.</li></ol>
      <h2>What Happens If You Don't Replace Spark Plugs</h2>
      <ol class="pg-list"><li><strong>Weak spark</strong> — hard starting and rough idle begin.</li><li><strong>Misfires</strong> — acceleration becomes inconsistent.</li><li><strong>Fuel washdown</strong> — unburned fuel removes oil from the cylinder walls.</li><li><strong>Carbon buildup</strong> — deposits form on valves and pistons.</li><li><strong>Coil stress</strong> — ignition coils work harder and may fail.</li><li><strong>Engine damage</strong> — long-term misfires can damage rings and valves.</li></ol>
      <p>A $6 plug can prevent a $300 coil failure or a $1,200 valve job.</p>
      <h2>DIY vs. Professional Replacement</h2>
      <p>Spark plug replacement is one of the easiest DIY tasks. You need a socket wrench, a spark plug socket, a feeler gauge, dielectric grease, and manufacturer-specified plugs. DIY is recommended if you're comfortable with basic tools, your engine is easily accessible, and you want to save money. Use a professional if plugs are hard to reach, you suspect deeper issues, plugs show abnormal wear, or you want a full tune-up.</p>
      <h2>How AftLog Tracks Spark Plug Intervals</h2>
      <p>AftLog automatically reads your engine model, applies manufacturer intervals, tracks your logged hours, reminds you when plugs are due, logs replacement dates, stores photos of plug condition, and notes symptoms that mean it's time to replace them early — keeping your ignition system healthy season after season.</p>
      <h2>Checklist: Spark Plug Replacement</h2>
      <ul class="pg-list"><li>Remove one plug at a time</li><li>Inspect color and deposits</li><li>Check the gap</li><li>Install the new plug</li><li>Apply dielectric grease</li><li>Torque to manufacturer spec</li><li>Reconnect the wire firmly</li><li>Log the replacement in AftLog</li></ul>
      <h2>Summary</h2>
      <p>Spark plugs are small but critical. Replacing them every 100 hours — or sooner for two-strokes and carbureted engines — keeps your outboard starting easily, idling smoothly, and running at full power. By watching for symptoms and inspecting plugs regularly, you can prevent misfires, fuel waste, and long-term engine damage.</p>
      <p>AftLog tracks your intervals automatically — so you never miss a replacement.</p>""",
                 '<li><a href="lower-unit-service.html">Lower-unit service: when and why</a></li><li><a href="outboard-oil.html">How often to change outboard oil</a></li><li><a href="winterize.html">How to winterize your boat</a></li>'),
         active="/blog/")


register("blog/impeller-replacement", "Outboard Impeller Replacement — Symptoms, Timing, and Why It Matters", "Learn when to replace your outboard impeller, how to spot early symptoms of failure, and why timely water-pump service prevents overheating and engine damage.",
         article("impeller-replacement", "Impeller Replacement: Symptoms and Timing",
                 "Your impeller is the heart of your cooling system. When it wears out, your engine overheats — fast. Here's how to know when it's time to replace it, what symptoms to watch for, and how often to service it.",
                 "Maintenance", """<img class="blog-hero" src="/images/screen-impeller.png" alt="Outboard water-pump diagram — the impeller sits inside the water-pump housing it shows" loading="lazy">
      <p>Your outboard's impeller is a small rubber component with flexible vanes that spin inside the water-pump housing. Its job is simple: pull water from outside the boat and push it through the engine to keep it cool. Without it, your engine overheats within minutes.</p>
      <p>Despite its importance, the impeller is one of the most overlooked maintenance items on small boats. Many owners don't know when to replace it, what symptoms indicate trouble, or how impeller wear affects engine performance. This guide explains when to replace your impeller, why timing matters, how to spot early symptoms, and what happens if you ignore the warning signs.</p>
      <h2>Why Impeller Replacement Matters</h2>
      <p>The impeller is made of rubber. Over time rubber dries out, cracks, stiffens, loses flexibility, becomes brittle, and wears unevenly. When the vanes can't flex properly, the pump loses pressure, cooling water flow drops, and the engine overheats.</p>
      <p>Overheating is one of the fastest ways to damage an outboard. It can cause warped heads, melted pistons, scored cylinders, blown head gaskets, failed thermostats, and damaged sensors. A <strong>$20–$40 impeller</strong> prevents a <strong>$1,000–$4,000 repair</strong>.</p>
      <h2>Recommended Impeller Replacement Intervals</h2>
      <p>Most manufacturers recommend replacing the impeller <strong>every 2–3 years</strong> for recreational use — but there are important exceptions.</p>
      <p><strong>Replace every year if</strong> you run in sandy or silty water, operate in shallow rivers, beach your boat frequently, run in weedy lakes, store the engine for long periods, or run high hours (150+ per season). <strong>Replace immediately if</strong> the tell-tale stream weakens, the engine overheats, you sucked up sand or debris, the impeller sat dry for months, or you bought a used engine with unknown history.</p>
      <p>AftLog tracks impeller intervals automatically based on your engine model and logged hours.</p>
      <h2>Symptoms of a Worn or Failing Impeller</h2>
      <p>Impeller failure rarely happens suddenly. Instead, symptoms appear gradually — if you know what to look for:</p>
      <ol class="pg-list"><li><strong>Weak or intermittent tell-tale stream</strong> — the most common early warning sign. A healthy impeller produces a strong, steady stream; a failing one produces weak flow, sputtering flow, delayed flow after startup, or flow that disappears at idle.</li><li><strong>Engine overheating</strong> — if the temperature alarm sounds, check the impeller first.</li><li><strong>High idle temperature</strong> — if idle temps creep higher over time, the impeller may be losing efficiency.</li><li><strong>Steam in the tell-tale</strong> — indicates hot water and restricted flow.</li><li><strong>No tell-tale at startup</strong> — if it doesn't appear within 5–10 seconds, shut down immediately.</li><li><strong>Debris in the water-pump housing</strong> — sand, silt, or weeds can damage the vanes.</li><li><strong>Rubber smell</strong> — a faint burning-rubber smell can indicate vane friction or failure.</li></ol>
      <h2>What Happens If You Don't Replace the Impeller</h2>
      <ol class="pg-list"><li><strong>Vanes stiffen</strong> — cooling efficiency drops.</li><li><strong>Vanes crack</strong> — water flow becomes inconsistent.</li><li><strong>Vanes break off</strong> — pieces of rubber travel through the cooling system.</li><li><strong>Water passages clog</strong> — overheating becomes severe.</li><li><strong>Engine overheats</strong> — the temperature alarm sounds.</li><li><strong>Internal damage</strong> — pistons, cylinders, and head gaskets fail.</li><li><strong>Engine shutdown</strong> — severe overheating forces an emergency stop.</li></ol>
      <p>Replacing the impeller every 2–3 years prevents all of this.</p>
      <h2>How Impeller Replacement Works</h2>
      <p>Impeller replacement is moderately simple and takes 30–60 minutes.</p>
      <ol class="pg-list"><li><strong>Remove the lower unit</strong> — unbolt the gearcase from the midsection.</li><li><strong>Access the water-pump housing</strong> — located on top of the lower unit.</li><li><strong>Remove the housing</strong> — inspect for sand, silt, or debris.</li><li><strong>Remove the old impeller</strong> — check for missing vanes.</li><li><strong>Install the new impeller</strong> — lubricate with water-pump grease.</li><li><strong>Replace the housing gasket</strong> — ensures proper sealing.</li><li><strong>Reinstall the lower unit</strong> — align the driveshaft and shift shaft.</li><li><strong>Test the tell-tale</strong> — start the engine and verify strong flow.</li></ol>
      <p>If vanes are missing, the cooling passages may need flushing.</p>
      <h2>DIY vs. Professional Replacement</h2>
      <p>Impeller replacement is DIY-friendly if you're comfortable removing the lower unit, your engine is small (2–60 HP), bolts are accessible, and you have a manual. Use a professional if your engine is large (90–300 HP), bolts are corroded, you suspect overheating damage, vanes are missing, or you want a full cooling-system inspection.</p>
      <h2>How AftLog Helps</h2>
      <p>AftLog automatically tracks impeller intervals, logs replacement dates, stores photos of impeller condition, notes symptoms (weak tell-tale, overheating), reminds you when service is due, and links to your engine's maintenance schedule.</p>
      <h2>Checklist: Impeller Replacement</h2>
      <ul class="pg-list"><li>Remove the lower unit</li><li>Inspect the housing for debris</li><li>Remove the old impeller</li><li>Check for missing vanes</li><li>Install the new impeller</li><li>Replace the gasket</li><li>Reinstall the lower unit</li><li>Test the tell-tale</li><li>Log the service in AftLog</li></ul>
      <h2>Summary</h2>
      <p>Your impeller is the heart of your cooling system. Replacing it every 2–3 years — or sooner in harsh conditions — prevents overheating, protects your engine, and ensures reliable performance. By watching for symptoms like weak tell-tale flow and rising temperatures, you can catch impeller wear early and avoid costly repairs.</p>
      <p>AftLog tracks your intervals automatically, so you never miss a replacement.</p>""",
                 '<li><a href="spark-plug-intervals.html">Spark plug intervals explained</a></li><li><a href="lower-unit-service.html">Lower-unit service: when and why</a></li><li><a href="battery-care-small-boats.html">Battery care for small boats</a></li>'),
         active="/blog/")

register("blog/battery-care-small-boats", "Boat Battery Care Guide — Charging, Storage, and Seasonal Maintenance", "Learn how to care for your boat's battery, prevent off-season failure, extend lifespan, and keep your electrical system reliable all season long.",
         article("battery-care-small-boats", "Battery Care for Small Boats",
                 "Boat batteries rarely die on the water — they die in storage. Here's how to charge, maintain, and store your battery properly so your boat starts strong every time.",
                 "Maintenance", """<img class="blog-hero" src="/images/screen-battery-care.png" alt="Marine battery system diagram — charging, terminals, and connections" loading="lazy">
      <p>A reliable battery is one of the most important components on a small boat. It powers your starter motor, electronics, bilge pump, lights, GPS, fish finder, radio, and safety equipment. When a battery fails, your day on the water can end abruptly — or worse, you may find yourself unable to start the engine or call for help.</p>
      <p>The surprising truth is that most boat batteries don't fail on the water. They fail in storage, during the off-season, when they sit unused, slowly discharging, sulfating, and deteriorating. Proper battery care is simple, inexpensive, and dramatically extends battery life. This guide explains how to care for your battery, store it, charge it, prevent early failure, and how AftLog tracks battery health.</p>
      <h2>Why Boat Batteries Fail</h2>
      <p>Boat batteries live a harder life than car batteries. They face vibration, moisture, temperature swings, long periods of inactivity, deep discharges, inconsistent charging, and corrosion from salt or humidity. The most common failure causes are:</p>
      <ol class="pg-list"><li><strong>Sulfation</strong> — when a battery sits partially discharged, lead sulfate crystals form on the plates, reducing capacity.</li><li><strong>Deep discharge</strong> — running electronics for hours without charging can drain the battery below safe levels.</li><li><strong>Off-season neglect</strong> — batteries slowly discharge over winter; below 10.5 volts causes permanent damage.</li><li><strong>Corroded terminals</strong> — loose or corroded terminals reduce voltage and cause hard starting.</li><li><strong>Overcharging</strong> — cheap chargers can overcharge and boil the electrolyte.</li><li><strong>Vibration damage</strong> — loose batteries can crack plates or damage internal connections.</li></ol>
      <h2>Types of Boat Batteries</h2>
      <p><strong>Flooded lead-acid (FLA)</strong> — traditional, affordable, reliable; but requires topping up water, is sensitive to vibration, and prone to sulfation. <strong>AGM (absorbed glass mat)</strong> — sealed, maintenance-free, vibration-resistant, charges faster, low self-discharge; but more expensive and sensitive to overcharging. <strong>Lithium (LiFePO4)</strong> — modern, lightweight, long-lasting, deep-cycle friendly, stable voltage; but expensive, needs a compatible charger, and isn't ideal for cold climates.</p>
      <p>AftLog lets you specify your battery type so maintenance reminders match your setup.</p>
      <h2>How to Charge Your Boat Battery Properly</h2>
      <p>Charging is the most important part of battery care. Use a <strong>smart charger</strong> — it regulates voltage, prevents overcharging, maintains float charge, desulfates plates, and shuts off when full. Avoid cheap trickle chargers, which can overcharge. Charge after every outing (even short trips drain the battery slightly), keep the battery above <strong>12.4 volts</strong> (below this sulfation begins), avoid deep discharges (never below 50% unless it's a deep-cycle model), and check charging-system output — your outboard should produce 13.8–14.4 volts at cruising RPM, or the alternator/regulator may be failing.</p>
      <h2>Off-Season Battery Storage</h2>
      <p>Most battery failures happen during winter storage. Here's how to prevent them:</p>
      <ol class="pg-list"><li><strong>Fully charge the battery before storage</strong> — less likely to sulfate.</li><li><strong>Disconnect the terminals</strong> — prevents parasitic drain.</li><li><strong>Store in a cool, dry place</strong> — ideal 5–15°C (40–60°F); avoid freezing.</li><li><strong>Use a smart maintainer</strong> — holds a safe float voltage all winter.</li><li><strong>Check voltage monthly</strong> — below 12.4V, recharge immediately.</li><li><strong>Avoid concrete floors</strong> — moisture can still cause discharge.</li><li><strong>Clean terminals before storage</strong> — corrosion accelerates in inactivity.</li></ol>
      <h2>How to Inspect Your Battery</h2>
      <ol class="pg-list"><li><strong>Check voltage</strong> — healthy resting voltage is 12.6–12.8V.</li><li><strong>Check terminals</strong> — corrosion, loose connections, or frayed cables.</li><li><strong>Check the case</strong> — swelling or bulging indicates internal damage.</li><li><strong>Check electrolyte</strong> (flooded batteries) — plates covered; top up with distilled water.</li><li><strong>Check age</strong> — lead-acid 3–5 years, AGM 4–7 years, lithium 8–12 years; replace proactively if older.</li></ol>
      <h2>Symptoms of a Weak or Failing Battery</h2>
      <ul class="pg-list"><li>Slow cranking</li><li>Clicking sound when starting</li><li>Dim lights</li><li>Electronics shutting off</li><li>Voltage dropping quickly under load</li><li>Battery not holding a charge</li><li>Corrosion buildup</li><li>Swollen case</li></ul>
      <p>If you notice any of these, test or replace the battery.</p>
      <h2>How AftLog Helps</h2>
      <p>AftLog automatically tracks battery age, logs voltage readings, stores photos of terminal condition, reminds you to charge after trips, provides off-season storage checklists, notes symptoms of battery failure, and helps diagnose electrical issues.</p>
      <h2>Checklist: Battery Care</h2>
      <ul class="pg-list"><li>Charge after every outing</li><li>Keep voltage above 12.4V</li><li>Inspect terminals monthly</li><li>Clean corrosion immediately</li><li>Use a smart charger</li><li>Store fully charged</li><li>Disconnect terminals for winter</li><li>Check voltage monthly during storage</li><li>Log battery age in AftLog</li></ul>
      <h2>Summary</h2>
      <p>Boat batteries are simple, but they require consistent care. Charging properly, storing correctly, and inspecting regularly will dramatically extend battery life and prevent off-season failure. Whether you use lead-acid, AGM, or lithium, following these steps ensures your boat starts strong every time.</p>
      <p>AftLog tracks battery health automatically — so you're never caught off guard.</p>""",
                 '<li><a href="impeller-replacement.html">Impeller replacement: symptoms and timing</a></li><li><a href="spark-plug-intervals.html">Spark plug intervals explained</a></li><li><a href="lower-unit-service.html">Lower-unit service: when and why</a></li>'),
         active="/blog/")


register("blog/engine-wont-start", "Outboard Won't Start — Step-by-Step Troubleshooting Guide for Small Boats", "Learn what to do when your outboard won't start, the most common causes, how to troubleshoot safely on the water, and when to call for help.",
         article("engine-wont-start", "How to Handle an Engine That Won't Start",
                 "Few moments in boating are more frustrating than an engine that won't start. Here's the calm, step-by-step process every boater should follow to diagnose the problem and get back underway safely.",
                 "Safety", """<img class="blog-hero" src="/images/screen-engine-wont-start.png" alt="Marine electrical system diagram — battery power is the first thing to check when an engine won't start" loading="lazy">
      <p>Few moments in boating are more stressful than turning the key — or pressing the start button — and hearing nothing. No crank. No click. No ignition. Just silence. Whether you're at the dock, at the ramp, or drifting offshore, an engine that won't start can turn a great day into a tense one.</p>
      <p>The good news is that most \u201cwon't start\u201d situations are caused by simple, fixable issues. With a calm, methodical approach, you can diagnose the problem quickly and often get the engine running again without tools or technical knowledge.</p>
      <h2>Stay Calm and Think Systematically</h2>
      <p>When an engine won't start, panic is your enemy. Outboards are simple machines. They need only three things to start: spark, fuel, and air — plus, rarely, compression. And before any of that, they need electrical power and the safety interlocks satisfied.</p>
      <p>Most starting failures fall into one of these categories: battery or electrical issue, kill-switch or safety interlock, fuel delivery problem, flooding, vapor lock, starter motor or solenoid issue, or an ignition-system fault.</p>
      <h2>Step 1 — Check the Kill-Switch (Most Common Cause)</h2>
      <p>The kill-switch lanyard is responsible for more \u201cwon't start\u201d situations than any other single cause. Make sure the lanyard is clipped in properly — even a slightly loose clip prevents starting. Check for hidden kill-switches: some boats have a helm kill-switch, stern kill-switch, wireless fob kill-switch, or neutral-safety interlock. If any are tripped, the engine will not crank. Typical symptoms are no crank, no click, gauges may still power on, and the starter does nothing. If the kill-switch is the problem, fixing it often restores immediate starting.</p>
      <h2>Step 2 — Check Battery Power</h2>
      <p>If the kill-switch is fine, the next most common issue is battery power. Turn on accessories — do the lights, horn, or electronics work? If everything is dead, the battery is fully discharged or disconnected. If accessories work but the engine won't crank, the battery may be weak, corroded, poorly connected, or unable to supply starter current. Check the terminals for corrosion, loose clamps, broken wires, or frayed cables. Tighten terminals firmly; corrosion can be cleaned with a knife, key, or even a coin in an emergency. If the engine cranks now, the issue was a loose or corroded connection.</p>
      <h2>Step 3 — Check the Gear Selector</h2>
      <p>Outboards will not start unless the gear selector is in neutral. Move the shifter firmly into neutral — sometimes the detent is soft or misaligned. Try wiggling slightly while starting. Symptoms of a neutral-safety issue are no crank, no click, working gauges, and a fine battery. If the engine starts after adjusting the shifter, the neutral-safety switch was the culprit.</p>
      <h2>Step 4 — Check the Fuel System</h2>
      <p>If the engine cranks but won't start, the issue is usually fuel: check the fuel level; check the fuel line for kinks, disconnected fittings, or a collapsed hose; and check the primer bulb — it should be firm when squeezed (if soft, squeeze until firm, listen for fuel entering the engine, and check for air leaks at fittings). Check the tank vent — a closed vent causes vacuum lock (symptoms: engine starts then dies, bulb collapses, fuel flow stops). And check the fuel filter — if you have a clear bowl, look for water, debris, or phase-separated ethanol.</p>
      <h2>Step 5 — Check for Flooding</h2>
      <p>Flooding happens when too much fuel enters the cylinders. Symptoms include a strong fuel smell, the engine cranking but not firing, sputtering, and wet spark plugs. To clear flooding: open the throttle fully (fast idle lever or throttle-only mode), crank for 5–10 seconds, release the throttle, then try starting normally.</p>
      <h2>Step 6 — Check for Vapor Lock (Hot Restart Problems)</h2>
      <p>Vapor lock occurs when fuel vaporizes in the lines on hot days: the engine ran fine earlier, won't restart after sitting hot, the bulb is soft, and it sputters but won't fire. Fix: squeeze the primer bulb until firm, open the tank vent, wait 2–3 minutes, and try starting again.</p>
      <h2>Step 7 — Check the Starter Motor and Solenoid</h2>
      <p>If you hear a click, repeated clicking, or slow cranking, the starter or solenoid may be the issue. Try tapping the starter lightly (sometimes brushes stick), check battery voltage again (low voltage causes slow cranking), and check the main fuse — a blown fuse can prevent starter engagement.</p>
      <h2>Step 8 — Check Spark</h2>
      <p>If the engine cranks but won't fire, spark may be the issue — symptoms are normal cranking, no ignition, no sputter, and no attempt to fire. Possible causes are fouled spark plugs, a failed ignition coil, water intrusion, or damaged plug wires. Removing and inspecting one plug can reveal the issue.</p>
      <h2>Step 9 — If You're on the Water</h2>
      <ol class="pg-list"><li><strong>Drop anchor if possible</strong> — prevents drifting into hazards.</li><li><strong>Turn on your radio</strong> — monitor channel 16.</li><li><strong>Notify someone if needed</strong> — a simple \u201cengine trouble, anchored, troubleshooting\u201d message is enough.</li><li><strong>Keep calm</strong> — most issues are fixable.</li></ol>
      <h2>Step 10 — When to Call for Help</h2>
      <p>Call for assistance if you smell burning, the engine overheated, you struck something, the starter smokes, the battery is completely dead, fuel is leaking, you're drifting into danger, or the weather is worsening. Safety first — engines can be repaired, people cannot.</p>
      <h2>How AftLog Helps</h2>
      <p>AftLog's diagnostic tools help you identify symptoms, follow step-by-step troubleshooting, log engine behavior, track battery health, track fuel-system maintenance, store photos of plugs, filters, and terminals, and know when professional service is needed.</p>
      <h2>Checklist: Engine Won't Start</h2>
      <ul class="pg-list"><li>Check the kill-switch</li><li>Check battery power</li><li>Check the terminals</li><li>Check the gear selector</li><li>Check fuel level</li><li>Check the primer bulb</li><li>Check the tank vent</li><li>Check for flooding</li><li>Check for vapor lock</li><li>Check the spark plugs</li><li>Check the starter motor</li><li>Anchor if drifting</li><li>Call for help if unsafe</li></ul>
      <h2>Summary</h2>
      <p>An engine that won't start is frustrating, but rarely catastrophic. With a calm, systematic approach, you can diagnose most issues quickly and often get back underway without tools. By understanding the common causes — kill-switch, battery, fuel, flooding, vapor lock — you'll be prepared for the moment every boater eventually faces.</p>
      <p>AftLog guides you through the process step-by-step, so you're never alone when your engine refuses to start.</p>""",
                 '<li><a href="overheating-on-the-water.html">Overheating on the water: what to do</a></li><li><a href="spark-plug-intervals.html">Spark plug intervals explained</a></li><li><a href="lower-unit-service.html">Lower-unit service: when and why</a></li>'),
         active="/blog/")

register("blog/overheating-on-the-water", "Outboard Overheating Guide — What to Do, Causes, and How to Prevent Damage", "Learn what to do when your outboard overheats, the warning signs, the most common causes, and how to safely cool the engine and prevent long-term damage.",
         article("overheating-on-the-water", "Overheating on the Water: What to Do",
                 "When your outboard overheats, every second counts. Here's how to respond calmly, diagnose the cause, protect your engine, and get back underway safely.",
                 "Safety", """<img class="blog-hero" src="/images/screen-overheating.png" alt="Cooling-system diagram — the tell-tale and water flow that warn of overheating" loading="lazy">
      <p>An overheating outboard is one of the most urgent problems a boater can face. When the temperature alarm sounds or the tell-tale stream weakens, you have only minutes to act before serious damage occurs. Overheating can warp heads, melt pistons, destroy thermostats, and cause thousands of dollars in repairs.</p>
      <p>The good news is that most overheating events are caused by simple, fixable issues — and if you respond quickly and calmly, you can often resolve the problem on the water and prevent long-term damage. This guide explains what to do when your outboard overheats, the most common causes, how to diagnose the issue, and how to prevent overheating in the future.</p>
      <h2>Recognizing Overheating Symptoms</h2>
      <ol class="pg-list"><li><strong>Temperature alarm</strong> — a loud, continuous beep or tone; the most reliable warning.</li><li><strong>Reduced power / limp mode</strong> — the engine automatically reduces RPM to protect itself.</li><li><strong>Weak or no tell-tale stream</strong> — cooling water flow is reduced or missing.</li><li><strong>Steam from the tell-tale</strong> — indicates hot water and restricted flow.</li><li><strong>Hot engine cover</strong> — if the cowling feels unusually hot, shut down immediately.</li><li><strong>Rough idle or stalling</strong> — overheating can affect combustion.</li></ol>
      <p>If you notice any of these signs, act immediately.</p>
      <h2>Step 1 — Shut Down the Engine Immediately</h2>
      <p>Continuing to run an overheating engine can cause catastrophic damage. Turn off the engine as soon as the alarm sounds — do not try to \u201climp back\u201d unless you are in immediate danger. Drop anchor if drifting to prevent drifting into hazards while you troubleshoot.</p>
      <h2>Step 2 — Check the Tell-Tale Stream</h2>
      <p>The tell-tale is your window into the cooling system. A strong stream means the issue may be internal (thermostat, sensor, blockage). A weak or sputtering stream likely means impeller wear or partial blockage. No stream means cooling water is not reaching the engine — shut down immediately. Steam means water is entering but not circulating properly.</p>
      <h2>Step 3 — Inspect the Water Intake</h2>
      <p>Most overheating events are caused by blocked intakes. Check for weeds, mud, sand, plastic bags, fishing line, or debris. Clear the intake manually — with a stick, knife, or your hand (carefully). Restart briefly to check the tell-tale; if the stream returns strong, the blockage was the cause.</p>
      <h2>Step 4 — Squeeze the Primer Bulb</h2>
      <p>A soft primer bulb can indicate fuel vapor lock or air in the line, which can indirectly cause overheating by reducing engine RPM and water-pump speed. If the bulb is soft, squeeze until firm, check for leaks, and restart while monitoring the tell-tale.</p>
      <h2>Step 5 — Check for Shallow Water or Sand Ingestion</h2>
      <p>Running in shallow water can suck sand into the cooling system — symptoms are a weak tell-tale, sputtering flow, overheating at idle, and debris in the stream. If you suspect sand ingestion: shut down, tilt the engine up, inspect the intakes, and restart briefly to flush. If the tell-tale stays weak, the impeller may be damaged.</p>
      <h2>Step 6 — Check the Impeller</h2>
      <p>The impeller is the heart of the cooling system — if it fails, overheating is inevitable. Symptoms of impeller failure are a weak or no tell-tale, overheating at low RPM, steam, and recent sandy or weedy conditions. If the impeller is the cause, you cannot fix it on the water — return to shore at idle or be towed.</p>
      <h2>Step 7 — Check the Thermostat</h2>
      <p>Thermostats regulate engine temperature. If one sticks closed, overheating occurs quickly. Symptoms are a strong tell-tale, overheating at mid-range RPM, normal idle temperature, and a sudden alarm after acceleration. Thermostat issues require service but are not usually catastrophic if caught early.</p>
      <h2>Step 8 — Check for Internal Blockages</h2>
      <p>Salt, scale, or debris can clog cooling passages. Symptoms are a strong tell-tale, persistent overheating, steam, and inconsistent temperature. This requires professional flushing.</p>
      <h2>Step 9 — Let the Engine Cool</h2>
      <ol class="pg-list"><li>After shutting down, <strong>wait 10–15 minutes</strong> and let the engine cool naturally.</li><li><strong>Do not pour cold water on the engine</strong> — rapid cooling can crack components.</li><li><strong>Restart briefly to test</strong> — if the tell-tale is strong and the alarm stays off, you may continue at reduced speed.</li></ol>
      <h2>Step 10 — Return to Shore Safely</h2>
      <p>If the engine continues to overheat: idle back slowly (low RPM reduces heat load), avoid planing (high RPM increases cooling demand), and if overheating persists at idle, shut down and call for assistance.</p>
      <h2>Common Causes of Overheating</h2>
      <ol class="pg-list"><li>Blocked water intake — weeds, mud, sand, debris</li><li>Worn impeller — most common cause of persistent overheating</li><li>Thermostat failure — stuck closed or clogged</li><li>Sand ingestion — clogs passages and damages the impeller</li><li>High RPM in hot weather — cooling demand exceeds supply</li><li>Low engine RPM due to fuel issues — weak cooling flow</li><li>Internal blockage — salt, scale, corrosion</li><li>Sensor failure — false alarms (rare)</li></ol>
      <h2>How to Prevent Overheating</h2>
      <ol class="pg-list"><li>Replace the impeller every 2–3 years — more often in sandy or shallow water</li><li>Avoid running in very shallow water</li><li>Inspect intakes regularly — especially after beaching or weed beds</li><li>Keep the tell-tale clean — salt can clog the outlet</li><li>Flush the engine after saltwater use</li><li>Replace the thermostat every 3–5 years</li><li>Maintain the fuel system — weak RPM reduces cooling flow</li><li>Log overheating events in AftLog</li></ol>
      <h2>How AftLog Helps</h2>
      <p>AftLog automatically tracks impeller intervals, logs overheating events, stores photos of tell-tale flow, notes symptoms of cooling issues, reminds you when service is due, provides step-by-step diagnostics, helps identify intake blockages, and tracks thermostat replacement intervals.</p>
      <h2>Checklist: Overheating Response</h2>
      <ul class="pg-list"><li>Shut down immediately</li><li>Drop anchor</li><li>Check the tell-tale</li><li>Inspect the water intake</li><li>Clear debris</li><li>Squeeze the primer bulb</li><li>Check for sand ingestion</li><li>Let the engine cool</li><li>Restart briefly</li><li>Idle back if safe</li><li>Call for help if overheating persists</li><li>Log the event in AftLog</li></ul>
      <h2>Summary</h2>
      <p>Overheating is one of the most urgent problems an outboard can face, but most causes are simple and fixable. By responding quickly — shutting down, checking the tell-tale, clearing the intake, and inspecting the impeller — you can often resolve the issue on the water and prevent long-term damage. With proper maintenance and awareness, overheating becomes a rare event.</p>
      <p>AftLog guides you through the process step-by-step, so you're never alone when temperatures rise.</p>""",
                 '<li><a href="engine-wont-start.html">How to handle an engine that won\'t start</a></li><li><a href="impeller-replacement.html">Impeller replacement: symptoms and timing</a></li><li><a href="battery-care-small-boats.html">Battery care for small boats</a></li>'),
         active="/blog/")


register("blog/how-to-build-a-float-plan", "How to Build a Float Plan — The Essential Boating Safety Habit", "Learn how to create a proper float plan, what information to include, who to share it with, and why it's one of the most important safety steps before every trip.",
         article("how-to-build-a-float-plan", "How to Build a Float Plan",
                 "A float plan tells someone where you're going and when you'll be back. If you're overdue, they call for help with the details. Here's how to build one properly — and why it's the single best safety habit on the water.",
                 "Safety", """<img class="blog-hero" src="/images/screen-float-plan.png" alt="AftLog Float Plan screen (placeholder — to be replaced with the Float Plan screenshot)" loading="lazy">
      <p>Before every boating trip — whether it's a short afternoon cruise or a full-day adventure — you should tell someone where you're going and when you'll be back. This simple act is called a float plan, and it's one of the most effective safety habits in boating.</p>
      <p>Search and rescue organizations emphasize it constantly: if you become overdue, your shore contact can call for help with the details — your destination, your crew, your expected return time, and your boat description. That information dramatically speeds up rescue response and can make the difference between a minor inconvenience and a dangerous situation.</p>
      <p>A float plan doesn't need to be complicated. It just needs to be clear, shared, and followed. This guide explains how to build a proper float plan, what information to include, who to share it with, and how AftLog makes the process fast and reliable.</p>
      <h2>Why Float Plans Matter</h2>
      <p>A float plan is a safety net. If something goes wrong — engine trouble, weather changes, injury, fuel issues, or simply losing track of time — your shore contact knows where you went, who was with you, when you planned to return, how to reach you, and when to call for help. This eliminates guesswork. Without a float plan, responders may not know which lake or river you're on, which launch ramp you used, what direction you traveled, how many people are aboard, or whether you changed plans mid-trip. A float plan gives rescuers a starting point — and that saves time.</p>
      <blockquote>Search and rescue asks: tell someone where you are going and when you will be back. If you are overdue, they call for help — with the details.</blockquote>
      <h2>When You Should Create a Float Plan</h2>
      <p>You should create a float plan for every boating trip, but it's especially important when boating alone, with children, in unfamiliar waters, offshore or on large lakes, in poor or changing weather, at night, during shoulder seasons, or in areas with limited cell coverage. Even short trips benefit — emergencies rarely announce themselves ahead of time.</p>
      <h2>What Your Float Plan Should Include</h2>
      <p>A proper float plan includes six essential pieces of information — the same fields shown in your AftLog Float Plan screen:</p>
      <ol class="pg-list"><li><strong>Boat information</strong> — boat name, make/model, color, registration number; helps responders identify your vessel.</li><li><strong>Destination</strong> — be specific, e.g. \u201cnorth shore of Lake of the Prairies, fishing near the rock wall\u201d or \u201crunning the river to Blind River, stopping at the second bend.\u201d</li><li><strong>Departure time</strong> — when you left or plan to leave.</li><li><strong>Expected return time</strong> — defines when your shore contact should start worrying.</li><li><strong>Crew list</strong> — names of everyone aboard.</li><li><strong>Shore contact</strong> — name and phone number of the person who will monitor your return.</li></ol>
      <p><strong>Optional but helpful:</strong> your planned route, backup destinations, fuel level, safety gear aboard, engine type and horsepower, trailer license plate, emergency radio channel, and weather conditions at departure.</p>
      <h2>Who Should Receive Your Float Plan</h2>
      <p>Share your float plan with someone who will notice if you're late, can call for help, knows your general boating habits, and is reachable by phone or text — a spouse or partner, close friend, parent, neighbor, marina staff, or cottage owner. Avoid people who may forget or ignore the responsibility.</p>
      <h2>How to Share Your Float Plan</h2>
      <p>You can share by text message, email, phone call, messaging apps, or by leaving a note at the cottage or marina. The key is that your shore contact receives the plan and understands their role.</p>
      <h2>What Your Shore Contact Should Do</h2>
      <ol class="pg-list"><li>Save your float plan message</li><li>Note your expected return time</li><li>Try calling you if you're overdue</li><li>If unreachable, wait 15–30 minutes</li><li>If still overdue, call for help</li><li>Provide the float plan details to responders</li></ol>
      <h2>How AftLog Helps</h2>
      <p>AftLog's Float Plan screen is designed to make planning simple and fast — fields for boat, destination, depart/return, crew, and contact; an automatic summary card when the plan is armed; a share button for SMS or messaging; and a clear safety explanation. The summary card shows exactly what you entered, so your plan is complete before you share it.</p>
      <h2>Common Mistakes to Avoid</h2>
      <ol class="pg-list"><li><strong>Not sharing the plan</strong> — a float plan only works if someone receives it.</li><li><strong>Being vague about destination</strong> — \u201cgoing fishing\u201d is not a float plan.</li><li><strong>Forgetting to include return time</strong> — your contact won't know when to worry.</li><li><strong>Changing plans without updating</strong> — send a quick update if you explore elsewhere.</li><li><strong>Assuming cell coverage</strong> — remote lakes often have dead zones.</li></ol>
      <h2>Checklist: Building a Float Plan</h2>
      <ul class="pg-list"><li>Boat information entered</li><li>Destination clearly defined</li><li>Departure time set</li><li>Return time set</li><li>Crew listed</li><li>Shore contact chosen</li><li>Plan shared</li><li>Phone charged</li><li>Weather checked</li><li>Safety gear aboard</li></ul>
      <h2>Summary</h2>
      <p>A float plan is one of the simplest and most effective boating safety habits. By telling someone where you're going and when you'll be back, you give search and rescue the information they need to find you quickly if something goes wrong. With AftLog's Float Plan screen, creating and sharing a plan takes less than a minute — and it could save your life. Whether you're heading out for a quiet evening on the lake or a full-day adventure, build a float plan every time. It's the single best safety habit on the water.</p>""",
                 '<li><a href="engine-wont-start.html">How to handle an engine that won\'t start</a></li><li><a href="overheating-on-the-water.html">Overheating on the water: what to do</a></li><li><a href="battery-care-small-boats.html">Battery care for small boats</a></li>'),
         active="/blog/")


register("blog/launch-checklist", "Boat Launch Checklist — Step-by-Step Guide for a Smooth Ramp Experience", "Learn the complete boat launch checklist, including ramp preparation, trailer steps, safety checks, and how AftLog's Launch Mode keeps everything organized.",
         article("launch-checklist", "Launch Checklist: The Complete Guide",
                 "Launching a boat should be smooth, calm, and predictable. Here's the complete launch checklist — from parking-lot prep to backing down the ramp — based on AftLog's built-in Launch Mode.",
                 "Checklists", """<img class="blog-hero" src="/images/screen-launch-mode.png" alt="AftLog Launch Mode checklist (placeholder — to be replaced with the Launch Mode screenshot)" loading="lazy">
      <p>Launching a boat is one of the most common — and most stressful — moments in recreational boating. Ramps can be busy, crowded, and fast-moving. A smooth launch depends on preparation, calmness, and a clear checklist. That's why AftLog includes a dedicated Launch Mode, a big-button, hands-free friendly checklist designed to make every launch predictable and safe.</p>
      <p>This guide walks through the complete launch process, explains each checklist item, and shows how AftLog's Launch Mode helps you stay organized at the ramp.</p>
      <h2>Why a Launch Checklist Matters</h2>
      <p>A launch checklist prevents ramp delays, forgotten drain plugs, trailer damage, boat damage, ramp accidents, engine-starting issues, and safety oversights. Most launch mistakes happen when boaters rush or skip steps. A checklist ensures nothing is forgotten — especially under pressure. AftLog's Launch Mode is built around this idea, with a simple, tap-friendly interface and a clear completion banner: \u201cReady to launch! Drain plug in, straps off, crew set. Take it slow.\u201d</p>
      <h2>Part 1 — Parking-Lot Preparation (Before You Approach the Ramp)</h2>
      <p>The ramp is not the place to prepare your boat. Do everything you can in the parking lot before you get in line. This keeps the ramp flowing smoothly and reduces stress.</p>
      <ol class="pg-list"><li><strong>Drain plug in</strong> — the most important step; a missing drain plug can sink a boat at the dock.</li><li><strong>Trailer straps off</strong> — remove transom straps, rear tie-downs, and any additional restraints; leave the winch strap attached until you're at the water.</li><li><strong>Winch unhooked (at the water only)</strong> — loosen the winch strap in the parking lot, but unhook only when the boat is at the waterline.</li><li><strong>Bow line tied</strong> — so you can guide the boat once it floats off the trailer.</li><li><strong>Fenders on</strong> — on the side you'll tie up after launching.</li><li><strong>Key and kill-switch lanyard in</strong> — key in the ignition, lanyard clipped, before backing down the ramp.</li><li><strong>Battery switch on</strong> — set to ON or 1/BOTH depending on your setup.</li><li><strong>Fuel tank full or noted</strong> — check fuel, and note it in your log so you know your range.</li></ol>
      <h2>Part 2 — Approaching the Ramp</h2>
      <p>Once your boat is fully prepared, get in line. Be patient, don't block the ramp, don't prepare your boat on the ramp, move with purpose but not haste, and communicate clearly with your crew. A calm launch is a safe launch.</p>
      <h2>Part 3 — Backing Down the Ramp</h2>
      <p>AftLog's Launch Mode includes \u201cBack it in slowly\u201d — the most important ramp behavior. Use mirrors, keep steering inputs small, back slowly and steadily, ask a crew member to guide you, avoid sudden movements, and stop when the stern begins to float. The correct trailer depth varies, but generally wheels are partially submerged, bunks just below the waterline, and the bow still supported by the winch post. Too deep and the boat floats early; too shallow and it won't slide off.</p>
      <h2>Part 4 — Launching the Boat</h2>
      <ol class="pg-list"><li><strong>Stop the vehicle</strong> — park and set the parking brake.</li><li><strong>Unhook the winch strap</strong> — once the boat is floating.</li><li><strong>Guide the boat with the bow line</strong> — walk it off the trailer gently.</li><li><strong>Move the boat to the dock</strong> — tie off securely using fenders.</li><li><strong>Start the engine</strong> — check the tell-tale stream, idle stability, battery voltage, and fuel level.</li></ol>
      <h2>Part 5 — Parking the Trailer</h2>
      <ol class="pg-list"><li>Drive the vehicle to the parking area — quickly but safely.</li><li>Park straight and centered — respect the trailer-parking lines.</li><li>Lock your vehicle — keep keys secure.</li><li>Return to the boat — your crew should remain with the boat until you return.</li></ol>
      <h2>How AftLog Helps</h2>
      <p>AftLog's Launch Mode is designed for real-world ramp use: big buttons for hands-free tapping, a simple linear checklist, a clear completion banner, no emojis (brand rule), safety-first ordering, and fast access from the dashboard. It ensures you never forget critical steps like the drain plug, kill-switch, or battery switch.</p>
      <h2>Checklist: Launch Mode (AftLog Preset)</h2>
      <ul class="pg-list"><li>Drain plug in</li><li>Trailer straps off</li><li>Winch unhooked</li><li>Bow line tied</li><li>Fenders on</li><li>Key and kill-switch lanyard in</li><li>Battery switch on</li><li>Fuel tank full or noted</li><li>Back it in slowly</li></ul>
      <h2>Summary</h2>
      <p>Launching a boat doesn't need to be stressful. With proper preparation, clear steps, and AftLog's Launch Mode guiding you, every launch becomes smooth, safe, and predictable. By following the checklist — drain plug, straps, bow line, fenders, kill-switch, battery, fuel, and slow backing — you eliminate the most common ramp mistakes and keep your boating day on track.</p>""",
                 '<li><a href="retrieve-checklist.html">Retrieve checklist: avoid trailer mistakes</a></li><li><a href="how-to-build-a-float-plan.html">How to build a float plan</a></li><li><a href="battery-care-small-boats.html">Battery care for small boats</a></li>'),
         active="/blog/")

register("blog/retrieve-checklist", "Boat Retrieval Checklist — Step-by-Step Guide for a Safe and Smooth Haul-Out", "Learn the complete boat retrieval checklist, including ramp approach, trailer alignment, safety steps, and how AftLog's Retrieve Mode prevents common mistakes.",
         article("retrieve-checklist", "Retrieve Checklist: Avoid Trailer Mistakes",
                 "Retrieving your boat at the ramp is where most trailer mistakes happen. Here's the complete retrieval checklist — based on AftLog's built-in Retrieve Mode — to keep your haul-out smooth and safe.",
                 "Checklists", """<img class="blog-hero" src="/images/screen-retrieve-mode.png" alt="AftLog Retrieve Mode checklist (placeholder — to be replaced with the Retrieve Mode screenshot)" loading="lazy">
      <p>Retrieving your boat at the ramp is often more stressful than launching. You're tired, the ramp is busy, the wind may be pushing you sideways, and you're trying to line up the trailer perfectly while other boaters wait. This is where most trailer mistakes happen — forgotten straps, missing drain plugs, misaligned trailers, and rushed maneuvers.</p>
      <p>AftLog includes a dedicated Retrieve Mode, a big-button checklist designed to make haul-out predictable and safe. This guide walks through the complete retrieval process, explains each checklist item, and shows how AftLog helps you avoid the most common mistakes at the ramp.</p>
      <h2>Why a Retrieval Checklist Matters</h2>
      <p>Retrieving a boat involves more moving parts than launching: trailer alignment, boat positioning, ramp traffic, wind and current, safety gear, engine shutdown, and securing the boat for travel. Missing even one step — like forgetting the winch hook or leaving the drain plug in — can cause damage or safety issues. AftLog's Retrieve Mode is built around preventing these mistakes, with a clear completion banner: \u201cRetrieve complete. Plug out, straps on, winch hooked. Safe to drive.\u201d</p>
      <h2>Part 1 — Preparing the Boat at the Dock</h2>
      <ol class="pg-list"><li><strong>Bow line tied</strong> — you'll need it to guide the boat onto the trailer.</li><li><strong>Fenders on</strong> — keep them on while maneuvering near the dock; remove only after the boat is secured on the trailer.</li><li><strong>Key out</strong> — turn off the engine and remove the key.</li><li><strong>Kill-switch lanyard off</strong> — unclip so it doesn't snag or get lost.</li><li><strong>Battery switch off</strong> — turn off before trailering.</li></ol>
      <h2>Part 2 — Bringing the Trailer Down the Ramp</h2>
      <p>Move with purpose, don't block the ramp, avoid preparing the boat on the ramp, and communicate clearly with your crew. The correct trailer depth generally has wheels partially submerged, bunks just below the waterline, and the winch post above water. Too deep and the boat floats sideways; too shallow and it won't climb the bunks.</p>
      <h2>Part 3 — Guiding the Boat Onto the Trailer</h2>
      <p>Use the bow line to guide the boat straight onto the trailer. Approach slowly, use wind and current to your advantage, keep the bow centered, use short controlled movements, and avoid powering onto the trailer unless permitted. Once the bow reaches the winch post, secure it immediately.</p>
      <h2>Part 4 — Securing the Boat for Travel</h2>
      <p>This is where most retrieval mistakes happen. AftLog's Retrieve Mode includes the essential steps:</p>
      <ol class="pg-list"><li><strong>Winch hooked</strong> — attach the winch hook to the bow eye and crank tight.</li><li><strong>Straps on</strong> — install transom straps, rear tie-downs, and any additional restraints.</li><li><strong>Drain plug out</strong> — so water can drain during travel.</li><li><strong>Fenders off (optional)</strong> — remove once the boat is fully secured.</li><li><strong>Check trailer lights</strong> — verify brake lights and turn signals.</li><li><strong>Check safety chains</strong> — ensure they're crossed and secure.</li><li><strong>Check hitch lock</strong> — confirm the hitch is latched and locked.</li></ol>
      <h2>Part 5 — Driving Up the Ramp</h2>
      <p>AftLog includes \u201cBack it out slowly\u201d, which applies in reverse during retrieval. Drive up slowly and steadily — avoid sudden acceleration, the boat is heavy and wet — watch for pedestrians and other trailers, and move to the parking area quickly to clear the ramp.</p>
      <h2>Part 6 — Final Parking-Lot Checks</h2>
      <ol class="pg-list"><li>Re-check winch strap tension — wet boats can shift slightly</li><li>Re-check transom straps — ensure they're tight</li><li>Verify the drain plug is out — water should be draining</li><li>Inspect trailer tires — look for bulges or low pressure</li><li>Check engine position — tilt the engine up for travel</li><li>Secure loose items — coolers, rods, tackle, and gear</li></ol>
      <h2>How AftLog Helps</h2>
      <p>AftLog's Retrieve Mode is designed for real-world ramp use: big buttons for hands-free tapping, a simple linear checklist, a clear completion banner, no emojis (brand rule), safety-first ordering, and fast access from the dashboard. It ensures you never forget critical steps like the winch hook, drain plug, or transom straps.</p>
      <h2>Checklist: Retrieve Mode (AftLog Preset)</h2>
      <ul class="pg-list"><li>Bow line tied</li><li>Fenders on</li><li>Key out</li><li>Kill-switch lanyard off</li><li>Battery switch off</li><li>Drain plug out</li><li>Straps on</li><li>Winch hooked</li><li>Back it out slowly</li></ul>
      <h2>Summary</h2>
      <p>Retrieving your boat doesn't need to be stressful. With proper preparation, clear steps, and AftLog's Retrieve Mode guiding you, every haul-out becomes smooth, safe, and predictable. By following the checklist — bow line, fenders, key, kill-switch, battery, drain plug, straps, winch, and slow driving — you eliminate the most common ramp mistakes and protect your boat and trailer.</p>""",
                 '<li><a href="launch-checklist.html">Launch checklist: the complete guide</a></li><li><a href="how-to-build-a-float-plan.html">How to build a float plan</a></li><li><a href="engine-wont-start.html">How to handle an engine that won\'t start</a></li>'),
         active="/blog/")


register("blog/used-boat-inspection", "Used-Boat Inspection Checklist — What to Look For Before You Buy", "A complete guide to inspecting a used boat, including hull, engine, electrical, trailer, and safety systems — based on AftLog's built-in inspection checklist.",
         article("used-boat-inspection", "Used-Boat Inspection Checklist",
                 "Buying a used boat can save thousands — but only if you know what to look for. Here's the complete inspection checklist, based on AftLog's built-in Used-Boat template.",
                 "Checklists", """<img class="blog-hero" src="/images/screen-used-boat.png" alt="AftLog Used-Boat Inspection checklist (placeholder — to be replaced with the inspection screenshot)" loading="lazy">
      <p>Buying a used boat can be one of the smartest decisions a boater makes. You can save thousands of dollars, avoid steep depreciation, and often get a well-maintained vessel that performs like new. But used boats vary widely in condition, and a poor inspection can turn a great deal into an expensive mistake.</p>
      <p>AftLog includes a dedicated Used-Boat Inspection checklist — a structured, big-button guide that walks you through every major system: hull, transom, engine, electrical, fuel, bilge, trailer, and safety gear. This article expands on that checklist, explaining exactly what to look for and how to evaluate a boat before you buy.</p>
      <h2>Why Used-Boat Inspections Matter</h2>
      <p>A boat is a collection of systems — hull, transom, engine, lower unit, steering, electrical, fuel, bilge, and trailer. If any is compromised, repairs can be costly. A cracked transom, damaged lower unit, or neglected electrical system can turn a $10,000 boat into a $15,000 project. A structured inspection prevents surprises and gives you confidence in your purchase.</p>
      <h2>Part 1 — Hull Condition</h2>
      <p>Check for cracks and stress marks around the bow, near the transom, around cleats and the windshield, and along the chines (hairline cracks are common; deep cracks are not). Check the gelcoat for oxidation, chalkiness, blistering, or repairs. Inspect the underside for gouges, beaching scars, impact marks, or exposed fiberglass. Tap the hull lightly — dull thuds can indicate moisture (water intrusion).</p>
      <h2>Part 2 — Transom Condition</h2>
      <p>The transom supports the engine — a weak transom is a deal-breaker. Check for cracks around the mounting bolts, flexing when you push the engine, water intrusion, soft spots, and delamination. Test by grabbing the engine and pushing side-to-side; if the transom flexes, walk away.</p>
      <h2>Part 3 — Prop & Lower Unit</h2>
      <p>The lower unit is expensive to repair, so inspect carefully. Check the prop for bent blades, chips, cracks, or fishing line around the shaft (line can cut seals and cause water intrusion). Ask to see the gear oil — healthy oil is clear, amber, and free of metal; milky oil means water intrusion and an expensive repair. Check the skeg for cracks, missing chunks, or welded repairs, and confirm the engine shifts smoothly into forward and reverse.</p>
      <h2>Part 4 — Steering & Controls</h2>
      <p>Check the steering for stiffness, binding, uneven resistance, or hydraulic leaks. Check the controls for smooth throttle, smooth shifting, proper idle, and no grinding noises.</p>
      <h2>Part 5 — Electrical System</h2>
      <p>Electrical issues are common in used boats. Test the lights, horn, bilge pump, livewell pump, GPS/fish finder, radio, gauges, and ignition. Inspect the wiring for condition, corrosion, and loose connections, plus the battery cables.</p>
      <h2>Part 6 — Battery Health</h2>
      <p>Check the battery age, resting voltage (12.6–12.8V), terminal corrosion, and secure mounting. Weak batteries cause hard starting and electrical issues.</p>
      <h2>Part 7 — Fuel System</h2>
      <p>Inspect the fuel lines for cracks, stiffness, or leaks; check the primer bulb, tank vent, and fuel filter (for water or debris), and smell for fuel in the compartments. Ask when the fuel filter was last changed and whether the boat has had ethanol-related issues.</p>
      <h2>Part 8 — Bilge & Pumps</h2>
      <p>Check the bilge pump operation, float switch, livewell pumps, hoses, and clamps, and look for signs of water intrusion. A wet bilge can indicate leaks or hull issues.</p>
      <h2>Part 9 — Trailer Condition</h2>
      <p>The trailer is half the value of the package. Inspect the tires (age, cracks, pressure), bearings (heat after towing), lights, winch strap, bunks and carpet, rust, and frame integrity. Test by spinning each wheel — grinding indicates bad bearings.</p>
      <h2>Part 10 — Safety Gear</h2>
      <p>Check for life jackets, throwables, a fire extinguisher, a whistle/horn, anchor and rope, a first-aid kit, and navigation lights. Missing safety gear adds cost.</p>
      <h2>Part 11 — Engine Start & Water Test</h2>
      <p>If possible, always test the engine on the water. Check cold-start behavior, tell-tale strength, idle stability, acceleration, top-end RPM, vibration, shifting, temperature, and charging voltage. A water test reveals issues a driveway start cannot.</p>
      <h2>Part 12 — Paperwork & History</h2>
      <p>Ask for service records, winterization receipts, ownership documents, the engine serial number, and trailer registration. A well-documented boat is a well-maintained boat.</p>
      <h2>How AftLog Helps</h2>
      <p>AftLog's Used-Boat Inspection checklist provides big-button, tap-friendly items, a structured inspection flow, photo attachments for each item, notes for seller comments, a final summary card, and exportable results — a professional-grade inspection process.</p>
      <h2>Checklist: Used-Boat Inspection (AftLog Preset)</h2>
      <ul class="pg-list"><li>Hull condition</li><li>Transom condition</li><li>Prop &amp; lower unit</li><li>Steering &amp; controls</li><li>Electrical system</li><li>Battery health</li><li>Fuel system</li><li>Bilge &amp; pumps</li><li>Trailer condition</li><li>Safety gear</li></ul>
      <h2>Summary</h2>
      <p>Buying a used boat is a smart move — but only if you inspect it properly. By following AftLog's Used-Boat Inspection checklist, you can evaluate every major system, spot hidden issues, and make a confident, informed purchase. A structured inspection protects your wallet and ensures your new boat is safe, reliable, and ready for the water.</p>""",
                 '<li><a href="launch-checklist.html">Launch checklist: the complete guide</a></li><li><a href="retrieve-checklist.html">Retrieve checklist: avoid trailer mistakes</a></li><li><a href="engine-wont-start.html">How to handle an engine that won\'t start</a></li>'),
         active="/blog/")

register("blog/spring-prep-getting-your-boat-ready", "Spring Boat Prep Guide — De-Winterization, Safety Checks, and First-Launch Readiness", "A complete spring boat-prep guide covering de-winterization, engine checks, fuel system inspection, batteries, safety gear, and first-launch procedures.",
         article("spring-prep-getting-your-boat-ready", "Spring Prep: Getting Your Boat Ready",
                 "Spring is the most important maintenance moment of the year. Here's the complete guide to de-winterizing your boat, inspecting critical systems, and getting ready for a safe first launch.",
                 "Seasonal Prep", """<img class="blog-hero" src="/images/screen-spring-prep.png" alt="AftLog app (placeholder for spring-prep — to be replaced with a spring-prep screenshot)" loading="lazy">
      <p>Spring is the most important maintenance moment of the year for any boat owner. After months of storage, your boat needs a careful, structured de-winterization process to ensure everything is safe, reliable, and ready for the season. A smooth spring prep prevents breakdowns, protects your engine, and sets the tone for a trouble-free summer.</p>
      <p>AftLog includes seasonal reminders, maintenance intervals, and checklists that make spring prep predictable and easy. This guide expands on those tools, giving you a complete, step-by-step process to get your boat ready for the water.</p>
      <h2>Why Spring Prep Matters</h2>
      <p>Winter is hard on boats. Long periods of inactivity, cold temperatures, moisture, and fuel degradation can affect batteries, fuel systems, cooling systems, electrical connections, lower-unit seals, safety gear, and trailer components. Spring prep ensures every system is inspected, tested, and ready for the season.</p>
      <h2>Part 1 — Remove Winter Covers and Inspect the Boat</h2>
      <ol class="pg-list"><li>Remove tarps, shrink-wrap, or covers — check for mold, moisture, rodent damage, torn insulation, or missing hardware.</li><li>Inspect the hull — cracks, blisters, scratches, gelcoat damage, signs of impact.</li><li>Inspect the transom — cracks around mounting bolts, flexing, water intrusion, soft spots.</li><li>Inspect the interior — mildew, water pooling, damaged upholstery, loose hardware.</li></ol>
      <p>Spring is the best time to catch small issues before they become big ones.</p>
      <h2>Part 2 — Battery and Electrical System</h2>
      <p>Winter is tough on batteries — most failures happen during storage. Charge the battery fully with a smart charger, check voltage (healthy resting is 12.6–12.8V), inspect terminals for corrosion, loose clamps, or frayed cables, test the lights, horn, bilge pump, livewell pump, GPS/fish finder, radio, and gauges, and inspect wiring for cracked insulation, rodent damage, or loose connectors. AftLog's battery-care reminders help track battery age and condition.</p>
      <h2>Part 3 — Fuel System</h2>
      <p>Fuel can degrade over winter, especially ethanol blends. Inspect fuel lines for cracks, stiffness, leaks, or soft spots; check the primer bulb (should be firm); inspect the fuel filter for water, debris, or phase-separated ethanol (replace if needed); check the tank vent is clear; top up with fresh gasoline to dilute old fuel; and add stabilizer if the fuel sat all winter.</p>
      <h2>Part 4 — Engine and Lower Unit</h2>
      <ol class="pg-list"><li>Change the engine oil (four-stroke) — if you didn't in the fall.</li><li>Replace the oil filter — always with the oil.</li><li>Change lower-unit gear oil — look for milky oil, metal flakes, or a burnt smell.</li><li>Inspect the prop — bent blades, chips, or fishing line around the shaft.</li><li>Inspect the impeller — replace if it's been 2–3 years.</li><li>Inspect spark plugs — replace if fouled, worn, corroded, or the gap widened.</li><li>Check the tell-tale — start on muffs and verify strong water flow.</li></ol>
      <p>AftLog tracks all these intervals automatically.</p>
      <h2>Part 5 — Cooling System</h2>
      <p>Check the tell-tale stream (strong and steady), inspect the water intakes for sand, weeds, or debris, replace the impeller if due (spring is the best time), and inspect the thermostat (replace every 3–5 years).</p>
      <h2>Part 6 — Steering and Controls</h2>
      <p>Check the steering for stiffness, binding, uneven resistance, or hydraulic leaks; check throttle and shift are smooth and responsive; and lubricate pivot points with marine grease.</p>
      <h2>Part 7 — Bilge and Pumps</h2>
      <p>Test the bilge pump, test the float switch by lifting it manually, inspect hoses for cracks or loose clamps, and check for water — a wet bilge may indicate leaks.</p>
      <h2>Part 8 — Trailer Inspection</h2>
      <p>Your trailer is half the value of your boat. Inspect the tires for cracks, bulges, or low pressure; inspect bearings (spin the wheels — grinding indicates bad bearings); test the lights; inspect the winch strap (replace if frayed); inspect the bunks (carpet and wood); and inspect the safety chains (secure, not rusted).</p>
      <h2>Part 9 — Safety Gear</h2>
      <p>Spring is the perfect time to refresh safety gear — check life jackets, throwables, a fire extinguisher, a whistle/horn, anchor and rope, a first-aid kit, navigation lights, spare fuses, and spare prop hardware. Replace anything worn or expired.</p>
      <h2>Part 10 — First Launch Checklist</h2>
      <ul class="pg-list"><li>Drain plug in</li><li>Battery switch on</li><li>Kill-switch lanyard clipped</li><li>Fenders on</li><li>Bow line tied</li><li>Fuel level checked</li><li>Engine started on muffs</li><li>Tell-tale verified</li><li>Trailer straps off</li><li>Winch strap loosened</li></ul>
      <p>AftLog's Launch Mode covers all of these steps.</p>
      <h2>How AftLog Helps</h2>
      <p>AftLog provides seasonal reminders, maintenance intervals, launch and retrieve checklists, battery-care guidance, engine-service tracking, photo logs, and safety-gear checklists — so spring prep becomes structured, predictable, and stress-free.</p>
      <h2>Summary</h2>
      <p>Spring prep is the foundation of a safe and reliable boating season. By inspecting your hull, engine, fuel system, electrical system, trailer, and safety gear, you prevent breakdowns and protect your investment. With AftLog's seasonal reminders and built-in checklists, de-winterization becomes simple, organized, and confidence-building. A well-prepared boat makes every spring launch feel like a fresh start.</p>""",
                 '<li><a href="battery-care-small-boats.html">Battery care for small boats</a></li><li><a href="impeller-replacement.html">Impeller replacement: symptoms and timing</a></li><li><a href="launch-checklist.html">Launch checklist: the complete guide</a></li>'),
         active="/blog/")


register("blog/fall-haul-out-checklist", "Fall Boat Haul-Out Checklist — Winterization, Engine Care, and Storage Prep", "A complete fall haul-out guide covering winterization, engine protection, fuel stabilization, lower-unit care, battery storage, and trailer preparation.",
         article("fall-haul-out-checklist", "Fall Haul-Out Checklist",
                 "Fall haul-out is the most important maintenance moment of the year. Here's the complete checklist for winterizing your boat, protecting your engine, and storing everything safely until spring.",
                 "Seasonal Prep", """<img class="blog-hero" src="/images/screen-fall-haul-out.png" alt="AftLog app (placeholder for fall haul-out — to be replaced with a haul-out/winterization photo)" loading="lazy">
      <p>Fall haul-out is the single most important maintenance moment of the year. Winter is hard on boats — freezing temperatures, moisture, fuel degradation, and long periods of inactivity can damage engines, batteries, and hull components. A proper haul-out protects your investment and ensures your boat is ready for a trouble-free spring.</p>
      <p>AftLog includes seasonal reminders, maintenance intervals, and structured checklists that make fall haul-out predictable and stress-free. This guide expands on those tools, giving you a complete, step-by-step process to prepare your boat for winter.</p>
      <h2>Why Fall Haul-Out Matters</h2>
      <p>Winter can damage engines, lower units, cooling systems, batteries, fuel systems, electrical connections, the hull and transom, and trailer components. A structured haul-out prevents freeze damage, corrosion, fuel separation, battery failure, lower-unit water intrusion, mold and mildew, and rodent damage. Fall is your chance to reset the boat, protect every system, and start next season fresh.</p>
      <h2>Part 1 — Final Fall Trip and Ramp Retrieval</h2>
      <p>Before winterization, take a final trip to burn off old fuel, listen for unusual noises, check tell-tale strength, verify charging voltage, and note any issues for spring service. Then retrieve using AftLog's Retrieve Mode — bow line tied, fenders on, key out, kill-switch lanyard off, battery switch off, drain plug out, straps on, winch hooked, back it out slowly.</p>
      <h2>Part 2 — Drain Water and Moisture</h2>
      <ol class="pg-list"><li><strong>Remove the drain plug</strong> — let the hull drain completely.</li><li><strong>Tilt the engine down</strong> — drains the cooling passages, lower unit, and exhaust housing.</li><li><strong>Drain livewells and bait tanks</strong> — remove plugs and let them dry.</li><li><strong>Drain the bilge</strong> — use the bilge pump if needed.</li><li><strong>Remove wet gear</strong> — coolers, ropes, anchors, and life jackets should dry before storage.</li></ol>
      <h2>Part 3 — Engine Winterization</h2>
      <ol class="pg-list"><li><strong>Stabilize the fuel</strong> — add marine fuel stabilizer and run for 5–10 minutes to circulate it.</li><li><strong>Fog the engine</strong> (two-stroke and some four-stroke) — fogging oil protects internal components from corrosion.</li><li><strong>Change engine oil</strong> (four-stroke) — fall is best: contaminants removed, fresh oil sits all winter, moisture minimized.</li><li><strong>Replace the oil filter</strong> — always with the oil.</li><li><strong>Change lower-unit gear oil</strong> — look for milky oil, metal flakes, or a burnt smell; changing in fall prevents freeze damage.</li><li><strong>Inspect the prop</strong> — bent blades, chips, or fishing line around the shaft (remove line — it cuts seals).</li><li><strong>Grease all fittings</strong> — steering pivot, tilt tube, prop shaft, throttle linkage.</li><li><strong>Check the thermostat</strong> — replace every 3–5 years.</li><li><strong>Inspect the impeller</strong> — replace if it's been 2–3 years.</li></ol>
      <h2>Part 4 — Fuel System Protection</h2>
      <p>Add fuel stabilizer (prevents ethanol separation), top up the tank (a full tank reduces condensation), inspect fuel lines for cracks or stiffness, replace the fuel filter (fall is the best time), and check the primer bulb (should be firm).</p>
      <h2>Part 5 — Battery Storage</h2>
      <p>Most battery failures happen during winter. Fully charge the battery with a smart charger, disconnect the terminals to prevent parasitic drain, remove the battery and store indoors if possible, use a smart maintainer, and check voltage monthly (healthy resting is 12.6–12.8V).</p>
      <h2>Part 6 — Electrical System</h2>
      <p>Inspect wiring for cracked insulation, rodent damage, or corrosion; test electronics (GPS, fish finder, radio, lights); and remove sensitive electronics to store indoors.</p>
      <h2>Part 7 — Interior and Hull Protection</h2>
      <p>Clean the interior to remove dirt, moisture, and debris; remove food and scented items to prevent rodent attraction; inspect the hull for cracks or damage; wash and wax the hull (wax protects gelcoat during winter); and dry all compartments to prevent mold.</p>
      <h2>Part 8 — Trailer Inspection</h2>
      <p>Inspect the tires for cracks and proper pressure, grease the bearings, inspect the lights (wiring and bulbs), inspect the winch strap (replace if frayed), inspect the bunks (carpet and wood), and inspect the safety chains to ensure they're secure.</p>
      <h2>Part 9 — Covering and Storage</h2>
      <ol class="pg-list"><li>Use a proper boat cover — avoid cheap tarps that trap moisture.</li><li>Support the cover — prevent pooling.</li><li>Ventilate — moisture causes mold.</li><li>Store indoors if possible — best protection.</li><li>If storing outdoors — use shrink-wrap or a high-quality cover.</li></ol>
      <h2>How AftLog Helps</h2>
      <p>AftLog provides seasonal reminders, maintenance intervals, haul-out checklists, battery-care guidance, engine-service tracking, photo logs, and safety-gear checklists — so fall haul-out becomes structured, predictable, and stress-free.</p>
      <h2>Summary</h2>
      <p>Fall haul-out is the foundation of a safe, reliable spring launch. By winterizing your engine, stabilizing fuel, draining water, protecting your battery, inspecting your trailer, and covering your boat properly, you prevent freeze damage, corrosion, and costly repairs. A well-prepared boat sleeps safely all winter — and wakes up ready for spring.</p>""",
                 '<li><a href="fuel-storage-best-practices.html">Fuel storage best practices</a></li><li><a href="spring-prep-getting-your-boat-ready.html">Spring prep: getting your boat ready</a></li><li><a href="winterize.html">How to winterize your boat</a></li>'),
         active="/blog/")

register("blog/fuel-storage-best-practices", "Boat Fuel Storage Best Practices — Prevent Ethanol Damage, Water Contamination, and Winter Degradation", "Learn how to store boat fuel safely, prevent ethanol separation, avoid water contamination, protect your engine over winter, and ensure reliable spring starts.",
         article("fuel-storage-best-practices", "Fuel Storage Best Practices",
                 "Fuel is the lifeblood of your engine — but it degrades quickly when stored. Here's how to store boat fuel properly, prevent ethanol problems, and keep your engine safe through winter.",
                 "Seasonal Prep", """<img class="blog-hero" src="/images/screen-fuel-storage.png" alt="Fuel system diagram — tank, lines, and stabilizer for safe fuel storage" loading="lazy">
      <p>Fuel is the lifeblood of your outboard engine. But gasoline — especially ethanol-blended fuel — degrades quickly when stored. Over time, fuel absorbs moisture, separates, forms varnish, and loses volatility. Poor fuel storage is one of the most common causes of hard starting, rough idle, stalling, and springtime engine trouble.</p>
      <p>Whether you're storing your boat for winter, keeping fuel in portable tanks, or managing fuel for a full season, proper storage protects your engine and prevents expensive repairs. This guide explains how fuel degrades, how to store it safely, how to prevent ethanol problems, and how AftLog helps you track fuel health.</p>
      <h2>Why Fuel Storage Matters</h2>
      <p>Gasoline begins degrading within 30–60 days, especially ethanol blends (E10). As fuel ages it suffers <strong>moisture absorption</strong> (ethanol attracts water, causing phase separation, corrosion, poor combustion, stalling, and injector damage), <strong>phase separation</strong> (a water-ethanol layer at the tank bottom and a low-octane layer above — engines draw from the bottom, the worst part), <strong>varnish formation</strong> (sticky deposits that clog carburetors, injectors, fuel pumps, and filters), <strong>loss of volatility</strong> (hard starting, rough idle, misfires), and <strong>corrosion</strong> in tanks, lines, fittings, and carburetor bowls.</p>
      <h2>Part 1 — Choosing the Right Fuel</h2>
      <p>Most boaters use <strong>E10</strong> because it's widely available, but it requires careful storage. <strong>Non-ethanol marine fuel</strong>, when available, is ideal for long-term storage, small outboards, carbureted engines, and seasonal boats. On octane: use what your engine manufacturer recommends — freshness matters more than octane.</p>
      <h2>Part 2 — Fuel Stabilizer: Your Best Defense</h2>
      <p>Stabilizer is essential for any fuel stored longer than 30–60 days. It slows oxidation, prevents phase separation, reduces moisture absorption, protects injectors and carburetors, and keeps fuel fresh for 6–12 months. Add it before winter storage, before storing portable tanks, before long periods of inactivity, or whenever fuel may sit more than 60 days. Add stabilizer, fill with fresh fuel, then run the engine 5–10 minutes so treated fuel reaches the carburetor, injectors, and fuel pump.</p>
      <h2>Part 3 — Storing Fuel in Boat Tanks</h2>
      <ol class="pg-list"><li>Fill the tank 90–95% full — reduces condensation; leave a small air gap for expansion.</li><li>Add stabilizer — treat the entire tank.</li><li>Run the engine — circulate stabilized fuel.</li><li>Close the tank vent (if safe) — check manufacturer guidance.</li><li>Inspect the tank — corrosion, leaks, loose fittings, cracked hoses.</li><li>Store the boat level — prevents water pooling in the tank.</li></ol>
      <h2>Part 4 — Storing Fuel in Portable Tanks</h2>
      <p>Portable tanks need special care: empty or fill them entirely (never half-full — half-full promotes condensation), store indoors to avoid temperature swings, use stabilizer on all portable fuel, inspect the cap seal (a damaged seal lets moisture in), check the primer bulb (replace if cracked or soft), and safely dispose of fuel older than 6–12 months.</p>
      <h2>Part 5 — Fuel Lines and Filters</h2>
      <p>Fuel lines degrade over time, especially with ethanol. Inspect for cracks, stiffness, leaks, soft spots, or discoloration. Replace fuel filters annually (fall is best), check the primer bulb (firm when squeezed), and inspect the tank vent (clear and functioning).</p>
      <h2>Part 6 — Carbureted Engines vs. EFI Engines</h2>
      <p>Carbureted engines are more sensitive to old fuel — varnish forms in jets, bowls, and floats, so drain carburetors before long-term storage. EFI engines are more tolerant, but injectors can still clog, so stabilizer is essential.</p>
      <h2>Part 7 — Winter Storage: The Complete Process</h2>
      <ol class="pg-list"><li>Add stabilizer — treat the entire tank.</li><li>Fill the tank 90–95% — minimize condensation.</li><li>Run the engine — circulate stabilized fuel.</li><li>Replace the fuel filter — remove contaminants.</li><li>Inspect fuel lines — replace if cracked.</li><li>Store the boat level — prevent water pooling.</li><li>Check portable tanks — treat or empty them.</li></ol>
      <h2>Part 8 — Spring Fuel Preparation</h2>
      <ol class="pg-list"><li>Inspect fuel — look for water or cloudiness.</li><li>Check the filter — replace if needed.</li><li>Check the primer bulb — should be firm.</li><li>Add fresh fuel — dilute any remaining winter fuel.</li><li>Start the engine on muffs — verify smooth idle and strong tell-tale.</li></ol>
      <h2>How AftLog Helps</h2>
      <p>AftLog provides seasonal reminders, fuel-system maintenance intervals, checklists for fall haul-out and spring prep, photo logs of fuel filters and lines, notes for fuel type and stabilizer use, and alerts for symptoms of fuel degradation.</p>
      <h2>Summary</h2>
      <p>Fuel storage is one of the most important — and most overlooked — parts of boat maintenance. By using stabilizer, filling tanks properly, inspecting fuel lines, replacing filters, and storing fuel correctly, you prevent ethanol problems, water contamination, and springtime engine trouble. Fresh fuel means a fresh start every season.</p>""",
                 '<li><a href="fall-haul-out-checklist.html">Fall haul-out checklist</a></li><li><a href="spring-prep-getting-your-boat-ready.html">Spring prep: getting your boat ready</a></li><li><a href="winterize.html">How to winterize your boat</a></li>'),
         active="/blog/")


BLOG_ARTICLES = [
    ("How to winterize your boat", "A step-by-step winterization plan — fuel, engine, water systems, battery, and cover.", "Maintenance", "/blog/winterize.html", "/images/screen-app-dashboard.png"),
    ("Boat maintenance checklist for beginners", "The 12 checks every new owner should know before launching.", "Maintenance", "/blog/beginner-checklist.html", "/images/screen-app-checklists.png"),
    ("How often to change outboard oil", "Intervals, why they matter, and how AftLog tracks them for you.", "Maintenance", "/blog/outboard-oil.html", "/images/screen-smp-plan.png"),
    ("Lower-unit service: when and why", "Gear oil, seals, and the simple checks that keep your lower unit alive.", "Maintenance", "/blog/lower-unit-service.html", "/images/screen-lower-unit.png"),
    ("Spark plug intervals explained", "Why 200 hours is the rule, and the symptoms of worn plugs.", "Maintenance", "/blog/spark-plug-intervals.html", "/images/screen-spark-plugs.png"),
    ("Impeller replacement: symptoms and timing", "Weak tell-tale? It's usually the impeller. Here's when to change it.", "Maintenance", "/blog/impeller-replacement.html", "/images/screen-impeller.png"),
    ("Battery care for small boats", "Charge, store, and check — batteries die in the off-season, not on the water.", "Maintenance", "/blog/battery-care-small-boats.html", "/images/screen-battery-care.png"),
    ("Boat safety equipment list", "What to carry on board — and how to check it before every launch.", "Safety", "/blog/safety-equipment.html", "/images/screen-portal-health.png"),
    ("How to handle an engine that won't start", "A calm, ordered checklist for the most frustrating moment in boating.", "Safety", "/blog/engine-wont-start.html", "/images/screen-engine-wont-start.png"),
    ("Overheating on the water: what to do", "Recognize it early and know when to stop — before it becomes a big repair.", "Safety", "/blog/overheating-on-the-water.html", "/images/screen-overheating.png"),
    ("How to build a float plan", "Tell someone where you're going — it takes two minutes and saves lives.", "Safety", "/blog/how-to-build-a-float-plan.html", "/images/screen-float-plan.png"),
    ("Launch checklist: the complete guide", "Plug, pump, battery, gear — everything checked before you leave the ramp.", "Checklists", "/blog/launch-checklist.html", "/images/screen-launch-mode.png"),
    ("Retrieve checklist: avoid trailer mistakes", "The five-minute routine that prevents ramp-day damage.", "Checklists", "/blog/retrieve-checklist.html", "/images/screen-retrieve-mode.png"),
    ("Used-boat inspection checklist", "The 13-section walkthrough that helps you buy with confidence.", "Checklists", "/blog/used-boat-inspection.html", "/images/screen-used-boat.png"),
    ("Spring prep: getting your boat ready", "De-winterize, inspect, and launch right the first time.", "Seasonal prep", "/blog/spring-prep-getting-your-boat-ready.html", "/images/screen-spring-prep.png"),
    ("Fall haul-out checklist", "The off-season routine that makes spring easy.", "Seasonal prep", "/blog/fall-haul-out-checklist.html", "/images/screen-fall-haul-out.png"),
    ("Fuel storage best practices", "Stabilizer, full tanks, and why ethanol needs a plan.", "Seasonal prep", "/blog/fuel-storage-best-practices.html", "/images/screen-fuel-storage.png"),
    ("How AftLog's AI assistant works", "Diagnostics, manual extraction, photo analysis, and predictive alerts.", "AI & Portal", "/ai.html", "/images/screen-vea-result.png"),
    ("Understanding your Boat Health Score", "What the 0-100 score means and how to raise it.", "AI & Portal", "/portal.html", "/images/screen-portal-year.png"),
    ("Year in Review: making sense of your season", "Trips, hours, fuel, and milestones — your season at a glance.", "AI & Portal", "/portal.html", "/images/screen-portal-year.png"),
]


def _blog_card(t, b, cat, href, thumb, featured=False):
    inner = (f'<img class="pg-thumb" src="{thumb}" alt="" loading="lazy">'
             if thumb else '<div class="pg-thumb pg-thumb-soon"><span>Coming soon</span></div>')
    inner += f'<span class="pg-cat-tag">{cat}</span><h3>{t}</h3><p>{b}</p>'
    cls = "pg-blog-card" + (" pg-featured-card" if featured else "")
    if href:
        return f'<a class="{cls}" data-cat="{cat.lower()}" href="{href}">{inner}</a>'
    return f'<div class="{cls} pg-blog-card-soon" data-cat="{cat.lower()}">{inner}</div>'


def blog_hub():
    feat_names = ("How to winterize your boat",
                  "Boat maintenance checklist for beginners",
                  "How AftLog's AI assistant works")
    featured = "".join(_blog_card(*a, featured=True) for a in BLOG_ARTICLES if a[0] in feat_names)
    cats = ["All", "Maintenance", "Safety", "Checklists", "Seasonal prep", "AI & Portal"]
    bar = "".join(
        f'<button type="button" class="pg-cat-btn{" on" if c == "All" else ""}" data-cat="{c.lower()}">{c}</button>'
        for c in cats)
    grid = "".join(_blog_card(*a) for a in BLOG_ARTICLES)
    filter_js = """<script>
  (function () {
    var btns = document.querySelectorAll('.pg-cat-btn');
    var cards = document.querySelectorAll('.pg-blog-card');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        var cat = b.dataset.cat;
        cards.forEach(function (c) {
          c.style.display = (cat === 'all' || c.dataset.cat === cat) ? '' : 'none';
        });
      });
    });
  })();
</script>"""
    return (
        hero("Latest Articles",
             "Practical, plain-language articles for boat owners: maintenance, safety, checklists, seasonal prep, and the AI Portal.")
        + section("Featured", f'<div class="pg-featured-row">{featured}</div>')
        + f'<section class="section section--alt pg-cat-section"><div class="container">'
        + f'<div class="pg-cat-bar" role="group" aria-label="Filter articles by category">{bar}</div>'
        + f'<div class="pg-article-grid">{grid}</div></div></section>'
        + filter_js
        + section("Need help or have questions?",
                  '<div class="pg-actions"><a class="btn btn-primary" href="/support.html">Support</a>'
                  '<a class="btn btn-secondary" href="/faq.html">FAQ</a></div>')
    )


BLOG_INDEX = blog_hub()
register("blog/index", "AftLog Blog — Boat Maintenance Tips", "Articles for boat owners: maintenance, safety, checklists, and seasonal prep.",
         BLOG_INDEX, active="/blog/")

register("blog/winterize", "How to winterize your boat", "A step-by-step winterization plan: fuel, engine, water systems, battery, and cover.",
         article("winterize", "How to winterize your boat",
                 "A step-by-step plan that protects your engine, fuel system, and battery through the off-season.",
                 "Seasonal prep", """<p>Winterizing is the difference between a spring that starts on the first turn and a spring full of repairs. Do it before the first hard frost.</p>
      <ol class="pg-list">
        <li><strong>Stabilize the fuel.</strong> Add fuel stabilizer and run the engine long enough to work it through the system.</li>
        <li><strong>Fog the engine.</strong> Fogging oil protects cylinders from corrosion while it sits.</li>
        <li><strong>Drain water systems.</strong> Engine block, livewells, ballast, and fresh water — standing water freezes and cracks.</li>
        <li><strong>Change lower-unit oil.</strong> Old oil can hold water; fresh oil protects the gears all winter.</li>
        <li><strong>Remove the battery.</strong> Store it inside on a maintainer. A battery left to discharge all winter is often dead by spring.</li>
        <li><strong>Protect the outside.</strong> Cover, shrink-wrap, or indoor storage — sun and snow both damage gelcoat and vinyl.</li>
      </ol>
      <p>Run the <a href="/tools/winterization-planner.html">Winterization Planner</a> for your region's timing, then work the <a href="/checklists/winterization.html">winterization checklist</a> step by step.</p>""",
                 '<li><a href="beginner-checklist.html">Boat maintenance checklist for beginners</a></li><li><a href="outboard-oil.html">How often to change outboard oil</a></li><li><a href="safety-equipment.html">Boat safety equipment list</a></li>'),
         active="/blog/")

register("blog/beginner-checklist", "Boat maintenance checklist for beginners", "The 12 checks every new boat owner should know before launching.",
         article("beginner-checklist", "Boat maintenance checklist for beginners",
                 "A simple pre-launch routine that catches most problems before they're problems.",
                 "Checklists", """<ol class="pg-list">
        <li><strong>Kill switch / lanyard</strong> — present and working.</li>
        <li><strong>Battery</strong> — 12.6V+ at rest, terminals clean and tight.</li>
        <li><strong>Fuel</strong> — enough for the trip plus reserve; primer bulb firm.</li>
        <li><strong>Engine oil</strong> — level and age. When did you last change it?</li>
        <li><strong>Cooling</strong> — tell-tale stream strong within 30 seconds of start.</li>
        <li><strong>Steering</strong> — free and responsive, no stiffness.</li>
        <li><strong>Bilge</strong> — dry at the start; bilge pump works.</li>
        <li><strong>Drain plugs</strong> — in and tight.</li>
        <li><strong>Safety gear</strong> — PFDs, throwable, fire extinguisher, whistle/horn.</li>
        <li><strong>Lights</strong> — nav lights and anchor light (if running late).</li>
        <li><strong>Trailer</strong> — tires, lights, coupler, straps, breakaway cable.</li>
        <li><strong>Plan</strong> — tell someone where you're going and when you'll be back.</li>
      </ol>
      <p>AftLog turns this into an interactive launch checklist that teaches as you go — <a href="/features.html">see the features</a>.</p>""",
                 '<li><a href="safety-equipment.html">Boat safety equipment list</a></li><li><a href="winterize.html">How to winterize your boat</a></li>'),
         active="/blog/")

register("blog/outboard-oil", "How often to change outboard oil", "Intervals, why they matter, and how AftLog tracks them for you.",
         article("outboard-oil", "How often to change outboard oil",
                 "The 100-hour rule, the annual rule, and why both matter for a long engine life.",
                 "Maintenance", """<p>Most four-stroke outboards call for an oil and filter change every <strong>100 hours or once a year</strong>, whichever comes first. Two-strokes use injector oil and have no sump to drain — but the principle is the same: oil is the cheapest thing you'll ever replace on your engine.</p>
      <p>Short trips and idling are harder on oil than long cruises, so if you mostly putter around the dock, stick to the yearly side of the rule. Old oil loses its additives — that's what protects against wear and corrosion in a marine environment.</p>
      <p>Lower-unit oil is a separate job: typically every <strong>100 hours or annually</strong>, and worth checking right after a suspected impact. Milky or metallic oil means water or wear — get it looked at.</p>
      <p>AftLog tracks oil changes and lower-unit services per boat and reminds you when the next one is due — <a href="/features.html">find out how</a>.</p>""",
                 '<li><a href="winterize.html">How to winterize your boat</a></li><li><a href="beginner-checklist.html">Boat maintenance checklist for beginners</a></li>'),
         active="/blog/")

register("blog/safety-equipment", "Boat safety equipment list", "What to carry on board — and how to check it before every launch.",
         article("safety-equipment", "Boat safety equipment list",
                 "The legal minimums, the smart extras, and a pre-launch check routine.",
                 "Safety", """<ul class="pg-list">
        <li><strong>PFDs</strong> — one properly fitting lifejacket per person, plus a throwable device. Check straps and buoyancy yearly.</li>
        <li><strong>Fire extinguisher</strong> — appropriate class for your boat, charged, accessible, in date.</li>
        <li><strong>Sound signal</strong> — whistle or horn; a compressed-air horn with a spare.</li>
        <li><strong>Visual signals</strong> — flares or an approved electronic equivalent (check expiry dates).</li>
        <li><strong>First aid kit</strong> — including seasickness meds, sunscreen, and a thermal blanket.</li>
        <li><strong>VHF radio or phone in a waterproof case</strong> — with a charged backup battery.</li>
        <li><strong>Tools &amp; spares</strong> — kill switch lanyard, spare plugs, fuses, tow line, basic toolkit.</li>
        <li><strong>Manual bailing / bilge pump</strong> — in case the electric one fails.</li>
      </ul>
      <p>Regulations vary by province/state and boat size — check your local rules. AftLog's compliance tool and launch checklists keep it routine, not a chore: <a href="/features.html">see how</a>.</p>""",
                 '<li><a href="beginner-checklist.html">Boat maintenance checklist for beginners</a></li><li><a href="winterize.html">How to winterize your boat</a></li>'),
         active="/blog/")

# /privacy and /terms (brief factual placeholders — Louis to review)
register("privacy", "AftLog Privacy Policy", "How AftLog handles your data: on-device by default, no selling, no ads.",
         hero("Privacy", "Your boat data stays yours.")
         + section("What we collect and where it lives", """<ul class="pg-list">
      <li><strong>On-device by default.</strong> Your boats, logs, services, and checklists live in the app's local database. No account is required to use the app.</li>
      <li><strong>No selling.</strong> We never sell personal data and we don't run ads.</li>
      <li><strong>Optional portal sync.</strong> If you link to the AftLog Portal, only what you send is stored on the server, tied to your portal account.</li>
      <li><strong>AI questions.</strong> Questions you ask the AI assistant are processed by the AftLog server to produce an answer; the app and website never hold AI keys.</li>
      <li><strong>Waitlist email.</strong> Used only to contact you about AftLog availability.</li>
      <li><strong>License.</strong> AftLog Pro is a one-time lifetime purchase ($29, no subscription) — no recurring billing data is collected.</li>
    </ul>
    <h3>Your rights</h3>
    <ul class="pg-list">
      <li>Export your data any time (app: More → Backup / CSV export).</li>
      <li>Delete your data by removing the app or contacting us — we'll remove anything stored server-side on request.</li>
      <li>Contact: <a href="mailto:aftlog@yahoo.com?subject=AftLog%20privacy">aftlog@yahoo.com</a>.</li>
    </ul>
    <p class="pg-muted">Questions? <a href="/support.html">Contact us</a>.</p>"""))
register("terms", "AftLog Terms of Use", "The short version: use AftLog safely, don't abuse it, and remember it's a tool — not a replacement for a marine professional.",
         hero("Terms of Use", "Plain-language terms for using AftLog.")
         + section("The essentials", """<ul class="pg-list">
      <li>AftLog is a record-keeping and guidance tool. It is not a certified inspection, survey, or substitute for a qualified marine mechanic.</li>
      <li>Always follow your engine and boat manufacturer's manuals and local regulations over any app guidance.</li>
      <li>Free tier: one boat. AftLog Pro: one-time $29 lifetime license, non-transferable unless we say otherwise.</li>
      <li>Don't misuse the service, resell access, or attempt to breach the servers.</li>
      <li>We may update these terms; continued use means you accept the updates.</li>
    </ul>
    <p class="pg-muted">Questions? <a href="/support.html">Contact us</a>.</p>""")
         + section("Your rights, refunds &amp; termination", """<ul class="pg-list">
      <li><strong>Refunds.</strong> AftLog Pro comes with a 30-day money-back guarantee. Email <a href="mailto:aftlog@yahoo.com?subject=AftLog%20refund">aftlog@yahoo.com</a> within 30 days of purchase for a full refund.</li>
      <li><strong>Your data.</strong> Your boat data is yours. You can export it at any time (More → Backup / CSV export) and delete it by removing the app or contacting support.</li>
      <li><strong>Termination.</strong> We may suspend or terminate access for abuse (reselling licenses, attempting to breach servers, illegal use). You can stop using AftLog at any time — no notice needed.</li>
      <li><strong>Warranty.</strong> The app is provided as-is. We keep it reliable, but we don't guarantee the app or the AI assistant will be error-free, and we're not liable for damage arising from how you use it.</li>
      <li><strong>Contact.</strong> Questions about these terms: <a href="mailto:aftlog@yahoo.com?subject=AftLog%20terms">aftlog@yahoo.com</a>.</li>
    </ul>"""))


register(
    "tools/winterization-planner",
    "Winterization Planner — Freeze & Ice-Out Guide",
    "Region-aware winterization timing from the AftLog app: freeze-up and ice-out windows, why it matters, and the guided checklist.",
    hero("Winterization Planner",
         "Freeze-up and ice-out timing for your region — and a guided checklist to protect your engine through the off-season.")
    + '<section class="section section--light"><div class="container">'
    + '<label for="wz-region" class="pg-hint-label">Choose your region</label>'
    + '<select id="wz-region" class="pg-select"><option value="">Select a region…</option>'
    + "".join('<option value="%s">%s</option>' % (n,n) for n,f,i in [
        ("Southern Manitoba / Winkler","late October","mid-April"),
        ("Winnipeg / Lake Winnipeg","mid-November","mid-May"),
        ("Northern Manitoba / The Pas","late October","late May"),
        ("Ontario south","mid-December","mid-April"),
        ("Ontario north","mid-November","early May"),
        ("US northern states","November","April"),
        ("US southern states","mild","year-round")])
    + '</select>'
    + '<div class="wz-window" id="wz-window"><span class="wz-fill">Select a region to see your freeze-up and ice-out windows.</span></div>'
    + """<script>
        (function () {
          var REGIONS = [
            {name:'Southern Manitoba / Winkler', freezeUp:'late October', iceOut:'mid-April'},
            {name:'Winnipeg / Lake Winnipeg', freezeUp:'mid-November', iceOut:'mid-May'},
            {name:'Northern Manitoba / The Pas', freezeUp:'late October', iceOut:'late May'},
            {name:'Ontario south', freezeUp:'mid-December', iceOut:'mid-April'},
            {name:'Ontario north', freezeUp:'mid-November', iceOut:'early May'},
            {name:'US northern states', freezeUp:'November', iceOut:'April'},
            {name:'US southern states', freezeUp:'mild', iceOut:'year-round'}
          ];
          var sel = document.getElementById('wz-region');
          var out = document.getElementById('wz-window');
          sel.addEventListener('change', function () {
            var r = REGIONS.find(function (x) { return x.name === sel.value; });
            if (!r) { out.innerHTML = '<span class="wz-fill">Select a region to see your freeze-up and ice-out windows.</span>'; return; }
            out.innerHTML = '<strong>Freeze-up:</strong> ' + r.freezeUp + ' &nbsp;·&nbsp; <strong>Ice-out:</strong> ' + r.iceOut;
          });
        })();
      </script>"""
    + '</div></section>'
    + section("Why this matters", """<p>When water freezes it expands. Left in the engine, block, or manifolds over the off-season, it can crack cast iron and aluminum — the most expensive repair a boat owner faces. Winterizing clears the water and protects the fuel system, battery, and lower unit so the engine starts clean in spring.</p>
      <p>Winterize after your region's freeze-up window, before the first hard frost. Commission in spring after ice-out.</p>""")
    + section("Ready to winterize?", """<p>Run the guided winterization checklist — every step you complete saves a photo-worthy step for spring.</p>
      <p><a class="btn btn-primary" href="/checklists/winterization.html">Start the Winterization Checklist</a></p>
      <p class="pg-muted">In the app: More → Tools → Winterization Planner.</p>""")
    + section("Forgot to winterize?", """<p>If it already froze with water in the engine: do <strong>not</strong> crank it. Drain everything, check the block and manifolds for cracks, and call a mechanic if in doubt. Cracked blocks are expensive; frozen-then-thawed ones leak.</p>"""),
)


register(
    "checklists/winterization",
    "Winterization Checklist",
    "The step-by-step before-first-frost checklist — fuel, engine, water systems, battery, and cover.",
    hero("Winterization Checklist",
         "Work through these before the first hard frost to protect your boat over the off-season.")
    + section("Before you start", """<p>Winterizing is the difference between a spring that starts on the first turn and a spring full of repairs. Do it before the first hard frost.</p>
      <p>Plan it with the <a href="/tools/winterization-planner.html">Winterization Planner</a> for your region's timing.</p>""")
    + section("The checklist", """<ol class="pg-list">
      <li><strong>Stabilize the fuel.</strong> Add fuel stabilizer and run the engine long enough to work it through the system.</li>
      <li><strong>Fog the engine.</strong> Fogging oil protects cylinders from corrosion while it sits.</li>
      <li><strong>Drain water systems.</strong> Engine block, livewells, ballast, and fresh water — standing water freezes and cracks.</li>
      <li><strong>Change lower-unit oil.</strong> Old oil can hold water; fresh oil protects the gears all winter.</li>
      <li><strong>Remove the battery.</strong> Store it inside on a maintainer. A battery left to discharge all winter is often dead by spring.</li>
      <li><strong>Protect the outside.</strong> Cover, shrink-wrap, or indoor storage — sun and snow both damage gelcoat and vinyl.</li>
    </ol>""")
    + section("Still winterizing?", """<p>See the <a href="/blog/winterize.html">full winterization guide</a> on the blog, or run the checklist in the <a href="/features.html">AftLog app</a> where each step is interactive.</p>"""),
)



_FP_JS = """
<script>
(function () {
  var KEYS = ['boat','reg','len','from','to','eta','notes'];
  function load() { try { return JSON.parse(localStorage.getItem('aftlog_float_plan') || '{}'); } catch(e){ return {}; } }
  function save(d) { try { localStorage.setItem('aftlog_float_plan', JSON.stringify(d)); } catch(e){} }
  function q(id){ return document.getElementById(id); }
  window.fpAdd = function(list, nlabel, plabel){
    var box = q('fp-' + list);
    var row = document.createElement('div'); row.className='fp-prow';
    row.innerHTML = '<input class="fp-in" data-n style="flex:2" placeholder="'+nlabel+'"><input class="fp-in" data-p style="flex:1" placeholder="'+plabel+'"><button type="button" class="fp-x" onclick="this.parentNode.remove()">&times;</button>';
    box.appendChild(row);
  };
  window.fpCollect = function(){
    var d = load();
    KEYS.forEach(function(k){ d[k] = (q('fp-'+k)||{}).value || ''; });
    d.people = []; Array.prototype.forEach.call(document.querySelectorAll('#fp-people .fp-prow'), function(r){ d.people.push({name:r.querySelector('[data-n]').value, phone:r.querySelector('[data-p]').value}); });
    d.contacts = []; Array.prototype.forEach.call(document.querySelectorAll('#fp-contacts .fp-prow'), function(r){ d.contacts.push({name:r.querySelector('[data-n]').value, phone:r.querySelector('[data-p]').value}); });
    d.equipment = {}; Array.prototype.forEach.call(document.querySelectorAll('[data-eq]'), function(c){ d.equipment[c.dataset.eq] = c.checked; });
    return d;
  };
  window.fpSave = function(){ save(fpCollect()); alert('Float plan saved on this device.'); };
  window.fpExport = function(){ save(fpCollect()); window.print(); };
  window.fpDownload = function(){
    var d = fpCollect(); save(d);
    var labels = {pfd:'Lifejacket for everyone',radio:'VHF radio or charged phone',horn:'Horn / whistle',fireExt:'Fire extinguisher',firstAid:'First aid kit',flares:'Flares / day signals',blanket:'Thermal blanket',tow:'Tow line'};
    var t = 'FLOAT PLAN - AFTLOG\n\nMY BOAT\nBoat: '+(d.boat||'')+'  Reg: '+(d.reg||'')+'  Length: '+(d.len||'')+'ft\n\nPLAN\nFrom: '+(d.from||'')+'  To: '+(d.to||'')+'  ETA: '+(d.eta||'')+'\n';
    t += '\nPEOPLE ABOARD\n'; (d.people||[]).forEach(function(p){ if(p.name) t += '- ' + p.name + (p.phone ? ' ('+p.phone+')' : '') + '\n'; });
    t += '\nEMERGENCY CONTACT\n'; (d.contacts||[]).forEach(function(c){ if(c.name) t += '- ' + c.name + ' ' + c.phone + '\n'; });
    t += '\nEQUIPMENT\n'; Object.keys(labels).forEach(function(k){ t += (d.equipment && d.equipment[k] ? '[x] ' : '[ ] ') + labels[k] + '\n'; });
    if(d.notes) t += '\nNOTES\n' + d.notes + '\n';
    t += '\nLeave this plan with someone on shore. Generated by AftLog.';
    var blob = new Blob([t], {type:'text/plain'}); var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'aftlog-float-plan.txt'; a.click();
  };
  var d = load();
  KEYS.forEach(function(k){ if(q('fp-'+k)) q('fp-'+k).value = d[k] || ''; });
  if(d.equipment) Array.prototype.forEach.call(document.querySelectorAll('[data-eq]'), function(c){ c.checked = d.equipment[c.dataset.eq] !== false; });
  var seedPeople = (d.people||[]); var seedContacts = (d.contacts||[]);
  if(seedPeople.length) seedPeople.forEach(function(p){ fpAdd('people','Name','Phone'); var r=document.querySelectorAll('#fp-people .fp-prow'); var last=r[r.length-1]; last.querySelector('[data-n]').value=p.name||''; last.querySelector('[data-p]').value=p.phone||''; });
  else fpAdd('people','Name','Phone');
  if(seedContacts.length) seedContacts.forEach(function(c){ fpAdd('contacts','Contact','Phone'); var r=document.querySelectorAll('#fp-contacts .fp-prow'); var last=r[r.length-1]; last.querySelector('[data-n]').value=c.name||''; last.querySelector('[data-p]').value=c.phone||''; });
  else fpAdd('contacts','Contact','Phone');
})();
</script>
"""

def _float_plan_body():
    eq = "".join(
        '<label class="fp-check"><input type="checkbox" data-eq="%s" checked>%s</label>' % (k, v)
        for k, v in [
            ("pfd", "Lifejacket for everyone"), ("radio", "VHF radio or charged phone"),
            ("horn", "Horn / whistle"), ("fireExt", "Fire extinguisher"),
            ("firstAid", "First aid kit"), ("flares", "Flares / day signals"),
            ("blanket", "Thermal blanket"), ("tow", "Tow line"),
        ])
    body = (
        hero("Float Plan",
             "Tell someone where you're going and when you'll be back. If you're overdue, they call for help — with the details.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Fill it in below — your last plan is saved in this browser. Print (Save as PDF) or download a copy to share.</p>'
        + '<div class="fp-form">'
        + '<h2>My boat</h2>'
        + '<label class="pg-hint-label" for="fp-boat">Boat name</label><input id="fp-boat" class="fp-in" placeholder="e.g. Lund 1650">'
        + '<div class="fp-row"><div><label class="pg-hint-label" for="fp-reg">Registration</label><input id="fp-reg" class="fp-in" placeholder="ABC123"></div>'
        + '<div><label class="pg-hint-label" for="fp-len">Length (ft)</label><input id="fp-len" class="fp-in" placeholder="16"></div></div>'
        + '<h2>Plan</h2>'
        + '<label class="pg-hint-label" for="fp-from">Departing from</label><input id="fp-from" class="fp-in" placeholder="Harbour">'
        + '<label class="pg-hint-label" for="fp-to">Going to</label><input id="fp-to" class="fp-in" placeholder="Island">'
        + '<label class="pg-hint-label" for="fp-eta">ETA / back by</label><input id="fp-eta" class="fp-in" placeholder="18:00">'
        + '<h2>People aboard</h2><div id="fp-people" class="fp-plist"></div>'
        + '<button type="button" class="btn btn-secondary btn-sm" onclick="fpAdd(\'people\',\'Name\',\'Phone\')">+ Add person</button>'
        + '<h2>Emergency contact on shore</h2><div id="fp-contacts" class="fp-plist"></div>'
        + '<button type="button" class="btn btn-secondary btn-sm" onclick="fpAdd(\'contacts\',\'Contact\',\'Phone\')">+ Add contact</button>'
        + '<h2>Safety equipment on board</h2>'
        + eq
        + '<h2>Notes / route</h2><textarea id="fp-notes" class="fp-in" rows="3" placeholder="Route, hazards, expected return time…"></textarea>'
        + '<div class="fp-actions">'
        + '<button class="btn btn-primary" onclick="fpExport()">Print / Save as PDF</button>'
        + '<button class="btn btn-secondary" onclick="fpDownload()">Download .txt</button>'
        + '<button class="btn btn-secondary" onclick="fpSave()">Save on this device</button>'
        + '</div></div></div></section>'
        + _FP_JS
        + section("Why this matters", """<p>Search and rescue asks: tell someone where you're going and when you'll be back. If you are overdue, they call for help — with the details. It's the single best safety habit on the water.</p>""")
        + '<div class="pg-sidecard ms-promo"><div class="pg-sidecard-head">Marine Suite</div>'
        + '<p class="pg-muted" style="margin:0 0 8px">Checking conditions? CatchTales adds solunar, tide, and bite score for the fishing side.</p>'
        + '<a class="btn btn-secondary btn-sm" href="/catchtales.html">Explore CatchTales</a></div>'
    )
    return body


FP_BODY = _float_plan_body()

register(
    "tools/float-plan",
    "Float Plan — Tell Someone Where You're Going",
    "Prepare a proper float plan: trip details, people aboard, emergency contacts, safety equipment, and a printable/exportable copy.",
    FP_BODY,
)


def _buying_advisor_body():
    conditions = [("hull","Hull"),("transom","Transom"),("deck","Deck"),("wiring","Wiring"),("fuel","Fuel system"),("engine","Engine condition")]
    engine = [("compression","Compression"),("spark","Spark"),("idle","Idle behavior"),("corrosion","Corrosion")]
    trailer = [("frame","Frame"),("tires","Tires"),("lights","Lights")]
    paper = [("title","Title / bill of sale"),("registration","Registration"),("serials","Hull & engine serial numbers"),("records","Service records")]
    kinds = ["outboard","sterndrive","inboard","pwc"]

    def rating_group(prefix, items):
        rows = ""
        for key, label in items:
            rows += ("<label class=\"pg-hint-label\">"+label+"</label><div class=\"ba-rating\">"
                     '<button type="button" class="ba-rate" data-g="'+prefix+'" data-k="'+key+'" data-v="">&mdash;</button>'
                     '<button type="button" class="ba-rate" data-g="'+prefix+'" data-k="'+key+'" data-v="good">Good</button>'
                     '<button type="button" class="ba-rate" data-g="'+prefix+'" data-k="'+key+'" data-v="fair">Fair</button>'
                     '<button type="button" class="ba-rate" data-g="'+prefix+'" data-k="'+key+'" data-v="poor">Poor</button></div>')
        return rows

    type_btns = "".join('<button type="button" class="ba-type" data-t="%s">%s</button>' % (t, t.title()) for t in kinds)
    paper_box = "".join('<label class="fp-check"><input type="checkbox" data-p="%s">%s</label>' % (k, v) for k, v in paper)

    js = """
<script>
(function () {
  var K = {condition:["hull","transom","deck","wiring","fuel","engine"], engine:["compression","spark","idle","corrosion"], trailer:["frame","tires","lights"], paper:["title","registration","serials","records"]};
  var state = {boatType:'outboard', condition:{}, engine:{}, trailer:{}, paper:{}, notes:''};
  function load(){ try{ return Object.assign(state, JSON.parse(localStorage.getItem('aftlog_buying_advisor')||'{}')); }catch(e){ return state; } }
  function save(){ try{ localStorage.setItem('aftlog_buying_advisor', JSON.stringify(state)); }catch(e){} }
  function riskFlags(){
    var f=[]; var s=state; var miss=K.paper.filter(function(k){return !s.paper[k];});
    if(miss.length){ f.push('HIGH RISK - missing paperwork: '+miss.join(', ')+'.'); }
    ['hull','transom'].forEach(function(k){ if(s.condition[k]==='poor') f.push('CRITICAL - '+k+' rated POOR.'); });
    if(['hull','transom','deck'].some(function(k){return s.condition[k]==='fair';})) f.push('WATCH - structure rated fair.');
    var engPoor = K.engine.some(function(k){return s.engine[k]==='poor';}) || s.condition.engine==='poor';
    if(engPoor) f.push('HIGH RISK - engine issues detected.');
    if(K.trailer.some(function(k){return s.trailer[k]==='poor';})) f.push('HIGH RISK - trailer condition POOR.');
    var unrated = K.condition.filter(function(k){return !s.condition[k];}).length + K.engine.filter(function(k){return !s.engine[k];}).length;
    if(unrated>=6) f.push('INCOMPLETE - several sections not rated.');
    if(!f.length) f.push('No major risk warnings found.');
    return f;
  }
  function verdict(){ var f=riskFlags(); if(f.some(function(x){return x.indexOf('CRITICAL')===0;})) return 'WALK AWAY'; if(f.filter(function(x){return x.indexOf('HIGH')===0;}).length) return 'CONSIDER - with caution'; return 'LOOKS GOOD - get a sea trial + survey'; }
  function paint(){
    var f=riskFlags();
    document.getElementById('ba-warnings').innerHTML = '<strong>Verdict: '+verdict()+'</strong><br>'+f.map(function(x){return '&bull; '+x;}).join('<br>');
    document.querySelectorAll('.ba-type').forEach(function(b){ b.className = 'ba-type'+(state.boatType===b.dataset.t?' on':''); });
    document.querySelectorAll('.ba-rate').forEach(function(b){ var g=b.dataset.g, k=b.dataset.k; var v=state[g]?state[g][k]:null; b.className='ba-rate'+(v===b.dataset.v?' on':''); });
    document.querySelectorAll('[data-p]').forEach(function(c){ c.checked = !!state.paper[c.dataset.p]; });
  }
  document.querySelectorAll('.ba-type').forEach(function(b){ b.addEventListener('click', function(){ state.boatType=b.dataset.t; save(); paint(); }); });
  document.querySelectorAll('.ba-rate').forEach(function(b){ b.addEventListener('click', function(){ state[b.dataset.g]=state[b.dataset.g]||{}; state[b.dataset.g][b.dataset.k]=b.dataset.v; save(); paint(); }); });
  document.querySelectorAll('[data-p]').forEach(function(c){ c.addEventListener('change', function(){ state.paper[c.dataset.p]=c.checked; save(); paint(); }); });
  var notes=document.getElementById('ba-notes'); if(notes){ notes.value=state.notes||''; notes.addEventListener('input', function(){ state.notes=notes.value; save(); }); }
  window.baExport=function(){ save(); window.print(); };
  window.baSave=function(){ save(); alert('Buying advisor saved on this device.'); };
  window.baDownload=function(){ save(); var labels={hull:'Hull',transom:'Transom',deck:'Deck',wiring:'Wiring',fuel:'Fuel system',engine:'Engine condition',compression:'Compression',spark:'Spark',idle:'Idle behavior',corrosion:'Corrosion',frame:'Frame',tires:'Tires',lights:'Lights'};
    var t='USED-BOAT BUYING ADVISOR - AFTLOG\nBoat type: '+state.boatType+'\n'; ['condition','engine','trailer'].forEach(function(g){ t += '\n'+g.toUpperCase()+'\n'; Object.keys(state[g]||{}).forEach(function(k){ if(state[g][k]) t += '  '+labels[k]+': '+state[g][k]+'\n'; }); });
    t += '\nVERDICT: '+verdict()+'\nRISK WARNINGS\n'; riskFlags().forEach(function(x){ t += '  * '+x+'\n'; }); if(state.notes) t += '\nNOTES\n  '+state.notes+'\n';
    var blob=new Blob([t],{type:'text/plain'}); var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='aftlog-buying-advisor.txt'; a.click();
  };
  load(); paint();
})();
</script>
"""
    body = (
        hero("Buying Advisor",
             "Evaluate a used boat before you buy — condition, engine, trailer, and paperwork, with rule-based risk warnings.")
        + '<section class="section section--light"><div class="container"><div class="fp-form">'
        + '<p class="pg-muted">Answer honestly — AftLog warns on risk using simple rules. A screening aid, not a certified survey. Your session saves in this browser; Print (Save as PDF) or download a copy.</p>'
        + '<h2>Boat type</h2><div class="ba-types">' + type_btns + '</div>'
        + '<h2>Condition</h2>' + rating_group('condition', conditions)
        + '<h2>Engine checks</h2>' + rating_group('engine', engine)
        + '<h2>Trailer (if applicable)</h2>' + rating_group('trailer', trailer)
        + '<h2>Paperwork</h2><div class="fp-checkbox">' + paper_box + '</div>'
        + '<h2>Notes</h2><textarea id="ba-notes" class="fp-in" rows="3" placeholder="Asking price, observations…"></textarea>'
        + '<h2>Risk warnings</h2><div id="ba-warnings" class="ba-warnings">—</div>'
        + '<div class="fp-actions">'
        + '<button class="btn btn-primary" onclick="baExport()">Print / Save as PDF</button>'
        + '<button class="btn btn-secondary" onclick="baDownload()">Download .txt</button>'
        + '<button class="btn btn-secondary" onclick="baSave()">Save on this device</button>'
        + '</div></div></div></section>'
        + js
    )
    return body


BA_BODY = _buying_advisor_body()


register(
    "tools/buying-advisor",
    "Buying Advisor — Evaluate a Used Boat",
    "Screen a used boat before you buy: condition, engine, trailer, paperwork, and rule-based risk warnings with a shareable PDF.",
    BA_BODY,
)


def _ramp_mode_body():
    launch = [("plug","Drain plug in"),("straps","Transom straps off"),("winch","Winch unhooked"),
              ("lights","Trailer lights connected"),("bow","Bow rope ready"),("crew","Crew seated, lines clear")]
    retrieve = [("winch","Winch hooked + tight"),("straps","Transom straps on"),("plug","Drain plug out"),
                ("lights","Trailer lights + brake check"),("tie","Tie-downs / safety chain"),("gear","Keys + gear in the truck")]

    def items(mode, lst):
        return "".join('<label class="rm-item" data-mode="%s"><input type="checkbox" data-i="%s"><span class="rm-ic"></span>%s</label>' % (mode, k, v) for k, v in lst)

    js = """
<script>
(function () {
  var rmItems = document.querySelectorAll('.rm-item input');
  var flat = Array.prototype.filter.call(rmItems, function(c){ return c.checked; });
  function currentMode(){ return document.querySelector('.rm-mode.on').dataset.mode; }
  function paint(){
    var mode = currentMode();
    Array.prototype.forEach.call(document.querySelectorAll('.rm-item'), function(item){
      item.style.display = (item.dataset.mode === mode) ? '' : 'none';
    });
    var rem = mode === 'launch' ? 'Lights on? Plug in? Straps off before you back down the ramp.' : 'Winch tight, straps on, drain plug OUT before you leave. Check brake lights on the road.';
    document.getElementById('rm-reminder').textContent = rem;
    var visible = Array.prototype.filter.call(document.querySelectorAll('.rm-item input'), function(c){
      if(c.checked){ }
      return (c.closest('.rm-item').dataset.mode === mode);
    });
    var done = visible.filter(function(c){ return c.checked; }).length;
    var ready = visible.length > 0 && done === visible.length;
    var bar = document.getElementById('rm-progress');
    if(bar){ bar.value = visible.length ? done/visible.length : 0; bar.style.backgroundColor = ready ? '#76FF03' : '#FF4B4B'; }
    var banner = document.getElementById('rm-ready');
    if(banner){
      banner.style.display = ready ? 'block' : 'none';
      banner.textContent = mode === 'launch' ? 'Ready to launch! Drain plug in, straps off, crew set. Take it slow.' : 'Ready for the road! Winch tight, straps on, drain plug out, checks done.';
    }
  }
  Array.prototype.forEach.call(document.querySelectorAll('.rm-mode'), function(b){
    b.addEventListener('click', function(){
      Array.prototype.forEach.call(document.querySelectorAll('.rm-mode'), function(x){ x.classList.remove('on'); });
      b.classList.add('on'); paint();
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('.rm-item input'), function(c){
    c.addEventListener('change', function(){ paint(); });
  });
  document.getElementById('rm-reset').addEventListener('click', function(){
    Array.prototype.forEach.call(document.querySelectorAll('.rm-item input'), function(c){ c.checked = false; });
    paint();
  });
  paint();
})();
</script>
"""
    body = (
        hero("Ramp Mode",
             "Launch or retrieve with a distraction-free, big-button checklist — plus the safety reminders that matter.")
        + '<section class="section section--light"><div class="container"><div class="fp-form">'
        + '<div class="rm-tabs"><button type="button" class="rm-mode on" data-mode="launch">Launch</button>'
        + '<button type="button" class="rm-mode" data-mode="retrieve">Retrieve</button></div>'
        + '<progress id="rm-progress" max="1" value="0" class="rm-progress"></progress>'
        + '<div id="rm-ready" class="rm-ready" style="display:none"></div>'
        + '<div class="rm-remind" id="rm-reminder"></div>'
        + '<div class="rm-items">' + items('launch', launch) + items('retrieve', retrieve) + '</div>'
        + '<button type="button" id="rm-reset" class="btn btn-secondary">Reset</button>'
        + '</div></div></section>'
        + js
        + section("Why it matters", """<p>Ramps are where most trailer-boat damage happens — and where it's easiest to forget the basics. A fixed checklist keeps the drain plug in, the straps off, and the winch unhooked before you back down. Session-only: nothing is saved.</p>""")
    )
    return body


RM_BODY = _ramp_mode_body()


register(
    "tools/ramp-mode",
    "Ramp Mode — Launch & Retrieve Checklist",
    "A distraction-free, big-button launch and retrieve checklist for the boat ramp, with safety reminders.",
    RM_BODY,
)


def _calculators_body():
    imports = (
        '<section class="section section--light"><div class="container">'
        '<p class="pg-muted">Same formulas as the AftLog app. Metric-first with imperial conversions. Inputs are clamped to safe ranges; results are colour-coded.</p>'
        '<div class="cal-toggle"><button type="button" class="btn btn-sm cal-unit on" data-u="metric">Metric</button>'
        '<button type="button" class="btn btn-sm cal-unit" data-u="imperial">Imperial</button></div>'
    )
    def card(idnum, name, desc, fields_html, out_id):
        head = '<article class="cal-card" id="cal-%d"><h2>%d. %s</h2><p class="pg-muted">%s</p>' % (
            idnum, idnum, name, desc)
        return head + fields_html + '<div class="cal-out" id="%s">—</div></article>' % (out_id)
    f_fuel = ('<div class="cal-fields"><label>Horsepower<input id="fu_hp" type="number" value="150" min="1"></label>'
              '<label>Throttle fraction (0-1, cruise ~0.7)<input id="fu_t" type="number" value="0.7" step="0.05" min="0.1" max="1"></label>'
              '<label class="cal-check"><input id="fu_2s" type="checkbox">2-stroke</label></div>')
    f_slip = ('<div class="cal-fields"><label>Speed <span data-uf="kmh">km/h</span><input id="sl_sp" type="number" value="40"></label>'
              '<label>RPM<input id="sl_rpm" type="number" value="4000"></label>'
              '<label>Prop pitch (inches)<input id="sl_p" type="number" value="19"></label></div>')
    f_tongue = ('<div class="cal-fields"><label>Total weight <span data-uf="kg">kg</span><input id="tw_w" type="number" value="1000"></label>'
                '<label>Percentage (approx. 10)<input id="tw_p" type="number" value="10" min="1" max="20"></label></div>')
    f_anchor = ('<div class="cal-fields"><label>Water depth <span data-uf="m">m</span><input id="an_d" type="number" value="6"></label>'
                '<label>Bow height <span data-uf="m">m</span><input id="an_b" type="number" value="1.5"></label>'
                '<label>Scope ratio (e.g., 5:1)<input id="an_s" type="number" value="5" min="2" max="10"></label></div>')
    f_volt = ('<div class="cal-fields"><label>Run length <span data-uf="m">m</span><input id="vo_l" type="number" value="10"></label>'
              '<label>Amps<input id="vo_a" type="number" value="15"></label>'
              '<label>Cable size <span data-uf="mm2">mm²</span><input id="vo_c" type="number" value="2.5" min="0.1"></label></div>')
    f_oil = ('<div class="cal-fields"><label>Ratio (e.g., 50:1)<input id="oi_r" type="number" value="50" min="20" max="100"></label>'
             '<label>Fuel <span data-uf="L">L</span><input id="oi_f" type="number" value="20"></label></div>')

    body = (
        hero("Calculators", "Quick, grounded boating math — the same formulas as the AftLog app.")
        + imports
        + card(1, "Fuel burn", "How much fuel an engine uses at a given throttle.",
               f_fuel, "out-fuel")
        + card(2, "Prop slip", "How much propeller efficiency you're losing at speed (lower is better).",
               f_slip, "out-slip")
        + card(3, "Tongue weight", "The target trailer tongue weight for safe towing.",
               f_tongue, "out-tongue")
        + card(4, "Anchor scope", "How much rode (line) you need for a given depth and scope.",
               f_anchor, "out-anchor")
        + card(5, "Voltage drop", "Approx. voltage loss over a cable run (keep under 3 V).",
               f_volt, "out-volt")
        + card(6, "Oil mix (2-stroke premix)", "How much oil to add for a 2-stroke fuel mix.",
               f_oil, "out-oil")
        + '</section>'
    )
    # JS appended separately in _calculators_body return
    global _CALC_JS
    _CALC_JS = r"""
<script>
(function () {
  var unit = 'metric';
  function $(id){ return document.getElementById(id); }
  function n(v){ return (isNaN(v)?0:v); }
  function setOut(id, txt, level){ var o=$(id); if(o){ o.textContent=txt; o.className='cal-out'+(level?' '+level:''); } }
  function U(m, im){ return unit==='metric' ? m : im; }
  // metrics: which span shows m or im
  function paintUnits(){
    var map = {kmh:['km/h','mph'], kg:['kg','lb'], m:['m','ft'], mm2:['mm²','AWG'], L:['L','US gal']};
    document.querySelectorAll('[data-uf]').forEach(function(s){ var k=s.dataset.uf; if(map[k]) s.textContent = unit==='metric'?map[k][0]:map[k][1]; });
    Array.prototype.forEach.call(document.querySelectorAll('.cal-unit'), function(b){ b.classList.toggle('on', b.dataset.u===unit); });
  }
  function compute(){
    var hp = n($('fu_hp').value), t = Math.min(1, Math.max(0.05, n($('fu_t').value))), two = $('fu_2s').checked;
    var lhr = hp * (two?0.014:0.010) * t;
    setOut('out-fuel', (unit==='metric'? lhr.toFixed(1)+' L/hr' : (lhr/3.785).toFixed(1)+' gal/hr'), '');

    var sp = n($('sl_sp').value), rpm = n($('sl_rpm').value), pt = n($('sl_p').value);
    var tsp = unit==='metric'? sp : sp*1.60934;
    var theo = rpm*pt*0.000507; var slip = theo<=0?0:Math.max(0,Math.min(100,(1-tsp/theo)*100));
    setOut('out-slip', slip.toFixed(1)+'%', slip<10?'green':slip<20?'yellow':'red');

    var w = n($('tw_w').value), p = n($('tw_p').value);
    var tw = w*p/100;
    setOut('out-tongue', (unit==='metric'? tw.toFixed(0)+' kg':' (metric '+(tw/2.2046).toFixed(0)+')')+' → target ≈ '+(unit==='metric'? (tw).toFixed(0): (tw/2.2046).toFixed(0))+' lb', p<7?'red':p<=15?'green':'yellow');

    var d = n($('an_d').value), bh = n($('an_b').value), s = n($('an_s').value);
    var rodeM = (d+bh)*s;
    setOut('out-anchor', U(rodeM.toFixed(1)+' m', (rodeM*3.2808).toFixed(1)+' ft'), s>=5?'green':'yellow');

    var l = n($('vo_l').value), a = n($('vo_a').value), c = n($('vo_c').value);
    var lm = unit==='metric'? l : l*0.3048;
    var v = c<=0?0: (2*lm*a*0.017)/c;
    setOut('out-volt', v.toFixed(2)+' V', v<3?'green':v<10?'yellow':'red');

    var ratio = n($('oi_r').value), fuel = n($('oi_f').value);
    var oil = ratio>0 ? (unit==='metric'? fuel*1000/ratio : fuel*128/ratio) : 0;
    var valid = ratio>=20 && ratio<=100;
    setOut('out-oil', (unit==='metric'? oil.toFixed(0)+' mL' : oil.toFixed(1)+' oz')+' of oil', valid?'green':'red');
  }
  ['fu_hp','fu_t','fu_2s','sl_sp','sl_rpm','sl_p','tw_w','tw_p','an_d','an_b','an_s','vo_l','vo_a','vo_c','oi_r','oi_f'].forEach(function(id){
    var e = $(id); if(e) e.addEventListener('input', compute);
  });
  document.querySelectorAll('.cal-unit').forEach(function(b){ b.addEventListener('click', function(){ unit=b.dataset.u; paintUnits(); compute(); }); });
  paintUnits(); compute();
})();
</script>
"""
    return body + _CALC_JS


CALCS_BODY = _calculators_body()


register(
    "tools/calculators",
    "AftLog Calculators — Boat Math",
    "Fuel burn, prop slip, tongue weight, anchor scope, voltage drop, and 2-stroke oil mix — same formulas as the AftLog app.",
    CALCS_BODY,
)


def _vea_body():
    js = """
<script>
(function () {
  var DATA = null; var active = 0;
  function load(){
    fetch('/data/vea.json').then(function(r){ return r.json(); }).then(function(d){
      DATA = d;
      var sel = document.getElementById('vea-diagram');
      (d.diagrams||[]).forEach(function(dg, i){
        var o = document.createElement('option'); o.value = i; o.textContent = dg.title; sel.appendChild(o);
      });
      if((d.diagrams||[]).length) { paint(0); }
    }).catch(function(){ var el=document.getElementById('vea-canvas'); if(el) el.textContent='Could not load diagram data.'; });
  }
  function paint(i){
    var dg = DATA.diagrams[i];
    var canvas = document.getElementById('vea-canvas');
    var img = document.getElementById('vea-img');
    img.src = dg.asset;
    var iv = document.getElementById('vea-interactive');
    iv.innerHTML = '';
    (dg.hotspots||[]).forEach(function(h){
      var s = document.createElementNS('http://www.w3.org/2000/svg','svg');
      s.setAttribute('viewBox','0 0 100 100'); s.setAttribute('preserveAspectRatio','none');
      var el = document.createElementNS('http://www.w3.org/2000/svg', h.shape==='circle'?'circle':'rect');
      if(h.shape==='circle'){ el.setAttribute('cx', h.x*100); el.setAttribute('cy', h.y*100); el.setAttribute('r', Math.max(h.w,h.h)*50); }
      else { el.setAttribute('x', h.x*100); el.setAttribute('y', h.y*100); el.setAttribute('width', h.w*100); el.setAttribute('height', h.h*100); }
      el.setAttribute('class','vea-hot');
      el.addEventListener('click', function(){ return false; });
      iv.appendChild(s); iv.lastChild.appendChild(el);
      el.addEventListener('click', function(){ openSymptom(h); });
      el.title = h.label;
    });
  }
  function esc(x){ return (x||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function openSymptom(h){
    var panel = document.getElementById('vea-panel');
    var sym = DATA.symptoms[h.symptomKey];
    var sev = sym ? (sym.severity||'info') : 'info';
    var sevLabel = {info:'Info', attention:'ATTENTION', serious:'SERIOUS', stop:'STOP'}[sev] || sev;
    var causes = '';
    var cs = sym && sym.causes ? sym.causes : {};
    Object.keys(cs).forEach(function(drive){
      if((cs[drive]||[]).length){ causes += '<div class=\"vea-drive\">'+esc(drive)+'</div><ul>' + cs[drive].map(function(c){ return '<li>'+esc(c)+'</li>'; }).join('') + '</ul>'; }
    });
    panel.innerHTML =
      '<div class=\"vea-sev vea-sev-'+sev+'\">'+esc(sevLabel)+'</div>' +
      '<h3>'+esc(h.label)+'</h3>' +
      (h.purpose ? '<p class=\"vea-purpose\">'+esc(h.purpose)+'</p>' : '') +
      '<p class=\"vea-check\"><strong>Check:</strong> '+esc(h.check)+'</p>' +
      (sym && sym.start ? '<div class=\"vea-block\"><strong>Start here:</strong> '+esc(sym.start)+'</div>' : '') +
      (causes ? '<div class=\"vea-block\"><strong>Likely causes:</strong>'+causes+'</div>' : '') +
      (sym && sym.ifNotResolved ? '<div class=\"vea-block vea-stuck\"><strong>If not resolved:</strong> '+esc(sym.ifNotResolved)+'</div>' : '') +
      '<button type=\"button\" class=\"btn btn-secondary btn-sm\" onclick=\"closePanel()\">Close</button>';
    panel.classList.add('open');
  }
  window.closePanel = function(){ document.getElementById('vea-panel').classList.remove('open'); };
  document.addEventListener('DOMContentLoaded', load);
  window.vSelect = function(i){ paint(+i); };
})();
</script>
"""
    body = (
        hero("Visual Engine Assist",
             "Tap a part on the engine to open its trouble-shooting flow — plain-language causes and what to check first.")
        + '<section class="section section--light"><div class="container">'
        + '<label class="pg-hint-label" for="vea-diagram">Choose a system</label>'
        + '<select id="vea-diagram" class="pg-select" onchange="vSelect(this.value)"><option value="">Loading systems…</option></select>'
        + '<div class="vea-stage">'
        + '<div class="vea-canvas" id="vea-canvas"><img id="vea-img" alt="Engine diagram"><div id="vea-interactive" class="vea-hotzone"></div></div>'
        + '<aside class="vea-panel" id="vea-panel"></aside>'
        + '</div>'
        + '<p class="pg-muted">Zoom with your browser/scroll. Tap a highlighted area to open its troubleshooting flow. Offline-friendly — nothing is uploaded.</p>'
        + '</div></section>'
        + js
    )
    return body


VEA_BODY = _vea_body()


register(
    "tools/visual-engine-assist",
    "Visual Engine Assist — Tap Any Engine Part",
    "Interactive engine diagram: tap a part to open its plain-language troubleshooting flow with causes, severity, and next steps.",
    VEA_BODY,
)


def _ai_diag_body():
    js = """
<script>
(function () {
  var DATA = null;
  var state = {symptomKey:'', drive:'outboard', answers:{start:'',conditions:'',sounds:'',smells:'',vibrations:'',recentWork:''}, photo:''};
  var drives = ['outboard','inboard','jet','pontoon','other'];
  var Q = ['start','conditions','sounds','smells','vibrations','recentWork'];
  var QL = {start:'When did it start?',conditions:'Conditions (idle/throttle/load)',sounds:'Sounds',smells:'Smells',vibrations:'Vibrations',recentWork:'Recent maintenance'};
  function load(){ return state; }
  function save(){ try{ localStorage.setItem('aftlog_ai_diag', JSON.stringify(state)); }catch(e){} }
  function causesFor(k, dr){ var c=(DATA.symptoms[k]||{}).causes||{}; return c[dr]||c['default']||[]; }
  function fixesFor(k, dr){ var f=(DATA.symptoms[k]||{}).fixes||{}; return f[dr]||f['default']||[]; }
  function sevFor(k){ return (DATA.symptoms[k]||{}).severity||'info'; }
  function fallbackFor(k){ return (DATA.symptoms[k]||{}).ifNotResolved||''; }
  function pin(req){ return req && req.readyState <= 1; }
  function paint(){
    // symptom selector
    var sel = document.getElementById('aid-symptom');
    if (sel && !sel.dataset.built && DATA){
      sel.dataset.built='1';
      Object.keys(DATA.symptoms).sort().forEach(function(k){ var o=document.createElement('option'); o.value=k; o.textContent=k; sel.appendChild(o); });
    }
    if(sel) sel.value = state.symptomKey||'';
    // drive chips
    document.querySelectorAll('.ai-drive').forEach(function(b){ b.classList.toggle('on', b.dataset.d===state.drive); });
    // questions
    Q.forEach(function(k){ var e=document.getElementById('aiq-'+k); if(e && e.value==='__init') { } });
    // diagnosis
    var box = document.getElementById('ai-diagnosis');
    if(!state.symptomKey || !DATA){ box.innerHTML='<p class="pg-muted">Select a symptom to see the analysis.</p>'; }
    else {
      var sev = sevFor(state.symptomKey); var causes=causesFor(state.symptomKey,state.drive); var fixes=fixesFor(state.symptomKey,state.drive); var fb=fallbackFor(state.symptomKey);
      var sevCls = sev==='stop'?'stop':(sev==='serious'||sev==='attention')?'warn':'info';
      var h = '<span class="ai-sev ai-sev-'+sevCls+'">'+sev.toUpperCase()+'</span><h3>'+esc(state.symptomKey)+'</h3>';
      if(causes.length){ h+='<div class="ai-block"><strong>Likely causes</strong><ul>'+causes.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul></div>'; }
      if(fixes.length){ h+='<div class="ai-block"><strong>Next steps</strong><ul>'+fixes.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul></div>'; }
      if(fb){ h+='<div class="ai-block ai-fb"><strong>If not resolved:</strong> '+esc(fb)+'</div>'; }
      box.innerHTML = h;
    }
    // photo preview
    var pv=document.getElementById('ai-photo-preview');
    if(pv){ pv.style.display = state.photo ? 'block':'none'; if(state.photo && pv.tagName!=='IMG') {} }
  }
  function esc(x){ return (x||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function init(){
    try{ var s=JSON.parse(localStorage.getItem('aftlog_ai_diag')||'{}'); Object.keys(s).forEach(function(k){ if(k in state) state[k]=s[k]; }); }catch(e){}
    Q.forEach(function(k){ var e=document.getElementById('aiq-'+k); if(e) e.value=state.answers[k]||''; });
    if(state.photo) document.getElementById('ai-photo-preview').style.display='block';
    document.querySelectorAll('.ai-drive').forEach(function(b){ b.addEventListener('click', function(){ state.drive=b.dataset.d; save(); paint(); }); });
    Q.forEach(function(k){ var e=document.getElementById('aiq-'+k); if(e) e.addEventListener('input', function(){ state.answers[k]=e.value; save(); }); });
    fetch('/data/vea.json').then(function(r){return r.json();}).then(function(d){ DATA=d; paint(); }).catch(function(){}); 
    paint();
  }
  window.aiSymptom=function(){ if(sel){state.symptomKey=sel.value; save(); paint();} };
  window.aiSave=function(){ save(); alert('Diagnostic saved on this device.'); };
  window.aiExport=function(){ save(); window.print(); };
  window.aiDownload=function(){ save(); var k=state.symptomKey, h='AI DIAGNOSTIC - AFTLOG\nSymptom: '+(k||'?')+'\nEngine: '+state.drive+'\n\nDETAILS\n'; Q.forEach(function(q){ if(state.answers[q]) h += '  '+QL[q]+': '+state.answers[q]+'\n'; }); if(k&&DATA){ h+='\nLIKELY CAUSES\n'; causesFor(k,state.drive).forEach(function(c){h+='  * '+c+'\n';}); h+='\nNEXT STEPS\n'; fixesFor(k,state.drive).forEach(function(c){h+='  - '+c+'\n';}); var fb=fallbackFor(k); if(fb) h+='\nIF NOT RESOLVED\n  '+fb+'\n'; } var blob=new Blob([h],{type:'text/plain'}); var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='aftlog-ai-diagnostics.txt'; a.click(); };
  window.aiPhoto=function(input){
    if(!input.files || !input.files[0]) return;
    var reader=new FileReader(); reader.onload=function(e){
      state.photo=String(e.target.result).substr(0,240000); save();
      var pv=document.getElementById('ai-photo-preview'); if(pv) pv.style.display='block';
    }; reader.readAsDataURL(input.files[0]);
  };
  document.addEventListener('DOMContentLoaded', init);
})();
</script>
"""
    body = (
        hero("AI Diagnostics",
             "Pick a symptom, answer a few questions, and get the likely causes, next steps, and when to stop. Grounded on-device — nothing is uploaded.")
        + '<section class="section section--light"><div class="container"><div class="fp-form">'
        + '<label class="pg-hint-label" for="ai-symptom">Symptom</label>'
        + '<select id="ai-symptom" class="pg-select" onchange="window.aiSymptom&&aiSymptom()"><option value="">Loading symptoms…</option></select>'
        + '<label class="pg-hint-label" style="margin-top:14px">Engine type</label>'
        + '<div class="ai-drives">' + "".join('<button type="button" class="ai-drive" data-d="%s">%s</button>' % (d, d) for d in ["outboard","inboard","jet","pontoon","other"]) + '</div>'
        + '<label class="pg-hint-label" style="margin-top:14px">Photo (optional — stays on your device)</label>'
        + '<input type="file" accept="image/*" onchange="aiPhoto(this)" class="ai-file">'
        + '<div id="ai-photo-preview" style="display:none" class="ai-photo-ok">Photo attached (local only).</div>'
        + '<h2>Details</h2>'
        + "".join('<label class="pg-hint-label">%s</label><input id="aiq-%s" class="fp-in" placeholder="Tap to describe">' % (ql, k) for k, ql in [("start","When did it start?"),("conditions","Conditions (idle / throttle / load)"),("sounds","Sounds"),("smells","Smells"),("vibrations","Vibrations"),("recentWork","Recent maintenance")])
        + '<h2>Diagnosis</h2><div id="ai-diagnosis" class="ai-diagnosis">—</div>'
        + '<div class="fp-actions">'
        + '<button class="btn btn-primary" onclick="aiExport()">Print / Save as PDF</button>'
        + '<button class="btn btn-secondary" onclick="aiDownload()">Download .txt</button>'
        + '<button class="btn btn-secondary" onclick="aiSave()">Save on this device</button>'
        + '</div></div></div></section>'
        + js
        + section("Grounded, on-device", """<p>This uses the same structured symptom data as the AftLog app — ranked causes, next steps, and a clear stop line. It's guidance, not a certified diagnosis: see a marine mechanic for anything serious.</p>""")
    )
    return body


AID_BODY = _ai_diag_body()


register(
    "tools/ai-diagnostics",
    "AI Diagnostics — Guided Symptom Check",
    "Pick a symptom, answer a few questions, and get likely causes, next steps, and when to stop — grounded on-device.",
    AID_BODY,
)


register(
    "tools/ask-aftlog",
    "Ask AftLog — Grounded Offline Assistant",
    "A grounded chat assistant that answers boating, maintenance, and troubleshooting questions offline.",
    hero("Ask AftLog",
         "A grounded chat assistant — troubleshooting, checklists, calculators, winterization, and planner rules, answered offline.")
    + '<section class="section section--light"><div class="container"><div class="ask-box">'
    + '<div id="ask-log" class="ask-log"></div>'
    + '<div class="ask-row"><input id="ask-input" class="ask-input" placeholder="Ask about your boat…">'
    + '<button class="btn btn-primary" onclick="ask(document.getElementById(\'ask-input\').value)">Send</button></div>'
    + '<label class="ask-photo-label"><input type="file" accept="image/*" style="display:none" onchange="askPhoto(this)"> Attach photo (local only)</label>'
    + '<span class="ask-photo" style="display:none">Photo attached - stored on your device.</span>'
    + '<div class="fp-actions"><button class="btn btn-secondary" onclick="askExport()">Export conversation (.txt)</button></div>'
    + '</div></div></section>'
    + '<script src="/tools/ask-aftlog.js" defer></script>',
)


register(
    "tools/predictive-planner",
    "Predictive Planner — Anticipate Maintenance",
    "Predict upcoming maintenance from engine hours, logged services, and interval rules — with hours remaining, dates, and severity.",
    hero("Predictive Planner",
         "Anticipate what's next — from your engine hours, logged services, and interval rules.")
    + '<section class="section section--light"><div class="container"><div class="fp-form">'
    + '<p class="pg-muted">Enter current engine hours and avg hours/month, then the last-service hours/date per item. Everything is saved in this browser.</p>'
    + '<div class="pp-inputs"><label class="pg-hint-label">Current engine hours<input id="pp-hours" class="fp-in" type="number" value="250"></label>'
    + '<label class="pg-hint-label">Avg hours / month<input id="pp-avg" class="fp-in" type="number" value="20"></label></div>'
    + '<div id="pp-head" class="pp-head">-</div>'
    + '<div id="pp-list" class="pp-list"></div>'
    + '<div class="fp-actions">'
    + '<button class="btn btn-primary" onclick="ppExport()">Print / Save as PDF</button>'
    + '<button class="btn btn-secondary" onclick="ppDownload()">Download .txt</button>'
    + '</div></div></div></section>'
    + '<script src="/tools/predictive-planner.js" defer></script>',
)


register(
    "tools/trip-patterns",
    "Trip Patterns — Your Season at a Glance",
    "Analyze your trips: usage totals, seasonality, trends, and unusual trips — all on-device.",
    hero("Trip Patterns",
         "Your season at a glance — usage, seasonality, trends, and the trips that stand out.")
    + '<section class="section section--light"><div class="container"><div class="fp-form">'
    + '<p class="pg-muted">Add trips (date, distance, hours, optional fuel) and the engine computes your patterns. Everything stays in this browser.</p>'
    + '<div class="tp-add"><input id="tp-d" class="fp-in" placeholder="Date  YYYY-MM-DD" style="flex:2">'
    + '<input id="tp-km" class="fp-in" placeholder="km" type="number" style="flex:1">'
    + '<input id="tp-h" class="fp-in" placeholder="hours" type="number" style="flex:1">'
    + '<input id="tp-f" class="fp-in" placeholder="fuel L" type="number" style="flex:1">'
    + '<button class="btn btn-primary" onclick="tpAdd()">Add trip</button></div>'
    + '<button class="btn btn-secondary btn-sm" onclick="tpReset()">Clear all</button>'
    + '<div id="tp-results"><p class="pg-muted">Add at least one trip to see patterns.</p></div>'
    + '<div class="fp-actions"><button class="btn btn-secondary" onclick="tpExport()">Export .txt</button>'
    + '<button class="btn btn-secondary" onclick="window.print()">Print / Save as PDF</button></div>'
    + '</div></div></section>'
    + '<script src="/tools/trip-patterns.js" defer></script>',
)


def write(path: str, content: str):
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    print(f"  wrote {f.relative_to(ROOT)} ({len(content)} bytes)")


def generate_help(rooot=ROOT):
    """v1 Help System (DEEPSEEK STEP 8.1): read the canonical topic JSONs
    in help/topics/ and emit help/index.html + help/<id>.html + a static
    search index (help/topics-index.js). Shared header/footer + brand block.
    """
    topics_dir = (rooot / "help" / "topics")
    if not topics_dir.exists():
        print("  (no help/topics — skipping help pages)")
        return
    topics = []
    for f in sorted(topics_dir.glob("*.json")):
        try:
            topics.append(json.load(f.open(encoding="utf-8")))
        except Exception as e:
            print("  !! bad help json", f.name, e)
    topics.sort(key=lambda t: t["title"].lower())

    cats = []
    for t in topics:
        if t["category"] not in cats:
            cats.append(t["category"])

    def esc(s): return html.escape(s)

    # topic page
    def topic_doc(t):
        steps = "".join(
            f'<li class="pg-help-step">{esc(item["text"])}'
            + (f'<div class="pg-help-img">[screenshot: {esc(item["image"])}]</div>' if item.get("image") else '')
            + '</li>' for item in t["steps"])
        tips = "".join(f'<li>{esc(tip)}</li>' for tip in t.get("tips", []))
        related_ids = t.get("related", [])
        ids = {x["id"]: x for x in topics}
        related = "".join(
            f'<li><a href="/help/{esc(rid)}.html">{esc(ids[rid]["title"])}</a></li>'
            for rid in related_ids if rid in ids)
        body = (
            '<section class="section section--light"><div class="container pg-help">'
            f'<span class="pg-cat-tag">{esc(t["category"])}</span>'
            f'<h1>{esc(t["title"])}</h1>'
            f'<p class="pg-muted pg-help-desc">{esc(t["description"])}</p>'
            f'<h2>Steps</h2>'
            f'<ol class="pg-list">{steps}</ol>'
            + (f'<h2>Tips</h2><ul class="pg-list">{tips}</ul>' if tips else '')
            + (f'<h2>Related</h2><ul class="pg-list">{related}</ul>' if related else '')
            + '<p class="pg-muted" style="margin-top:22px"><a href="/help/index.html">Back to Help</a></p>'
            + '</div></section>'
        )
        # hero with brand block, but H1 is inside the body (we want the title as H1)
        # use page() with a custom body that includes its own H1
        top = (
            '<section class="hero hero--dark pg-hero"><div class="container hero-inner pg-hero-inner">'
            '<div class="hero-text">'
            '<div class="brand-block">'
            '<img class="hero-logo brand-logo" src="/images/aftlog-logo.png" alt="AftLog logo">'
            '<span class="kicker brand-slogan">Keeping your boat shipshape!</span>'
            '</div></div></div></section>'
        )
        return page("help", f"{t['title']} — AftLog Help", t["description"],
                    top + body, active="/help/")

    # index: search + category bar + cards
    cards = "".join(
        f'<a class="pg-blog-card" data-cat="{esc(t["category"].lower())}" '
        f'href="/help/{esc(t["id"])}.html"><span class="pg-cat-tag">{esc(t["category"])}</span>'
        f'<h3>{esc(t["title"])}</h3><p>{esc(t["description"])}</p></a>'
        for t in topics)
    cat_btns = ''.join(
        f'<button type="button" class="pg-cat-btn{" on" if c == cats[0] else ""}" data-cat="{esc(c.lower())}">{esc(c)}</button>'
        for c in ["All"] + cats)
    index_body = (
        hero("Help", "Step-by-step guides for AftLog — search a topic or browse by category.")
        + f'<section class="section section--alt pg-cat-section"><div class="container">'
        + f'<input class="pg-help-search" id="help-search" type="search" placeholder="Search help topics…" aria-label="Search help">'
        + f'<div class="pg-cat-bar" role="group" aria-label="Filter by category">{cat_btns}</div>'
        + f'<div class="pg-article-grid" id="help-grid">{cards}</div></div></section>'
        + '<div class="pg-marine-suite"><div class="brand-block"><span class="kicker brand-slogan">Marine Suite</span><h3>Two apps for one day on the water.</h3></div>'
        + '<p>AftLog handles your boat — maintenance, safety, and trip prep. CatchTales handles your fishing — species, spots, and conditions. Together, they make a full day on the water easier.</p>'
        + '<a href="/catchtales.html" class="pg-marine-cta">About CatchTales →</a></div>'
        + section("Still stuck?", '<p><a class="btn btn-secondary" href="/support.html">Contact support</a> · <a class="btn btn-secondary" href="/faq.html">See the FAQ</a></p>')
        + '<script src="/help/help.js"></script>'
    )
    write("help/index.html", page("help/index", "AftLog Help — Guides & How-To", "Step-by-step help topics for AftLog: logging, maintenance, planner, AI, tools, and backup.", index_body, active="/help/"))

    for t in topics:
        write(f"help/{t['id']}.html", topic_doc(t))

    # search/filter JS
    js = """(function () {
  var input = document.getElementById('help-search');
  var btns = document.querySelectorAll('.pg-cat-btn');
  var cards = document.querySelectorAll('#help-grid .pg-blog-card');
  var curCat = 'all';
  function apply() {
    var q = (input.value || '').toLowerCase();
    cards.forEach(function (c) {
      var ok = true;
      if (curCat !== 'all' && c.dataset.cat !== curCat) ok = false;
      if (ok && q) {
        var text = (c.textContent || '').toLowerCase();
        if (text.indexOf(q) === -1) ok = false;
      }
      c.style.display = ok ? '' : 'none';
    });
  }
  if (input) input.addEventListener('input', apply);
  if (btns) btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      curCat = b.dataset.cat;
      apply();
    });
  });
})();
"""
    write("help/help.js", js)
    print(f"  help: {len(topics)} topics, {len(cats)} categories")


# ── STEP 8.15–8.20: Compliance / Manual Finder / DIY / Battery / Glossary ──

def _compliance_body():
    rules = [
        ("Registration", "In Canada, recreational boats under 15 gross tonnes are registered provincially (licence numbers) — federal Pleasure Craft Licence is the standard. Renewal is typically every 10 years for the PLC, or yearly for provincial stickers where applicable."),
        ("Operator card", "Anyone born after April 1, 1983 needs a Pleasure Craft Operator Card in Canada. Carry it aboard."),
        ("PFDs", "One properly-fitting lifejacket/PFD per person, plus one buoyant heaving line and one throwable (if over 6 m). Children under 13 must wear theirs."),
        ("Safety gear", "Sound-signalling device, flashlight or flares, fire extinguisher (type 5B:C if motorized), and a bailer or bilge pump."),
        ("Trailer brakes", "Provincial rules vary, but Manitoba requires brakes on trailers above 1,361 kg — check your province's threshold."),
        ("Licence plate / insurance", "Trailers need plates; boat insurance is optional by law in most provinces but required by many marinas and lenders."),
    ]
    cards = "".join(
        f'<article class="cal-card"><h2>{t}</h2><p class="pg-muted">{d}</p></article>'
        for t, d in rules)
    return (
        hero("Compliance", "Registration, safety gear, and the boating rules that keep you legal — and covered.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Starter guide for Canada / Manitoba boating law. Check your province for the exact numbers.</p>'
        + '<p><a class="btn btn-primary" href="/blog/safety-equipment.html">See the safety equipment list</a></p>'
        + cards
        + '</div></section>'
        + section("Renewal reminders", "<p>Add your registration and insurance documents under a boat \u2192 Documents, with expiry dates. AftLog reminds you before they lapse.</p>")
    )


register("tools/compliance", "AftLog Compliance — Boating Rules & Safety Gear",
         "Canada/Manitoba boating compliance starter guide: registration, operator card, PFDs, safety gear, trailer brakes, and insurance rules.",
         _compliance_body())


_MANUAL_CATS = [
    ("Engine manuals — free (OEM)", [
        ("Mercury Marine", "https://www.mercurymarine.com/en/us/parts-and-service", "Searchable by serial number"),
        ("Yamaha Outboards", "https://www.yamaha-motor.ca/en/products/boating", "All models, incl. older"),
        ("Honda Marine", "https://marine.honda.com/support", "Straightforward PDF downloads"),
        ("Suzuki Marine", "https://suzukimarine.com/owners-zone/", "Owner + service manuals"),
        ("Evinrude / BRP", "https://www.evinrude.com", "Discontinued but still hosted"),
        ("Volvo Penta", "https://www.volvopenta.com", "Gas, diesel, sterndrive, IPS"),
        ("Mercury MerCruiser", "https://www.mercurymarine.com/en/us/parts-and-service", "Inboard/sterndrive"),
        ("Tohatsu", "https://www.tohatsu.com/tech_info/index.html", ""),
    ]),
    ("General manual libraries", [
        ("ManualsLib", "https://www.manualslib.com", "Boats, outboards, electronics, trailers, safety gear"),
        ("ManualsOnline", "https://www.manualsonline.com", "Consumer-electronics heavy"),
        ("BoatInfo.no", "https://boatinfo.no", "Huge archive — old Johnson/Evinrude, wiring diagrams. Hidden gem"),
    ]),
    ("Professional manuals (paid)", [
        ("Seloc", "https://www.selocmarine.com", "Outboards, inboards, sterndrives, jet — digital or print"),
        ("Clymer", "https://www.clymer.com", "Similar coverage, often more readable"),
        ("BoatUS", "https://www.boatus.com", "Specialty manuals and guides"),
    ]),
    ("Boat builders", [
        ("Lund", "https://www.lundboats.com", ""), ("Alumacraft", "https://www.alumacraft.com", ""),
        ("Crestliner", "https://www.crestliner.com", ""), ("Tracker", "https://www.trackerboats.com", ""),
        ("Bayliner", "https://www.bayliner.com", ""), ("Sea Ray", "https://www.searay.com", ""),
        ("Bennington (pontoon)", "https://www.benningtonmarine.com", ""), ("Princecraft (pontoon)", "https://www.princecraft.com", ""),
    ]),
    ("Trailers", [
        ("ShoreLand'r", "https://www.shorelandr.com", ""), ("EZ Loader", "https://www.ezloader.com", ""),
        ("Karavan", "https://www.karavantrailers.com", ""), ("Load Rite", "https://www.loadrite.com", ""),
    ]),
    ("Electronics & safety", [
        ("Garmin", "https://support.garmin.com", "Incl. legacy units"),
        ("Lowrance / Simrad", "https://www.lowrance.com/support", ""),
        ("Raymarine", "https://www.raymarine.com/manuals", ""),
        ("Minn Kota", "https://www.minnkotamotors.com/support", "Trolling motors"),
        ("Standard Horizon (VHF)", "https://www.standardhorizon.com", ""),
        ("ACR (EPIRB/PLB)", "https://www.acrartex.com", ""),
        ("Mustang Survival (PFD)", "https://www.mustangsurvival.com", ""),
    ]),
]


def _manual_finder_body():
    cats = "".join(
        '<div class="mf-cat" data-cat="%s"><h2>%s</h2><ul class="pg-list">%s</ul></div>' % (
            esc(c), esc(c), "".join(
                '<li class="mf-item"><a href="%s" target="_blank" rel="noopener">%s</a>%s</li>' % (
                    u, esc(n), (" — " + esc(nt)) if nt else "")
                for n, u, nt in items)
        ) for c, items in _MANUAL_CATS)
    js = """<script>
(function () {
  var input = document.getElementById('mf-search');
  var items = document.querySelectorAll('#mf-list .mf-item');
  if (input) input.addEventListener('input', function () {
    var q = (input.value || '').toLowerCase();
    items.forEach(function (it) { it.style.display = it.textContent.toLowerCase().indexOf(q) === -1 ? 'none' : ''; });
  });
})();
</script>"""
    return (
        hero("Manual Finder", "Official manuals and parts sources, grouped by category. Find + link only — never hosted.")
        + '<section class="section section--light"><div class="container">'
        + '<label class="pg-hint-label" for="mf-search">Search manuals</label>'
        + '<input id="mf-search" class="fp-in" type="search" placeholder="e.g. Mercury, Garmin, Lund…" aria-label="Search manuals">'
        + '<div id="mf-list">' + cats + '</div>'
        + js
        + '</div></section>'
    )


register("tools/manual-finder", "AftLog Manual Finder — Official Manuals & Sources",
         "37 categorized links to OEM and public manual sources: engines, boats, trailers, electronics, and safety gear.",
         _manual_finder_body())


_DIY = [
    ("Replace the impeller", ["Remove the lower unit.", "Pull the old impeller and note the key orientation.", "Grease the new one lightly and install the same way.", "Reassemble — never run it dry."]),
    ("Small gelcoat chip repair", ["Sand the chip with 220 grit.", "Clean with acetone.", "Apply gelcoat paste and let it cure.", "Sand 400\u21921200 and polish to blend."]),
    ("Change lower-unit gear oil", ["Drain the lower unit (check for milky oil = water).", "Fill from the bottom vent until oil appears at the top.", "Replace washers and reinstall screws."]),
    ("Repack trailer bearings", ["Jack and remove the wheel.", "Pull the hub and bearings.", "Clean, inspect, repack with marine grease.", "Reinstall with proper torque."]),
    ("Install a bilge pump", ["Mount the pump in the lowest bilge point.", "Wire through a fuse to the battery (auto-float switch recommended).", "Route the hose above the waterline.", "Test with water."]),
    ("Fix a slow cranking battery setup", ["Clean terminals and check voltage (12.6 V+ charged).", "Test with a load.", "Check the charging system at speed.", "Consider a dual-battery switch."]),
    ("Winterize a small outboard", ["Run with stabilizer, then disconnect fuel.", "Fog the carb.", "Drain water, change lower-unit oil.", "Store upright with the battery on a maintainer."]),
    ("Deep-clean and condition vinyl seats", ["Vacuum and brush.", "Clean with vinyl-safe cleaner.", "Condition with UV protectant.", "Cover when not in use."]),
]


def _diy_body():
    cards = "".join(
        '<article class="cal-card"><h2>%s</h2><ol class="pg-list">%s</ol></article>' % (
            esc(t), "".join("<li>%s</li>" % esc(s) for s in steps))
        for t, steps in _DIY)
    body = (
        hero("DIY Library", "Clear, step-by-step repairs and maintenance you can do yourself — with gear you already have.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Starter guides. When in doubt, or for anything involving gas, high voltage, or lift points, see a marine professional.</p>'
        + '<div class="pg-card-grid">' + cards + '</div>'
        + '</div></section>'
    )
    return body


register("tools/diy-library", "AftLog DIY Library — Step-by-Step Repairs",
         "Eight beginner-friendly DIY guides: impeller, gelcoat, gear oil, trailer bearings, bilge pump, battery, winterizing an outboard, and vinyl care.",
         _diy_body())


_BATTERY_DEFAULTS = [
    ("Starting battery", "Installed — age unknown"),
    ("Trolling motor battery", "Not set up"),
    ("Trolling motor", "Not set up"),
    ("Transducer / fish finder", "Not set up"),
    ("Charger", "Not set up"),
    ("Battery switch", "Not set up"),
]


def _battery_body():
    defaults = json.dumps(_BATTERY_DEFAULTS)
    js = (r"""<script>
(function () {
  var KEY = 'aftlog_battery_gear';
  var DEFAULTS = __DEFAULTS__;
  function load(){ try { return JSON.parse(localStorage.getItem(KEY) || 'null') || JSON.parse(JSON.stringify(DEFAULTS)); } catch(e){ return JSON.parse(JSON.stringify(DEFAULTS)); } }
  function save(g){ try { localStorage.setItem(KEY, JSON.stringify(g)); } catch(e){} }
  var box = document.getElementById('bt-list');
  function render(){
    var g = load();
    box.innerHTML = '';
    g.forEach(function (it, i) {
      var row = document.createElement('div'); row.className = 'bt-item';
      row.innerHTML = '<div><strong>' + String(it[0]) + '</strong><div class="pg-muted">' + String(it[1]) + '</div></div>'
        + '<div><button type="button" class="btn btn-sm btn-secondary" onclick="btEdit(' + i + ')">Edit</button> '
        + '<button type="button" class="btn btn-sm btn-secondary" onclick="btRemove(' + i + ')">&times;</button></div>';
      box.appendChild(row);
    });
    window.btGear = g;
  }
  window.btEdit = function (i) {
    var g = load(); var name = g[i][0];
    var health = prompt('Health / notes for ' + name, g[i][1]);
    if (health !== null) { g[i][1] = health; save(g); render(); }
  };
  window.btRemove = function (i) { var g = load(); g.splice(i,1); save(g); render(); };
  window.btAdd = function () {
    var g = load(); var name = prompt('Equipment name', '');
    if (name && name.trim()) { g.push([name.trim(), 'Not set up']); save(g); render(); }
  };
  render();
})();
</script>""").replace("__DEFAULTS__", defaults)
    return (
        hero("Battery & Electronics", "Track the gear that keeps your boat alive — and size your wiring so it never dies at the dock.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">"Battery dying" is one of the most-searched boat problems. Track what you have, when it was bought, and its health here — saved in this browser.</p>'
        + '<div id="bt-list" class="pg-card-grid"></div>'
        + '<p><button type="button" class="btn btn-secondary" onclick="btAdd()">+ Add equipment</button></p>'
        + '<hr class="pg-hr">'
        + '<h2>Voltage drop & cable sizing</h2>'
        + '<p class="pg-muted">Long, undersized runs lose voltage. Keep the drop under 3\u0025 for critical gear. Estimate it with the app\u2019s calculator, then size up a gauge if needed.</p>'
        + '<p><a class="btn btn-primary" href="/tools/calculators.html#cal-5">Open the voltage drop calculator</a></p>'
        + js
        + '</div></section>'
        + section("Battery life", "<p>Most marine batteries last 4\u20135 years. Write the install date on the battery and log it here — age is the \u21161 cause of \u201cdies at the dock\u201d.</p>")
    )


register("tools/battery-electronics", "AftLog Battery & Electronics Tracker",
         "Track your boat's batteries and electronics, size wiring with the voltage drop calculator, and know when age kills a battery.",
         _battery_body())


_GLOSSARY = [
    ("Impeller", "The small rubber pump that moves cooling water through an outboard. Weak tell-tale usually means it's worn.", "The rubber water pump that pushes cooling water through the engine. If the \u201cpee stream\u201d (tell-tale) is weak, it's often the impeller. Replace every ~3 years or sooner if overheating."),
    ("Lower unit", "The bottom gearcase of an outboard. Check its oil for milkiness (water) or metal flakes.", "The gearcase at the bottom of an outboard. Holds the gears and the drive shaft; contains gear oil that should be checked for a milky look (water intrusion)."),
    ("Bellows", "Rubber boots on a sterndrive that keep water out. Cracked bellows can sink a boat.", "The rubber accordion boots on a sterndrive that keep water out and grease in around the drive shaft and shift cable. Cracked bellows = sinking risk."),
    ("Gimbal bearing", "A key bearing on a sterndrive that allows the drive to pivot. Water damage causes stiff steering.", "The bearing at the transom where a sterndrive pivots. Gets water-damaged if not greased; hard steering is a symptom."),
    ("Anode", "A metal piece that corrodes on purpose to protect your engine or outdrive from corrosion.", "A sacrificial zinc (or magnesium/aluminum) bolt that corrodes instead of your outdrive. If half eaten, it's doing its job."),
    ("Tell-tale", "The cooling-water stream from an outboard. Weak or no stream means pump trouble.", "The small \u201cpee hole\u201d stream of cooling water from an outboard. No stream = water pump problem."),
    ("Transom", "The back wall of the boat where the engine mounts. Soft spots mean rot.", "The flat back of the boat the engine bolts to. Soft spots here mean rot — a major buying warning sign."),
    ("Stringers", "Structural beams inside the hull. Rot leads to soft floors and major repairs.", "The internal framing that stiffens the hull. Rot here shows as soft floors."),
    ("Winterize", "Protecting the boat for winter by draining water, treating fuel, and prepping the engine.", "Preparing the boat for freezing: drain water, fog the engine, stabilize fuel, remove the battery. Skipping it can crack the engine block."),
    ("Commissioning", "Spring startup: charge battery, check impeller, inspect fuel, and run on muffs.", "Waking the boat up in spring: unwrap, charge the battery, check the impeller and fuel, first fire-up on muffs."),
    ("Porpoising", "The bow oscillates up and down at speed. Usually caused by trim or engine height.", "The bow bouncing up and down on plane. Usually trim or motor-height related."),
    ("Prop slip", "How much the prop loses grip in the water. Higher slip = less efficiency.", "The difference between theoretical and actual propeller speed — how efficiently the prop bites the water."),
    ("Bilge", "The lowest part of the boat where water collects. The bilge pump removes it.", "The lowest inside part of the hull where water collects; the bilge pump removes it."),
    ("Muffs", "Rubber cups that feed water to an outboard for running it on land.", "The clamp-on ear muffs that feed water to an outboard's cooling system while running it on land."),
    ("Float plan", "A note telling someone your route and return time. Huge safety benefit.", "Who you tell where you're going and when you'll be back — the single best safety habit."),
    ("Gear lube", "Oil inside the lower unit. Milky means water; metal means wear.", "The oil in the lower unit. Milky = water got in. Metal flakes = gears are wearing. Both are bad signs when buying."),
    ("HIN", "The boat's 12-digit serial number. Must match registration.", "Hull Identification Number — the boat's 12-character serial, like a VIN. Found on the transom; verify it matches the registration."),
    ("Osmosis", "Water blisters under the gelcoat. Cosmetic or structural depending on depth.", "Blisters under the gelcoat from water absorbed into the hull. Common on older fiberglass — can be cosmetic or serious."),
    ("Skeg", "The fin under the prop. Damage usually means an impact.", "The fin below the propeller that protects the prop and helps steering. Bent or broken = a past impact."),
    ("Rub rail", "The bumper strip around the hull. Damage shows docking impacts.", "The rubber/plastic bumper strip around the hull's top edge. Separated or cracked = dock or impact history."),
    ("Splashwell", "A recessed area near the outboard that helps keep water out.", "The recessed area at the back of the boat around the outboard that keeps following water out."),
    ("Primer bulb", "A rubber bulb that primes fuel to the engine. Should feel firm.", "The squeezable rubber bulb in the fuel line used to prime the engine. Should feel firm; soft or cracked = suspect."),
    ("Water-separating filter", "A fuel filter that removes water. Replace yearly.", "The fuel filter that catches water before it reaches the engine. Dirty = poor fuel maintenance."),
    ("Livewell", "A tank with pumps to keep fish alive.", "The tank that keeps caught fish alive — has its own pumps and plumbing."),
    ("Compression test", "A test of cylinder pressure. Big differences mean engine issues.", "Measures each cylinder's pressure; all should be within 10% of each other. A big difference = expensive engine trouble."),
    ("Keel", "The centerline ridge on the bottom of the hull. Often scraped or worn.", "The bottom ridge of the hull that takes damage when the boat is beached."),
    ("Chines", "The edges where the hull bottom meets the sides. Important for stability.", "The hull edges where the bottom meets the sides."),
    ("Freeboard", "How tall the boat's sides are above the water. More freeboard = safer in waves.", "The height of the hull side above the waterline."),
    ("Gunwale", "The top edge of the boat's sides. Often used as a handhold.", "The top edge or rail of the hull sides."),
    ("Trim tab", "A small plate that helps keep the boat level.", "Adjustable plates on the hull or outdrive that correct listing and optimize running attitude."),
    ("Cavitation", "Air bubbles around the prop that cause vibration and lost power.", "The collapse of vapor bubbles around the propeller blades, causing vibration and thrust loss."),
    ("Planing", "When the boat rises and skims on top of the water.", "The hydrodynamic state where the hull rises and rides on top of the water, reducing drag."),
    ("Draft", "How deep the boat sits in the water.", "The vertical distance between the waterline and the lowest point of the hull or drive."),
    ("Beam", "The width of the boat at its widest point.", "The maximum width of the vessel, influencing stability and interior volume."),
    ("Deadrise", "How V-shaped the hull is — deeper V = smoother ride.", "The angle between the hull bottom and a horizontal plane; higher angles improve rough-water performance."),
    ("Chine walk", "A side-to-side wobble at high speed.", "Instability at high speed where the hull oscillates between chines due to trim or weight imbalance."),
    ("LOA (Length Overall)", "The boat's full length from front to back.", "Total vessel length including appendages such as swim platforms and bow pulpits."),
    ("LWL (Waterline Length)", "How much of the boat sits in the water.", "The length of the hull at the waterline, affecting hull speed and stability."),
    ("Trim angle", "How high or low the motor is tilted.", "The angular position of the outboard or sterndrive relative to the transom, affecting lift and efficiency."),
    ("Heel", "When the boat leans to one side.", "Temporary lateral inclination caused by wind, waves, or turning forces."),
    ("List", "A steady lean caused by uneven weight.", "Persistent lateral inclination caused by uneven weight distribution."),
    ("Pitch", "The bow moving up and down.", "Longitudinal motion of the bow and stern in waves."),
    ("Yaw", "The bow swinging left and right.", "Rotational motion of the bow swinging port-starboard around the vertical axis."),
    ("Roll", "Side-to-side rocking.", "Side-to-side rotational motion around the vessel's longitudinal axis."),
    ("Scupper", "Deck drains that let water flow out.", "Deck drainage openings that discharge water overboard; essential for self-bailing systems."),
    ("Self-bailing cockpit", "A cockpit that drains water overboard instead of into the bilge.", "A cockpit designed to drain water via scuppers without relying on bilge pumps."),
    ("Hull speed", "The fastest a displacement hull can go efficiently.", "The theoretical maximum efficient speed of a displacement hull, based on waterline length."),
    ("Displacement hull", "A hull that pushes through the water instead of riding on top.", "A hull form that moves through the water without planing, prioritizing stability over speed."),
    ("Planing hull", "A hull that lifts and skims on top of the water.", "A hull designed to generate lift and ride above the water at higher speeds."),
    ("Ventilation (prop)", "When air reaches the prop and causes a sudden loss of thrust.", "Ingress of air to the propeller blades, causing RPM flare and loss of bite."),
    ("Following seas", "Waves coming from behind the boat.", "Sea conditions where waves approach from astern, affecting steering and stability."),
    ("Quartering seas", "Waves hitting the boat at an angle.", "Waves approaching at an oblique angle, influencing yaw and roll behavior."),
    ("Backing down (anchoring)", "Reversing gently to set the anchor.", "Applying reverse thrust to set the anchor firmly into the seabed."),
    ("Transom angle", "The angle of the back of the boat where the engine mounts.", "The geometric angle of the transom, influencing engine mounting height and trim range."),
    ("Keel guard", "A strip that protects the keel from scrapes.", "A sacrificial protective strip installed on the keel to prevent abrasion during beaching or loading."),
    ("Fairlead", "A guide that keeps a rope or anchor line from rubbing.", "A roller or guide that directs a line to prevent chafe and maintain proper lead angle."),
]


def _glossary_body():
    items = "".join(
        '<article class="pg-blog-card" data-term="%s"><h3>%s</h3><p class="pg-muted"><strong>Plain talk:</strong> %s</p><p class="pg-muted"><strong>For the pro:</strong> %s</p></article>' % (
            esc(t.lower()), esc(t), esc(b), esc(p))
        for t, b, p in _GLOSSARY)
    js = """<script>
(function () {
  var input = document.getElementById('gl-search');
  var cards = document.querySelectorAll('#gl-grid .pg-blog-card');
  if (input) input.addEventListener('input', function () {
    var q = (input.value || '').toLowerCase();
    cards.forEach(function (c) { c.style.display = (c.dataset.term || '').indexOf(q) === -1 ? 'none' : ''; });
  });
})();
</script>"""
    return (
        hero("Glossary", "Boat terms in plain talk — and the technical version for when it matters.")
        + '<section class="section section--light"><div class="container">'
        + '<label class="pg-hint-label" for="gl-search">Search boating terms</label>'
        + '<input id="gl-search" class="fp-in" type="search" placeholder="e.g. impeller, bilge, transom…" aria-label="Search glossary">'
        + '<div class="pg-card-grid" id="gl-grid">' + items + '</div>'
        + js
        + '</div></section>'
    )


register("tools/glossary", "AftLog Glossary — Boating Terms, Plainly Explained",
         "56 boat terms in plain talk plus the technical definition — impeller, bilge, transom, HIN, and more.",
         _glossary_body())


# ── STEP 7.1: Emergency Advisor ────────────────────────────────────────

_EMERGENCY_SCENARIOS = [
    ("Engine won't start", "#F5B041", [
        "Check the kill-switch lanyard is clipped on — it is the #1 cause.",
        "Is the fuel tank vent open? (Vapor-locked tanks won't prime.)",
        "Check the battery: dash lights on? Try the horn. No power = battery/connection.",
        "Press the primer bulb until firm, then try again — but not for more than 10 seconds at a time.",
        "If it cranks but won't fire: check the fuel filter for water (milky = water).",
        "Still no start after these: do NOT keep cranking (starter + battery damage). Call a mechanic.",
    ]),
    ("Boat is taking on water", "#E02020", [
        "PUT ON LIFE JACKETS FIRST. Tell everyone to stay calm and stay in the boat.",
        "Find the leak: bilge pump ON, check the drain plug is in and tight.",
        "If the plug is the problem, you can wedge it from outside with a rag if safe.",
        "If a hose split or bellows failed: clamp or pinch it shut if you can reach it safely.",
        "Slow a small leak by stuffing a rag, towel, or fender into the opening.",
        "Call for help NOW if water is rising faster than the bilge pump clears it. Share your position (above) with the rescue service.",
    ]),
    ("Overheating", "#E02020", [
        "Reduce throttle to idle immediately — do not shut off unless told to.",
        "Check the water intake is not blocked by weeds, a plastic bag, or mud (tilt up and clear it).",
        "Is the tell-tale stream weak or gone? Likely a blocked or worn impeller.",
        "If it cools at idle, run slowly to the nearest dock, watching the gauge.",
        "Never run hot at full throttle — a blown head gasket or warped head is a $1000+ bill.",
        "If the alarm keeps sounding, shut down, drop anchor, and call a mechanic or tow.",
    ]),
    ("Electrical failure", "#F5B041", [
        "Turn OFF the battery switch if there is one. Check for burning smell — if present, isolate power.",
        "Check battery connections: loose or corroded terminals cause most failures. Tighten/tap with a tool.",
        "Check the main fuse/breaker on the engine and panel. Spare fuses live in the onboard kit.",
        "Smell or see smoke? Shut everything down, get everyone clear, and call for help.",
        "If only some things work (lights but no start), it's a connection or ground issue — not the battery.",
        "On the water with no power: anchor, use a radio/phone, and wait for help. Don't swim for the ramp.",
    ]),
    ("Lost in fog", "#F5B041", [
        "Slow to a safe idle and STAY PUT if you can't see. Moving blind is how boats collide.",
        "Turn on navigation lights and a spotlight if dusk or dark.",
        "Sound the horn: 5 short blasts in fog signals \u201cI'm here — I can't see you\u201d.",
        "Open your maps/phone and confirm your position before moving at all.",
        "Listen for waves breaking on shore, other engines, or a ramp to orient yourself.",
        "If you truly don't know where you are, call the coast guard or a local marina and share your position (above).",
    ]),
    ("Prop damage", "#F5B041", [
        "Reduce throttle to idle immediately — a bent prop vibrates and can damage the drive.",
        "Check for vibration or a knocking sound from the lower unit.",
        "If you hit something: inspect the prop, skeg, and check for water entering the bilge.",
        "A small ding can wait; a badly bent blade means run slow or get towed.",
        "Do NOT run hard on a damaged prop — it strains the driveshaft and bearings.",
        "Note the damage (photo) and call a prop shop or mobile mechanic. Many props can be repaired, not replaced.",
    ]),
    ("Lost GPS", "#F5B041", [
        "Stay calm and stop if you can — moving blind makes it worse.",
        "You are not truly lost: the boat still floats, and you know roughly where you launched.",
        "Use the old tools: compass heading, landmarks, depth sounder, and your float plan (who knows where you went).",
        "Dead-reckon from your last known position — check the time and speed since then.",
        "If you have a VHF radio, call the coast guard or marina and give your best estimate; use your phone's offline maps if available.",
        "Only call for help if conditions or fuel are unsafe — otherwise head back the way you came, slowly.",
    ]),
    ("Smoke from engine", "#E02020", [
        "Shut the engine down immediately and get everyone away from the engine compartment.",
        "DO NOT open the engine hatch right away — a sudden rush of air can flash a fire. Wait a few minutes.",
        "If you can see flames, use the extinguisher ONLY from a safe position, aimed at the base of the fire.",
        "Electrical smoke smells sharp and acrid; fuel/oil smoke smells heavy — note which, it helps the mechanic.",
        "Get life jackets on and call for help now if there is any flame or heavy smoke — share your position (above).",
        "Never restart after smoke until the cause is found and the engine room has been aired out.",
    ]),
]


_EMERGENCY_JS = r"""<script>
(function () {
  var acc = document.querySelector('details.em-card'); if (acc) acc.open = true;
  var lat = null, lon = null, t = null;
  var btn = document.getElementById('em-locate');
  var err = document.getElementById('em-loc-error');
  var coord = document.getElementById('em-coord');
  var updated = document.getElementById('em-updated');
  var panel = document.getElementById('em-pos');
  var cbtn = document.getElementById('em-copy');
  var mbtn = document.getElementById('em-maps');
  function setPos(){
    if (!lat) return;
    coord.textContent = lat.toFixed(6) + ', ' + lon.toFixed(6);
    updated.textContent = 'Updated ' + (t ? 'just now' : '');
    panel.style.display = '';
    btn.parentNode.style.display = 'none';
    err.textContent = '';
  }
  function onErr(e){
    err.textContent = e && e.code === 1
      ? 'Location permission is off. Allow location to share your position — or open your maps app.'
      : 'Could not get your position. Try again.';
  }
  btn.addEventListener('click', function () {
    btn.disabled = true; btn.textContent = 'Getting position…';
    if (!navigator.geolocation) { onErr(null); btn.disabled = false; btn.textContent = 'Get my position'; return; }
    navigator.geolocation.getCurrentPosition(function (p) {
      lat = p.coords.latitude; lon = p.coords.longitude; t = Date.now();
      setPos(); btn.disabled = false; btn.textContent = 'Get my position';
    }, function (e) { onErr(e); btn.disabled = false; btn.textContent = 'Get my position'; }, { enableHighAccuracy: true, timeout: 12000 });
  });
  cbtn.addEventListener('click', function () {
    if (!lat) return;
    var txt = lat.toFixed(6) + ', ' + lon.toFixed(6);
    if (navigator.clipboard) { navigator.clipboard.writeText(txt); }
    coord.textContent = txt + '  \u2713 copied';
  });
  mbtn.addEventListener('click', function () {
    if (lat) window.open('https://maps.google.com/?q=' + lat + ',' + lon, '_blank', 'noopener');
  });
  var ctl = document.getElementById('em-contact');
  var KS = 'aftlog_emer_contact';
  try { ctl.value = localStorage.getItem(KS) || ''; } catch(e){}
  ctl.addEventListener('input', function () { try { localStorage.setItem(KS, ctl.value); } catch(e){} });
  var call = document.getElementById('em-call');
  function refreshCall(){
    var n = (ctl.value || '').replace(/[^0-9+]/g, '');
    if (n) { call.href = 'tel:' + n; call.style.display = ''; } else { call.style.display = 'none'; }
  }
  ctl.addEventListener('input', refreshCall); refreshCall();
})();
</script>"""


def _emergency_body():
    cards = "".join(
        '<details class="em-card" style="--em:%s"><summary>%s</summary><ol class="pg-list">%s</ol></details>' % (
            color, esc(title), "".join("<li>%s</li>" % esc(s) for s in steps))
        for title, color, steps in _EMERGENCY_SCENARIOS)
    return (
        hero("Emergency — What to do if…", "One tap gets calm, step-by-step guidance — with your exact position ready to share with help.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Stay calm. Read the first step, then the next. Only call for help when a step says so.</p>'
        + '<article class="cal-card pg-em-pos"><h2>Your exact position</h2>'
        + '<p class="pg-muted">If you need to tell someone exactly where you are, grab your position.</p>'
        + '<button type="button" id="em-locate" class="btn btn-primary">Get my position</button>'
        + '<p class="pg-muted pg-em-coord" id="em-coord" style="font-weight:700"></p>'
        + '<p class="pg-muted" id="em-updated"></p>'
        + '<div id="em-pos" style="display:none">'
        + '<button type="button" id="em-copy" class="btn btn-secondary btn-sm">Copy coordinates</button> '
        + '<button type="button" id="em-maps" class="btn btn-secondary btn-sm">Open in Maps</button>'
        + '</div>'
        + '<p class="pg-em-err" id="em-loc-error" style="color:#E02020"></p>'
        + '</article>'
        + '<article class="cal-card pg-em-contact"><h2>Call emergency contact</h2>'
        + '<p class="pg-muted">Keep a contact you trust who knows your plans and your boat.</p>'
        + '<label class="pg-hint-label" for="em-contact">Emergency contact number</label>'
        + '<input id="em-contact" class="fp-in" type="tel" placeholder="+1 555 123 4567">'
        + '<p><a id="em-call" class="btn btn-primary" href="#" style="display:none">Call contact</a></p>'
        + '</article>'
        + cards
        + _EMERGENCY_JS
        + '</div></section>'
        + section("When to call for help", "<p>Call the coast guard, marina, or tow service as soon as the situation is beyond a quick fix — while you still have time, fuel, and daylight. It is always easier to cancel a rescue than to start one too late.</p>")
    )


register("tools/emergency", "AftLog Emergency — What to Do If…",
         "Calm, step-by-step emergency guidance for the water: engine won't start, taking on water, overheating, electrical failure, fog, prop damage, lost GPS, and smoke.",
         _emergency_body())


# ── STEP 6.1–6.4: Trip + Fuel log (fuel-cycle brain) ──────────────────

_TRIP_JS = r"""<script>
(function () {
  var KS = 'aftlog_triplog';
  // Storage is always METRIC (km, L, hrs). Display converts by unit.
  var state = { tank: 30, trips: [], fills: [] };
  try { var s = JSON.parse(localStorage.getItem(KS) || 'null'); if (s) state = Object.assign({ tank: 30, trips: [], fills: [] }, s); } catch(e){}
  function save(){ try { localStorage.setItem(KS, JSON.stringify(state)); } catch(e){} }
  var _u = 'metric';
  var uBtn = document.getElementById('tl-unit');
  function kmD(km){ return _u==='metric' ? km : km/1.60934; }   // metric km -> display
  function lD(L){ return _u==='metric' ? L : L/3.78541; }        // metric L -> display
  var watch = null; var gps = {running:false, last:null, km:0, sec:0, timer:null};
  var gpsBtn = document.getElementById('tl-gps');
  var gpsStatus = document.getElementById('tl-gps-status');
  function haversine(a,b){ var R=6371, dLon=(b.lng-a.lng)*Math.PI/180, dLat=(b.lat-a.lat)*Math.PI/180; var x=Math.sin(dLat/2)*Math.sin(dLat/2)+Math.cos(a.lat*Math.PI/180)*Math.cos(b.lat*Math.PI/180)*Math.sin(dLon/2)*Math.sin(dLon/2); return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x)); }
  function startGps(){
    if (!navigator.geolocation) { gpsStatus.textContent = 'Geolocation not available — use the manual entry instead.'; return; }
    gps = {running:true, last:null, km:0, sec:0, timer:null};
    gpsBtn.textContent = 'Stop & save trip'; gpsBtn.className = 'btn btn-secondary';
    gpsStatus.textContent = 'Tracking…';
    gps.timer = setInterval(function(){
      gps.sec += 1;
      gpsStatus.textContent = 'Tracking… ' + kmD(gps.km).toFixed(1) + ' ' + (_u==='metric'?'km':'mi') + ' · ' + (gps.sec/60).toFixed(1) + ' min';
    }, 1000);
    watch = navigator.geolocation.watchPosition(function (p) {
      if (p.coords.accuracy > 60) return; // drop noisy fixes
      if (gps.last) gps.km += haversine(gps.last, p.coords);
      gps.last = p.coords;
    }, function(){ gpsStatus.textContent = 'Location error — use manual entry.'; }, { enableHighAccuracy:true, maximumAge:5000 });
  }
  function stopGps(){
    if (watch !== null) navigator.geolocation.clearWatch(watch);
    if (gps.timer) clearInterval(gps.timer);
    var hrs = gps.sec/3600;
    state.trips.push({ km: gps.km, hrs: hrs, ts: Date.now(), src:'GPS' });
    save(); renderTrips(); compute();
    var saved = kmD(gps.km).toFixed(1) + ' ' + (_u==='metric'?'km':'mi');
    gps = {running:false};
    gpsBtn.textContent = 'Start GPS trip'; gpsBtn.className = 'btn btn-primary';
    gpsStatus.textContent = 'Trip saved (' + saved + ').';
  }
  window.tlGps = function () { if (gps.running) stopGps(); else startGps(); };
  window.tlAddTrip = function () {
    var dist = parseFloat(document.getElementById('tl-dist').value || '');
    var mins = parseFloat(document.getElementById('tl-mins').value || '');
    var unit = document.getElementById('tl-unit-in').value;
    if (!(dist>0) || !(mins>0)) { alert('Enter a distance and a time.'); return; }
    var km = unit==='mi' ? dist*1.60934 : dist;
    state.trips.push({ km: km, hrs: mins/60, ts: Date.now(), src:'Manual' });
    document.getElementById('tl-dist').value=''; document.getElementById('tl-mins').value='';
    save(); renderTrips(); compute();
  };
  window.tlAddFill = function () {
    var v = parseFloat(document.getElementById('tl-litres').value || '');
    var unit = document.getElementById('tl-unit-in2').value;
    var cost = parseFloat(document.getElementById('tl-cost').value || '');
    if (!(v>0)) { alert('Enter how much fuel you added.'); return; }
    var L = unit==='gal' ? v*3.78541 : v;
    state.fills.push({ L: L, cost: isNaN(cost)?null:cost, ts: Date.now() });
    document.getElementById('tl-litres').value=''; document.getElementById('tl-cost').value='';
    save(); renderFills(); compute();
  };
  window.tlSetTank = function () { var v=parseFloat(document.getElementById('tl-tank').value||''); if(!(v>0)) return; state.tank = _u==='metric' ? v : v*3.78541; save(); compute(); };
  window.tlClear = function () { if(!confirm('Clear all trips and fills on this device?')) return; state.trips=[]; state.fills=[]; save(); renderTrips(); renderFills(); compute(); };
  window.tlUnit = function () { _u = _u==='metric' ? 'imperial' : 'metric'; uBtn.textContent = (_u==='metric'?'Switch to imperial':'Switch to metric'); paintUnits(); renderTrips(); renderFills(); compute(); };
  function paintUnits(){
    document.getElementById('tl-lab-dist').textContent = 'Distance ('+(_u==='metric'?'km':'mi')+')';
    document.getElementById('tl-lab-fuel').textContent = 'Fuel added ('+(_u==='metric'?'L':'US gal')+')';
    document.getElementById('tl-unit-in').value = _u==='metric' ? 'km' : 'mi';
    document.getElementById('tl-unit-in2').value = _u==='metric' ? 'L' : 'gal';
    document.getElementById('tl-tank').value = Math.round(lD(state.tank));
  }
  function fmtD(km){ return kmD(km).toFixed(1) + ' ' + (_u==='metric'?'km':'mi'); }
  function fmtL(L){ return lD(L).toFixed(1) + ' ' + (_u==='metric'?'L':'US gal'); }
  function renderTrips(){ var el=document.getElementById('tl-trips'); el.innerHTML = state.trips.slice().reverse().map(function(t){ return '<div class="tl-row">'+new Date(t.ts).toLocaleDateString()+' · '+fmtD(t.km)+' · '+(t.hrs*60).toFixed(0)+' min'+(t.src==='GPS'?' · GPS':'')+'</div>'; }).join('') || '<p class="pg-muted">No trips yet.</p>'; }
  function renderFills(){ var el=document.getElementById('tl-fills'); el.innerHTML = state.fills.slice().reverse().map(function(f){ return '<div class="tl-row">'+new Date(f.ts).toLocaleDateString()+' · '+fmtL(f.L)+(f.cost?' · $'+f.cost.toFixed(2):'')+'</div>'; }).join('') || '<p class="pg-muted">No fill-ups yet.</p>'; }
  // Per-cycle efficiency mirroring log_service.efficiencyKmPerL: for each
  // fill, distance travelled since it (until the next fill); average the last
  // up-to-3 cycles with distance. Falls back to overall km/L if no cycles.
  function efficiencyKmPerL(){
    var fl = state.fills.filter(function(f){ return f.L>0; }).slice().sort(function(a,b){ return a.ts-b.ts; });
    if (!fl.length) return 0;
    var effs = [];
    for (var i=0;i<fl.length;i++){
      var start = fl[i].ts;
      var d = (i < fl.length-1)
        ? state.trips.reduce(function(a,t){ return (t.ts>start && t.ts<=fl[i+1].ts) ? a+t.km : a; }, 0)
        : state.trips.reduce(function(a,t){ return t.ts>start ? a+t.km : a; }, 0);
      if (d>0) effs.push(d / fl[i].L);
    }
    if (!effs.length) return 0;
    var recent = effs.slice(Math.max(0, effs.length-3));
    return recent.reduce(function(a,b){return a+b;},0) / recent.length;
  }
  function compute(){
    var km = state.trips.reduce(function(a,t){return a+t.km;},0);
    var hrs = state.trips.reduce(function(a,t){return a+t.hrs;},0);
    var fuel = state.fills.reduce(function(a,f){return a+f.L;},0);
    var eff = efficiencyKmPerL();
    if (!(eff>0)) eff = (km>0 && fuel>0) ? km/fuel : 0;   // otherwise, overall km/L
    var spd = hrs>0 ? km/hrs : 0;               // km/hr
    var lph = hrs>0 ? fuel/hrs : 0;             // L/hr
    var tank = state.tank || 30;
    var kmEmpty = eff>0 ? Math.max(0,(tank-fuel)*eff) : null;
    var hrEmpty = (kmEmpty!==null && spd>0) ? kmEmpty/spd : null;
    setTxt('tl-kml', eff>0 ? (_u==='metric' ? eff.toFixed(2)+' km/L' : (eff*0.4251).toFixed(1)+' MPG') : '—');
    setTxt('tl-kph', spd>0 ? (_u==='metric' ? spd.toFixed(1)+' km/hr' : (spd*0.621371).toFixed(1)+' mph') : '—');
    setTxt('tl-lph', lph>0 ? (_u==='metric' ? lph.toFixed(1)+' L/hr' : lD(lph).toFixed(1)+' gal/hr') : '—');
    setTxt('tl-empty', kmEmpty!==null ? kmD(kmEmpty).toFixed(0)+' '+(_u==='metric'?'km':'mi') : '—');
    setTxt('tl-emptyhr', hrEmpty!==null ? hrEmpty.toFixed(1)+' hrs' : '—');
    var warn = document.getElementById('tl-warn');
    if (kmEmpty!==null && kmEmpty < 0.2*tank) { warn.textContent = 'LOW — roughly '+kmD(kmEmpty).toFixed(0)+' '+(_u==='metric'?'km':'mi')+' to empty. Fill up soon.'; warn.className='tl-warn on'; }
    else { warn.textContent=''; warn.className='tl-warn'; }
  }
  function setTxt(id, v){ var el=document.getElementById(id); if(el) el.textContent=v; }
  uBtn.addEventListener('click', tlUnit);
  paintUnits(); renderTrips(); renderFills(); compute();
})();
</script>"""


def _trip_log_body():
    return (
        hero("Trip & Fuel Log", "Log trips and fill-ups and AftLog learns your real fuel range — how far, how fast, and how many km/hours you have left.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Track a trip by GPS or enter it manually, log your fill-ups, set your tank size, and see your learned efficiency plus \u201cX km / Y hrs to empty\u201d.</p>'
        + '<button type="button" class="btn btn-sm btn-secondary" id="tl-unit">Switch to imperial</button>'
        + '<div class="tl-grid">'
        + '<div class="tl-card"><h2>Track a trip</h2>'
        + '<p><button type="button" class="btn btn-primary" id="tl-gps" onclick="tlGps()">Start GPS trip</button></p>'
        + '<p class="pg-muted" id="tl-gps-status"></p>'
        + '<hr class="pg-hr"><p class="pg-muted">Or manual entry:</p>'
        + '<label class="pg-hint-label" id="tl-lab-dist" for="tl-dist">Distance</label>'
        + '<div class="tl-inline"><input id="tl-dist" class="fp-in" type="number" min="0" step="0.1" placeholder="10"><select id="tl-unit-in" class="pg-select"><option value="km">km</option><option value="mi">mi</option></select></div>'
        + '<label class="pg-hint-label" for="tl-mins">Time (minutes)</label><input id="tl-mins" class="fp-in" type="number" min="1" placeholder="45">'
        + '<p><button type="button" class="btn btn-primary" onclick="tlAddTrip()">+ Add trip</button></p>'
        + '</div>'
        + '<div class="tl-card"><h2>Log a fill-up</h2>'
        + '<label class="pg-hint-label" id="tl-lab-fuel" for="tl-litres">Fuel added</label>'
        + '<div class="tl-inline"><input id="tl-litres" class="fp-in" type="number" min="0" step="0.1"><select id="tl-unit-in2" class="pg-select"><option value="L">L</option><option value="gal">US gal</option></select></div>'
        + '<label class="pg-hint-label" for="tl-cost">Cost ($, optional)</label><input id="tl-cost" class="fp-in" type="number" min="0" step="0.01">'
        + '<p><button type="button" class="btn btn-primary" onclick="tlAddFill()">+ Add fill-up</button></p>'
        + '</div>'
        + '</div>'
        + '<div class="tl-yours">'
        + '<h2>Your numbers</h2>'
        + '<div class="tl-stats">'
        + '<div class="tl-stat"><div id="tl-kml">—</div><span>Efficiency</span></div>'
        + '<div class="tl-stat"><div id="tl-kph">—</div><span>Avg speed</span></div>'
        + '<div class="tl-stat"><div id="tl-lph">—</div><span>Fuel burn</span></div>'
        + '<div class="tl-stat"><div id="tl-empty">—</div><span>To empty</span></div>'
        + '<div class="tl-stat"><div id="tl-emptyhr">—</div><span>…in hours</span></div>'
        + '</div>'
        + '<div class="tl-tank-row"><label class="pg-hint-label" for="tl-tank">Tank size:</label><input id="tl-tank" class="fp-in" type="number" min="1" value="30" style="max-width:110px"><button type="button" class="btn btn-sm btn-secondary" onclick="tlSetTank()">Set</button></div>'
        + '<div class="tl-warn" id="tl-warn"></div>'
        + '</div>'
        + '<div class="tl-history"><h2>Trips</h2><div id="tl-trips"></div><h2>Fill-ups</h2><div id="tl-fills"></div>'
        + '<p><button type="button" class="btn btn-sm btn-secondary" onclick="tlClear()">Clear all data</button></p></div>'
        + '<p class="pg-muted">For deeper seasonal analysis (monthly trends, outliers), see the <a href="/tools/trip-patterns.html">Trip Patterns</a> tool.</p>'
        + '<div class="pg-sidecard ms-promo"><div class="pg-sidecard-head">Marine Suite</div>'
        + '<p class="pg-muted" style="margin:0 0 8px">Logging a trip? CatchTales can track the fishing side — species, spots, and conditions.</p>'
        + '<a class="btn btn-secondary btn-sm" href="/catchtales.html">Explore CatchTales</a></div>'
        + _TRIP_JS
        + '</div></section>'
    )


register("tools/trip-log", "AftLog Trip & Fuel Log",
         "Log trips by GPS or manually, track fill-ups, and see your learned fuel range: km/L, avg speed, fuel burn, and km/hours to empty.",
         _trip_log_body())


# ── STEP 6.5–6.8: Checklists tool ─────────────────────────────────────

_CHKL_TEMPLATES = [
    ("launch", "Launch", ["Bilge plug is in and tight", "Key in / lanyard clipped on", "Safety gear aboard (PFDs, extinguisher, horn)", "Fuel — enough for the trip, vent open", "Engine trimmed for launch", "Cast-off lines clear", "Everyone has a fitted lifejacket", "Throttle / gear in neutral"]),
    ("retrieve", "Retrieve", ["Approach the ramp slow", "Kill the engine in neutral", "Tilt / trim the engine up", "Pull the bilge plug at the ramp", "Tie down the boat to the trailer", "Take gear off and stow", "Flush the engine (freshwater) if used in salt", "Cover the boat"]),
    ("towing", "Towing", ["Safety chains crossed under the coupler", "Coupler locked to the ball — verify the pin", "Trailer lights working", "Breakaway lanyard connected", "Tires at correct pressure + spare onboard", "Load balanced on the trailer (10% tongue)", "Straps and winch secured", "Boat plug and tie-downs left in"]),
    ("spring", "Spring Prep", ["Charge the battery, clean terminals", "Check / replace the impeller", "Inspect fuel lines and primer bulb", "Change lower-unit gear oil", "New spark plugs if due", "Run on muffs — check the tell-tale", "Check trailer lights and bearings", "Refresh the safety-gear kit"]),
    ("winter", "Winterization", ["Add fuel stabilizer and run it through", "Fog the engine", "Drain water systems (block, livewell, ballast)", "Change lower-unit gear oil", "Remove and store the battery on a maintainer", "Protect the outside — cover or indoor storage"]),
]


_CHKL_JS = r"""<script>
(function () {
  var KEY = 'aftlog_chkl_';
  var CUST_KEY = 'aftlog_chkl_custom';
  var store = {};
  function persist(id){ try { localStorage.setItem(KEY+id, JSON.stringify(store[id]||[])); } catch(e){} }
  function load(id){ try { return JSON.parse(localStorage.getItem(KEY+id)||'[]'); } catch(e){ return []; } }
  function customList(){ try { return JSON.parse(localStorage.getItem(CUST_KEY)||'[]'); } catch(e){ return []; } }
  function saveCustom(c){ try { localStorage.setItem(CUST_KEY, JSON.stringify(c)); } catch(e){} }
  // one delegated listener for ALL checkboxes (templates + custom)
  document.addEventListener('change', function (e) {
    var it = e.target.closest && e.target.closest('.chkl-item');
    if (!it) return;
    var id = it.dataset.id, i = +it.dataset.i;
    if (!store[id]) store[id] = load(id);
    var k = store[id].indexOf(i);
    if (k === -1) store[id].push(i); else store[id].splice(k, 1);
    persist(id); paintBar(id);
  });
  function paintBar(id){
    var items = document.querySelectorAll('.chkl-item[data-id="'+id+'"]');
    var done = 0; items.forEach(function(it){ if ((store[id]||[]).indexOf(+it.dataset.i)!==-1) done++; });
    var p = items.length ? Math.round(100*done/items.length) : 0;
    var bar = document.getElementById('chkl-bar-'+id); var txt = document.getElementById('chkl-pct-'+id);
    if (bar) bar.style.width = p+'%';
    if (txt) txt.textContent = done+'/'+items.length;
  }
  function itemHtml(id, i, label, checked){
    return '<label class="chkl-item" data-id="'+id+'" data-i="'+i+'"><input type="checkbox"'+(checked?' checked':'')+'><span>'+String(label)+'</span></label>';
  }
  function renderCustom(){
    var holder = document.getElementById('chkl-custom');
    if (!holder) return;
    var data = customList();
    holder.innerHTML = data.map(function(c, idx){
      var id = 'custom'+idx;
      store[id] = load(id);
      var items = (c.items||[]).map(function(it, i){ return itemHtml(id, i, it, (store[id]||[]).indexOf(i)!==-1); }).join('');
      return '<div class="chkl" data-id="'+id+'"><div class="chkl-head"><strong>'+String(c.name)+'</strong><span class="chkl-pct" id="chkl-pct-'+id+'"></span></div><div class="chkl-items">'+items+'</div><div class="chkl-bar-bg"><div class="chkl-bar" id="chkl-bar-'+id+'"></div></div></div>';
    }).join('') || '<p class="pg-muted">No custom checklists yet — create one below.</p>';
    data.forEach(function(c, idx){ paintBar('custom'+idx); });
  }
  window.chklAddCustom = function () {
    var name = (document.getElementById('chkl-name').value||'').trim();
    var items = (document.getElementById('chkl-items').value||'').split(/\n/).map(function(s){return s.trim();}).filter(Boolean);
    if (!name || !items.length) { alert('Give it a name and at least one item (one per line).'); return; }
    var c = customList(); c.push({name:name, items:items}); saveCustom(c);
    document.getElementById('chkl-name').value=''; document.getElementById('chkl-items').value='';
    renderCustom();
  };
  document.querySelectorAll('.chkl[data-id]').forEach(function(box){ var id=box.dataset.id; store[id]=load(id); paintBar(id); });
  renderCustom();
})();
</script>"""


def _checklists_body():
    cards = "".join(
        '<div class="chkl" data-id="%s"><div class="chkl-head"><strong>%s</strong><span class="chkl-pct" id="chkl-pct-%s"></span></div><div class="chkl-items">%s</div><div class="chkl-bar-bg"><div class="chkl-bar" id="chkl-bar-%s"></div></div></div>' % (
            key, esc(label), key,
            "".join(
                '<label class="chkl-item" data-id="%s" data-i="%d"><input type="checkbox"><span>%s</span></label>' % (key, i, esc(it))
                for i, it in enumerate(items)),
            key)
        for key, label, items in _CHKL_TEMPLATES)
    return (
        hero("Checklists", "Step-by-step launch, retrieve, towing, and seasonal checklists — with your progress saved in this browser.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Tap each item as you do it. Your progress is saved on this device so you can pick up where you left off.</p>'
        + '<div class="chkl-list">' + cards + '</div>'
        + '<hr class="pg-hr">'
        + '<h2>My checklists</h2>'
        + '<div id="chkl-custom" class="chkl-list"></div>'
        + '<label class="pg-hint-label" for="chkl-name">New checklist name</label>'
        + '<input id="chkl-name" class="fp-in" placeholder="e.g. Weekend trip">'
        + '<label class="pg-hint-label" for="chkl-items">Items — one per line</label>'
        + '<textarea id="chkl-items" class="fp-in" rows="4" placeholder="Fuel up&#10;Check weather&#10;Tell someone the float plan"></textarea>'
        + '<p><button type="button" class="btn btn-primary" onclick="chklAddCustom()">Create checklist</button></p>'
        + '<p class="pg-muted">For a guided used-boat walk-through with photos and a buy/consider/walk report, use the <a href="/tools/buying-advisor.html">Buying Advisor</a>.</p>'
        + '<div class="pg-sidecard ms-promo"><div class="pg-sidecard-head">Marine Suite</div>'
        + '<p class="pg-muted" style="margin:0 0 8px">Packing gear? CatchTales keeps tackle, bait, and spots organized for the day.</p>'
        + '<a class="btn btn-secondary btn-sm" href="/catchtales.html">Explore CatchTales</a></div>'
        + _CHKL_JS
        + '</div></section>'
    )


register("tools/checklists", "AftLog Checklists — Launch, Retrieve, Towing & Seasonal",
         "Interactive launch, retrieve, towing, spring-prep, and winterization checklists with saved progress, plus your own custom checklists.",
         _checklists_body())


# ── STEP 5.10: Cost Insights tool ─────────────────────────────────────

_COST_JS = r"""<script>
(function () {
  var KS = 'aftlog_cost';
  var state = { hours: [], services: [], fuel: [] };
  try { var s = JSON.parse(localStorage.getItem(KS) || 'null'); if (s) state = Object.assign({ hours: [], services: [], fuel: [] }, s); } catch(e){}
  function save(){ try { localStorage.setItem(KS, JSON.stringify(state)); } catch(e){} }
  window.coHours = function () {
    var h = parseFloat(document.getElementById('co-hrs').value || '');
    if (!(h>0)) { alert('Enter hours.'); return; }
    state.hours.push({ h: h, ts: Date.now() });
    document.getElementById('co-hrs').value=''; save(); renderH(); compute();
  };
  window.coService = function () {
    var name = (document.getElementById('co-sname').value||'').trim() || 'Service';
    var c = parseFloat(document.getElementById('co-scost').value || '');
    if (!(c>=0)) { alert('Enter a cost.'); return; }
    state.services.push({ name: name, c: c, ts: Date.now() });
    document.getElementById('co-sname').value=''; document.getElementById('co-scost').value=''; save(); renderS(); compute();
  };
  window.coFuel = function () {
    var lit = parseFloat(document.getElementById('co-flit').value || '');
    var c = parseFloat(document.getElementById('co-fcost').value || '');
    c = isNaN(c) ? null : c; lit = isNaN(lit) ? null : lit;
    if (c===null && lit===null) { alert('Enter a cost and/or litres.'); return; }
    state.fuel.push({ L: lit, c: c, ts: Date.now() });
    document.getElementById('co-flit').value=''; document.getElementById('co-fcost').value=''; save(); renderF(); compute();
  };
  window.coClear = function () { if(!confirm('Clear all cost data on this device?')) return; state={hours:[],services:[],fuel:[]}; save(); renderH(); renderS(); renderF(); compute(); };
  window.coExport = function () { window.print(); };
  window.coTxt = function () {
    var t = 'COST OF OWNERSHIP - AFTLOG\n\n';
    t += 'TOTAL: $' + sum('services')+sum('fuel') + '\n';
    var h = hi(); t += 'PER HOUR: $' + (h>0 ? ((sum('services')+sum('fuel'))/h).toFixed(2) : '0.00') + ' (over ' + h + ' hrs)\n\n';
    t += 'SERVICES\n'; state.services.forEach(function(x){ t += '- ' + x.name + ': $' + x.c + '\n'; });
    t += '\nFUEL\n'; state.fuel.forEach(function(x){ t += '- ' + new Date(x.ts).toLocaleDateString() + ': $' + (x.c||'?') + (x.L?' ('+x.L+' L)':'') + '\n'; });
    var blob = new Blob([t], {type:'text/plain'}); var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download='aftlog-cost.txt'; a.click();
  };
  function sum(k){ return state[k].reduce(function(a,x){ return a+(x.c||0); },0); }
  function hi(){ return state.hours.reduce(function(a,x){ return a+(x.h||0); },0); }
  function litres(){ return state.fuel.reduce(function(a,x){ return a+(x.L||0); },0); }
  function compute(){
    var services = sum('services');
    var fuel = sum('fuel');
    var total = services + fuel;
    var hours = hi();
    var per = hours>0 ? total/hours : 0;
    var burn = (hours>0 && litres()>0) ? litres()/hours : null;
    setT('co-big-total', '$'+total.toFixed(0));
    setT('co-big-perhr', '$'+per.toFixed(2));
    setT('co-services', '$'+services.toFixed(0));
    setT('co-fuel', '$'+fuel.toFixed(0));
    setT('co-burn', burn!==null ? burn.toFixed(1)+' L/hr' : '—');
    setT('co-hours', hours.toFixed(0)+' hrs');
  }
  function setT(id,v){ var el=document.getElementById(id); if(el) el.textContent=v; }
  function row(x){ return '<div class="tl-row">'+new Date(x.ts).toLocaleDateString()+' · '+(x.name||'')+(x.c!=null?' · $'+x.c.toFixed(2):'')+(x.L?' · '+x.L+' L':'')+(x.h?' · '+x.h+' hrs':'')+'</div>'; }
  function renderH(){ var el=document.getElementById('co-list-hrs'); el.innerHTML = state.hours.slice().reverse().map(row).join('') || '<p class="pg-muted">No hours logged yet.</p>'; }
  function renderS(){ var el=document.getElementById('co-list-svc'); el.innerHTML = state.services.slice().reverse().map(row).join('') || '<p class="pg-muted">No service or maintenance expenses yet.</p>'; }
  function renderF(){ var el=document.getElementById('co-list-fuel'); el.innerHTML = state.fuel.slice().reverse().map(row).join('') || '<p class="pg-muted">No fuel logs yet.</p>'; }
  renderH(); renderS(); renderF(); compute();
})();
</script>"""


def _cost_body():
    return (
        hero("Cost of Ownership", "See the real cost of running your boat — total spent, per hour, services, fuel, and fuel burn.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Log your engine hours, services, and fuel fills — everything is saved in this browser and rolled up into your cost of ownership.</p>'
        + '<div class="co-cards">'
        + '<div class="co-big"><div id="co-big-total">$0</div><span>Total spent</span></div>'
        + '<div class="co-big"><div id="co-big-perhr">$0.00</div><span>Per hour</span></div>'
        + '</div>'
        + '<div class="co-metrics">'
        + '<div class="co-metric"><div id="co-services">$0</div><span>Services</span></div>'
        + '<div class="co-metric"><div id="co-fuel">$0</div><span>Fuel</span></div>'
        + '<div class="co-metric"><div id="co-burn">—</div><span>Fuel burn</span></div>'
        + '<div class="co-metric"><div id="co-hours">0 hrs</div><span>Engine hours</span></div>'
        + '</div>'
        + '<div class="co-entry"><h2>Log engine hours</h2>'
        + '<div class="tl-inline"><input id="co-hrs" class="fp-in" type="number" min="0" step="0.1" placeholder="Hours"><button type="button" class="btn btn-primary" onclick="coHours()">+ Add hours</button></div>'
        + '<div id="co-list-hrs"></div></div>'
        + '<div class="co-entry"><h2>Add a service / expense</h2>'
        + '<div class="tl-inline"><input id="co-sname" class="fp-in" placeholder="e.g. impeller, winterize"><input id="co-scost" class="fp-in" type="number" min="0" step="0.01" placeholder="$"><button type="button" class="btn btn-primary" onclick="coService()">Add</button></div>'
        + '<div id="co-list-svc"></div></div>'
        + '<div class="co-entry"><h2>Log a fuel fill</h2>'
        + '<div class="tl-inline"><input id="co-flit" class="fp-in" type="number" min="0" step="0.1" placeholder="Litres"><input id="co-fcost" class="fp-in" type="number" min="0" step="0.01" placeholder="$"><button type="button" class="btn btn-primary" onclick="coFuel()">Add</button></div>'
        + '<div id="co-list-fuel"></div></div>'
        + '<p><button type="button" class="btn btn-secondary" onclick="coExport()">Print / Save as PDF</button> '
        + '<button type="button" class="btn btn-secondary" onclick="coTxt()">Download .txt</button> '
        + '<button type="button" class="btn btn-sm btn-secondary" onclick="coClear()">Clear all</button></p>'
        + '<p class="pg-muted">Log fuel costs and services consistently and this shows the real cost of running your boat — the number that surprises every owner.</p>'
        + _COST_JS
        + '</div></section>'
    )


register("tools/cost-insights", "AftLog Cost of Ownership",
         "Track service and fuel expenses plus engine hours, and see your total cost, per-hour cost, and fuel burn.",
         _cost_body())


# ── STEP 4.10: Parts Locator tool ─────────────────────────────────────

_PARTS_JS = r"""<script>
(function () {
  var CATS = [
    ['impeller','Impeller / Water Pump Kit','impeller kit'],
    ['spark','Spark Plugs','marine spark plug'],
    ['fuel_filter','Fuel Filter','fuel filter'],
    ['oil_filter','Oil Filter','marine oil filter'],
    ['gearcase_oil','Gearcase Oil','lower unit oil'],
    ['thermostat','Thermostat','marine thermostat'],
    ['anodes','Anodes','zinc anode'],
    ['propeller','Propeller','boat prop'],
    ['battery','Battery','marine battery'],
    ['bilge','Bilge Pump','bilge pump'],
    ['nav_lights','Navigation Lights','marine nav lights'],
    ['trailer_wiring','Trailer Wiring','trailer wiring'],
    ['trim_motor','Trim & Tilt Motor','trim motor'],
    ['steering','Steering Cable','steering cable']
  ];
  var SUPS = [
    ['Amazon','https://www.amazon.com/s?k={q}','https://www.amazon.ca/s?k={q}'],
    ['eBay','https://www.ebay.com/sch/i.html?_nkw={q}','https://www.ebay.ca/sch/i.html?_nkw={q}'],
    ['Walmart','https://www.walmart.com/search?q={q}','https://www.walmart.ca/search?q={q}'],
    ['Bass Pro','https://www.basspro.com/shop/en/search?q={q}','https://www.basspro.ca/shop/en/search?q={q}'],
    ["Cabela's",'https://www.cabelas.com/shop/en/search?q={q}','https://www.cabelas.ca/shop/en/search?q={q}'],
    ['West Marine','https://www.westmarine.com/search.html?q={q}',null],
    ['Canadian Tire',null,'https://www.canadiantire.ca/en/search-results.html?q={q}'],
    ['Princess Auto',null,'https://www.princessauto.com/en/search?q={q}'],
    ['Academy','https://www.academy.com/search?q={q}',null],
    ['AutoZone','https://www.autozone.com/search?q={q}',null],
    ["O'Reilly",'https://www.oreillyauto.com/search?q={q}',null]
  ];
  var BRANDS = ['Mercury','Yamaha','Honda','Suzuki','Evinrude'];
  var BRANDROWS = {
    Mercury:{impeller:'47-879872K1','fuel_filter':'35-883072T03',thermostat:'75692',spark:'NGK IZFR5G',anodes:'97-888756',propeller:'835257K1',gearcase_oil:'92-858064K01',trim_motor:'828708A1'},
    Yamaha:{impeller:'6H5-44352-00','fuel_filter':'6E5-24305-00',thermostat:'6G8-12411-00',spark:'NGK DPR6EA-9',anodes:'688-45251-02',propeller:'67H-45987-00',gearcase_oil:'Yamalube Marine Gear Oil',trim_motor:'6H1-43880-02'},
    Honda:{impeller:'06192-ZV1-000','fuel_filter':'16910-ZY3-003',thermostat:'19300-ZW1-003',spark:'NGK IFR6J11',anodes:'41106-ZW1-000',propeller:'41110-ZW1-000',gearcase_oil:'Honda Marine Hypoid',trim_motor:'36120-ZW4-013'},
    Suzuki:{impeller:'17551-93J00','fuel_filter':'15410-87J00',thermostat:'17670-87J00',spark:'NGK BKR6E',anodes:'55321-87J00',propeller:'57620-87L00',gearcase_oil:'Suzuki Hypoid',trim_motor:'38100-87J00'},
    Evinrude:{impeller:'774733','fuel_filter':'5004420',thermostat:'5005440',spark:'NGK IZFR6J',anodes:'5007697',propeller:'177284',gearcase_oil:'HPF PRO',trim_motor:'5007083'}
  };
  var UNIV = [['Bilge pump','Rule 500/800/1100'],['Bilge float switch','Rule SuperSwitch'],['Navigation lights','Attwood LED'],['Battery','Group 24/27/31'],['Battery switch','Perko 8501'],['Fuses','ATC/ATO marine'],['Breakers','Blue Sea Systems'],['Trailer wiring harness','4-pin/5-pin/7-pin'],['Trailer lights','LED submersible'],['Trailer bearings','1-1/16" or 1-3/8"'],['Trailer tires','ST175/80R13 or ST205/75R14'],['Winch strap','2" x 20-25 ft']];
  var catSel = document.getElementById('pl-cat');
  var brandSel = document.getElementById('pl-brand');
  var hpIn = document.getElementById('pl-hp');
  var smart = document.getElementById('pl-smart');
  var country = 'us';
  function fillCats(){
    CATS.forEach(function(c){ var o=document.createElement('option'); o.value=c[0]; o.textContent=c[1]; catSel.appendChild(o); });
    BRANDS.forEach(function(b){ var o=document.createElement('option'); o.value=b; o.textContent=b; brandSel.appendChild(o); });
  }
  window.plCountry = function (c){ country=c; Array.prototype.forEach.call(document.querySelectorAll('.pl-country'), function(b){ b.classList.toggle('on', b.dataset.c===c); }); find(); };
  function catName(id){ for(var i=0;i<CATS.length;i++) if(CATS[i][0]===id) return CATS[i]; return null; }
  function enc(s){ return encodeURIComponent(s).replace(/%20/g,'+'); }
  function find(){
    var cat = catName(catSel.value); if(!cat) return;
    var base = cat[2];
    var keyword = base;
    if (smart.checked) {
      var b = (brandSel.value||'').trim().toLowerCase().replace(/\s+/g,'+');
      var hp = parseInt(hpIn.value,10);
      if (b) keyword = hp>0 ? b+'+'+hp+'hp+'+base : b+'+'+base;
    }
    var out = document.getElementById('pl-links');
    out.innerHTML = '';
    var added = 0;
    SUPS.forEach(function(s){
      var url = country==='ca' ? (s[2]||s[1]) : s[1];
      if (!url) return;
      var a = document.createElement('a');
      a.className = 'btn btn-sm btn-secondary pl-link';
      a.href = url.replace('{q}', enc(keyword));
      a.target = '_blank'; a.rel = 'noopener';
      a.textContent = s[0];
      out.appendChild(a); added++;
    });
    document.getElementById('pl-keyword').textContent = keyword;
    document.getElementById('pl-count').textContent = added + ' suppliers (' + (country==='ca'?'Canada':'US') + ')';
    renderNumbers(cat[0], cat[1]);
  }
  function renderNumbers(cid, cname){
    var box = document.getElementById('pl-numbers');
    var brand = brandSel.value;
    var html = '';
    if (brand && BRANDROWS[brand]) {
      var row = BRANDROWS[brand][cid];
      html = '<h2>Common part number</h2><p class="pg-muted"><strong>'+brand+' · '+cname+':</strong> '+(row||'—')+'</p>';
      html += '<p class="pg-muted">Cross-reference numbers vary by model and year — always verify for your engine before buying.</p>';
    } else if (cid==='bilge'||cid==='battery'||cid==='nav_lights'||cid==='trailer_wiring') {
      var u = UNIV.filter(function(x){ return (cid==='bilge'&&(x[0].toLowerCase().indexOf('bilge')!==-1)) || (cid==='battery'&&x[0].toLowerCase()==='battery') || (cid==='nav_lights'&&x[0].toLowerCase().indexOf('navigation')!==-1) || (cid==='trailer_wiring'&&x[0].toLowerCase().indexOf('trailer wiring')!==-1); });
      html = '<h2>Common references</h2>' + u.map(function(x){ return '<div class="tl-row">'+x[0]+' · <strong>'+x[1]+'</strong></div>'; }).join('');
    } else {
      html = '<h2>Common part numbers</h2><p class="pg-muted">Choose an engine brand above to see cross-reference part numbers for this part.</p>';
    }
    box.innerHTML = html;
  }
  catSel.addEventListener('change', find);
  brandSel.addEventListener('change', find);
  hpIn.addEventListener('input', find);
  smart.addEventListener('change', find);
  fillCats(); plCountry('us');
})();
</script>"""


def _parts_locator_body():
    ctry = ('<div class="pl-country-row">'
            '<span class="pg-muted">Country:</span> '
            '<button type="button" class="btn btn-sm pl-country on" data-c="us" onclick="plCountry(\'us\')">US</button> '
            '<button type="button" class="btn btn-sm pl-country" data-c="ca" onclick="plCountry(\'ca\')">Canada</button></div>')
    return (
        hero("Parts Locator", "Pick a part, choose your engine, and jump straight to the suppliers who carry it.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">Choose a part and a country for direct supplier search links. Optional engine brand + HP builds a smarter search.</p>'
        + ctry
        + '<div class="pl-controls">'
        + '<label class="pg-hint-label" for="pl-cat">Part</label><select id="pl-cat" class="pg-select"></select>'
        + '<label class="pg-hint-label" for="pl-brand">Engine brand (optional)</label><select id="pl-brand" class="pg-select"><option value="">— none —</option></select>'
        + '<label class="pg-hint-label" for="pl-hp">Horsepower (optional)</label><input id="pl-hp" class="fp-in" type="number" min="0" placeholder="150" style="max-width:120px">'
        + '<label class="pg-hint-label"><input type="checkbox" id="pl-smart" checked> Build a smarter search with brand + HP</label>'
        + '</div>'
        + '<div class="pl-results">'
        + '<p class="pg-muted" id="pl-count"></p>'
        + '<p class="pg-muted">Keyword: <strong id="pl-keyword"></strong></p>'
        + '<div id="pl-links" class="pl-links"></div>'
        + '<div id="pl-numbers"></div>'
        + '</div>'
        + '<p class="pg-muted">Common part numbers are cross-reference numbers — always verify for your model and year before buying. Some suppliers may offer referral benefits.</p>'
        + _PARTS_JS
        + '</div></section>'
    )


register("tools/parts-locator", "AftLog Parts Locator",
         "14 part categories with US/Canada supplier search links and common cross-reference part numbers for Mercury, Yamaha, Honda, Suzuki, and Evinrude.",
         _parts_locator_body())


# ── Central /tools/ index (looks-up every tool) ──────────────────────

_TOOLS_CATALOG = [
    ("Safety & planning", [
        ("/tools/emergency.html", "Emergency — What to Do If…", "Calm steps + your GPS position ready to share with help."),
        ("/tools/float-plan.html", "Float Plan", "Tell someone where you're going and when you'll be back."),
        ("/tools/compliance.html", "Compliance", "Registration, safety gear, and the boating rules."),
        ("/tools/ramp-mode.html", "Ramp Mode", "Big-button launch and retrieve checklist for the ramp."),
    ]),
    ("Trip & fuel", [
        ("/tools/trip-log.html", "Trip & Fuel Log", "Log trips and fills; see your real fuel range and time-to-empty."),
        ("/tools/trip-patterns.html", "Trip Patterns", "Totals, averages, seasonality, and outliers from your trips."),
        ("/tools/predictive-planner.html", "Predictive Planner", "What's due next by hours, months, and severity."),
    ]),
    ("Checklists & seasonal", [
        ("/tools/checklists.html", "Checklists", "Launch, retrieve, towing and seasonal checklists with saved progress."),
        ("/tools/winterization-planner.html", "Winterization Planner", "Freeze-up and ice-out timing for your region."),
    ]),
    ("Buying & cost", [
        ("/tools/buying-advisor.html", "Buying Advisor", "Rule-based used-boat evaluation with risk warnings."),
        ("/tools/cost-insights.html", "Cost of Ownership", "Total spent, per-hour cost, services, fuel, and fuel burn."),
    ]),
    ("Maintenance & parts", [
        ("/tools/diy-library.html", "DIY Library", "Step-by-step repairs you can do yourself."),
        ("/tools/manual-finder.html", "Manual Finder", "Official manuals and parts sources, grouped."),
        ("/tools/parts-locator.html", "Parts Locator", "Pick a part and jump to suppliers who carry it."),
        ("/tools/battery-electronics.html", "Battery & Electronics", "Track your gear and size wiring."),
    ]),
    ("Diagnostics & AI", [
        ("/tools/ai-diagnostics.html", "AI Diagnostics", "Symptom + drive selector with causes and next steps."),
        ("/tools/visual-engine-assist.html", "Visual Engine Assist", "Tap a part on the diagram and get the check for it."),
        ("/tools/ask-aftlog.html", "Ask AftLog", "Boat-specific AI answers, grounded and offline."),
    ]),
    ("Reference & math", [
        ("/tools/calculators.html", "Calculators", "Fuel burn, prop slip, anchor, voltage drop, oil mix."),
        ("/tools/glossary.html", "Glossary", "Boat terms in plain talk — and the technical version."),
    ]),
]


def _tools_index_body():
    groups = "".join(
        '<div class="pg-tools-group"><h2>%s</h2><div class="pg-card-grid pg-tools-grid">%s</div></div>' % (
            esc(group),
            "".join(
                '<a class="pg-blog-card pg-tool-card" href="%s"><h3>%s</h3><p>%s</p></a>' % (url, esc(name), esc(desc))
                for url, name, desc in tools)
        )
        for group, tools in _TOOLS_CATALOG)
    return (
        hero("AftLog Tools", "Every free boating tool in one place — planning, tracking, maintenance, diagnostics, and reference.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">20 tools, all free and all work offline in your browser. For the full boat-manager experience — logbook, intervals, checklists, documents and more — use the <a href="/features.html">AftLog app</a> on your phone.</p>'
        + groups
        + '</div></section>'
    )


register("tools/index", "AftLog Tools — Every Free Boating Tool",
         "All 20 free AftLog boating tools in one place: safety, trip & fuel, checklists, buying, cost, maintenance, diagnostics, AI, and reference.",
         _tools_index_body())

def _catchtales_body():
    return (
        hero("CatchTales — your fishing logbook, built for real days on the water.", "Track catches, spots, conditions, and patterns — all offline, all yours.")
        + '<section class="section section--light"><div class="container">'
        + '<p class="pg-muted">CatchTales is the fishing companion to AftLog — AftLog keeps your boat shipshape, CatchTales logs the fishing. Together they cover a full day on the water.</p>'
        + '<h2>What CatchTales does</h2>'
        + '<div class="pg-card-grid">'
        + '<div class="pg-feature-card"><h3>Log catches</h3><p>Species, weight/length, photos, and conditions.</p></div>'
        + '<div class="pg-feature-card"><h3>Track fishing spots</h3><p>GPS, depth, best species.</p></div>'
        + '<div class="pg-feature-card"><h3>Record sessions</h3><p>Trips, tallies, voice input.</p></div>'
        + '<div class="pg-feature-card"><h3>Browse species</h3><p>Identification, limits, reference.</p></div>'
        + '<div class="pg-feature-card"><h3>Check conditions</h3><p>Weather, solunar, tide.</p></div>'
        + '<div class="pg-feature-card"><h3>Organize tackle</h3><p>Lures, tips, target species.</p></div>'
        + '<div class="pg-feature-card"><h3>View analytics</h3><p>Patterns, seasons, best times.</p></div>'
        + '<div class="pg-feature-card"><h3>Stay offline</h3><p>Works without a signal.</p></div>'
        + '</div>'
        + '</div></section>'
        + '<section class="section section--alt"><div class="container">'
        + '<h2>Works with AftLog</h2>'
        + '<p>AftLog handles your boat — maintenance, safety, and trip prep. CatchTales handles your fishing — species, spots, and conditions. Together, they make a full day on the water easier.</p>'
        + '<div class="pg-marine-suite"><div class="brand-block"><span class="kicker brand-slogan">Marine Suite</span><h3>Two apps for one day on the water.</h3></div>'
        + '<a href="/features.html" class="pg-marine-cta">Meet AftLog →</a></div>'
        + '</div></section>'
        + '<section class="section section--light"><div class="container">'
        + '<h2>Get CatchTales</h2>'
        + '<p class="pg-muted">Direct download arrives at CatchTales launch — coming soon.</p>'
        + '<p><span class="btn btn-secondary" aria-disabled="true">Coming soon</span></p>'
        + '<p class="pg-muted">Questions? <a href="mailto:catchtales@yahoo.com">Email CatchTales</a>.</p>'
        + '</div></section>'
    )


register("catchtales", "CatchTales — Fishing Companion · Works with AftLog", "CatchTales is AftLog's fishing companion — log trips, catches, spots, and conditions offline. Part of the Marine Suite.", _catchtales_body())


def main():
    print(f"Generating AftLog site → portal base: {PORTAL}")
    for p in PAGES:
        html_doc = page(p["slug"], p["title"], p["desc"], p["body"], p.get("active"))
        if p["slug"] == "blog/index":
            write("blog/index.html", html_doc)
        else:
            write(f"{p['slug']}.html", html_doc)

    generate_help()

    # sitemap
    static = ["", "features.html", "ai.html", "portal.html", "pricing.html",
              "faq.html", "support.html", "privacy.html", "terms.html",
              "catchtales.html",
              "updates/", "blog/", "blog/winterize.html",
              "blog/beginner-checklist.html", "blog/outboard-oil.html",
              "blog/safety-equipment.html", "tools/", "tools/index.html"]
    urls = "".join(f"  <url><loc>https://aftlog.com/{s}</loc></url>\n" for s in static)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

    # robots
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://aftlog.com/sitemap.xml\n")

    print("Done.")


if __name__ == "__main__":
    main()
