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

BLOG_ARTICLES = [
    ("How to winterize your boat", "A step-by-step winterization plan — fuel, engine, water systems, battery, and cover.", "Maintenance", "/blog/winterize.html", "/images/screen-app-dashboard.png"),
    ("Boat maintenance checklist for beginners", "The 12 checks every new owner should know before launching.", "Maintenance", "/blog/beginner-checklist.html", "/images/screen-app-checklists.png"),
    ("How often to change outboard oil", "Intervals, why they matter, and how AftLog tracks them for you.", "Maintenance", "/blog/outboard-oil.html", "/images/screen-smp-plan.png"),
    ("Lower-unit service: when and why", "Gear oil, seals, and the simple checks that keep your lower unit alive.", "Maintenance", None, None),
    ("Spark plug intervals explained", "Why 200 hours is the rule, and the symptoms of worn plugs.", "Maintenance", None, None),
    ("Impeller replacement: symptoms and timing", "Weak tell-tale? It's usually the impeller. Here's when to change it.", "Maintenance", None, None),
    ("Battery care for small boats", "Charge, store, and check — batteries die in the off-season, not on the water.", "Maintenance", None, None),
    ("Boat safety equipment list", "What to carry on board — and how to check it before every launch.", "Safety", "/blog/safety-equipment.html", "/images/screen-portal-health.png"),
    ("How to handle an engine that won't start", "A calm, ordered checklist for the most frustrating moment in boating.", "Safety", None, None),
    ("Overheating on the water: what to do", "Recognize it early and know when to stop — before it becomes a big repair.", "Safety", None, None),
    ("How to build a float plan", "Tell someone where you're going — it takes two minutes and saves lives.", "Safety", None, None),
    ("Launch checklist: the complete guide", "Plug, pump, battery, gear — everything checked before you leave the ramp.", "Checklists", None, None),
    ("Retrieve checklist: avoid trailer mistakes", "The five-minute routine that prevents ramp-day damage.", "Checklists", None, None),
    ("Used-boat inspection checklist", "The 13-section walkthrough that helps you buy with confidence.", "Checklists", None, None),
    ("Spring prep: getting your boat ready", "De-winterize, inspect, and launch right the first time.", "Seasonal prep", None, None),
    ("Fall haul-out checklist", "The off-season routine that makes spring easy.", "Seasonal prep", None, None),
    ("Fuel storage best practices", "Stabilizer, full tanks, and why ethanol needs a plan.", "Seasonal prep", None, None),
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


# ── Render ──────────────────────────────────────────────────────────────
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
              "updates/", "blog/", "blog/winterize.html",
              "blog/beginner-checklist.html", "blog/outboard-oil.html",
              "blog/safety-equipment.html"]
    urls = "".join(f"  <url><loc>https://aftlog.com/{s}</loc></url>\n" for s in static)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

    # robots
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://aftlog.com/sitemap.xml\n")

    print("Done.")


if __name__ == "__main__":
    main()
