# AftLog Platform — Release Manifest v1.111

**Platform release:** v1.111 · **Date:** 2026-08-17 · **Status:** FROZEN
**Supersedes:** all per-session states through DEEPSEEK Step 8 (Sessions 39–48).

This manifest freezes the AftLog architecture after the DEEPSEEK
consolidation (Steps 1–8). It is the authority for what ships and how the
four components connect. Changes to anything listed here require a new
manifest version.

---

## 1. Architecture freeze (final)

### 1.1 AI pipeline (unified — ONE proxy)
```
App      ──POST /ai/gemini──▶  Portal Server ──▶ Gemini (gemini-3.6-flash)
Portal  ──in-process call──▶  AiProxyService ──▶ Gemini
Website ──POST /ai/gemini──▶  Portal Server ──▶ Gemini
```
- No direct Gemini calls anywhere except `aftlog_server/lib/services/ai_proxy.dart`.
- No Gemini keys outside the server environment (`AFTLOG_GEMINI_KEY`).

### 1.2 Publisher pipeline
```
App      ──POST /admin/publish──▶ Server ──▶ GitHub (aftlog/aftlog-site)
Portal  ──in-process call──────▶ GithubProxyService ──▶ GitHub
Website ──GET  /admin/publish──▶ Server (review count)
```
- No direct GitHub calls anywhere except `aftlog_server/lib/services/github_proxy.dart`.
- No GitHub tokens outside the server environment (`AFTLOG_GITHUB_TOKEN`).

### 1.3 License Manager
- Server-only writer for `pro_licenses` (Firestore).
- **Lifetime-only** — the product is a one-time $29 purchase, no
  subscriptions (Decision #3). `/admin/licenses` refuses non-lifetime.
- App + Portal + Website never hold or see any license credential.

### 1.4 Design system
- **Portal DS = canonical** (Sessions 38 + 48): dark `#0B0B0D`, accents
  `#E02020`/`#FF4B4B`, portal light surface `#EDEDF2`, portal `portal.css`
  tokens.
- **Website DS aligned** to the same palette (`aftlog.css` + `aftlog-pages.css`),
  website light surface `#F5F5F7`.
- **App DS unchanged** (Flutter `AftLogTheme`, dark-only). No new colors
  anywhere; no redesigns.

### 1.5 Routing
- **Website:** multi-page static (GitHub Pages, `.html` URLs, `/blog/` +
  `/updates/` directories).
- **Portal:** multi-page dynamic (Dart shelf + `web/portal/*.html` shell
  pages; `/portal/` hub is the entry point).
- **App:** Flutter screens (SQLite offline-first).
- **Server:** REST endpoints (shelf), single process, dev server on :8080.

---

## 2. What's in v1.111

### App (Android) — internal label: app 1.108.7 (versionCode 154)
AI proxy integration (Ask AftLog + VEA photo assist via `/ai/gemini`) ·
Smart Planner · Diagnostics (rule-based) · Manual extraction (Engine
Manual Assist) · Offline-first logging · Checklists + Wizards · Emergency
screen · Boat model + intervals · Lifetime license support (Enter Pro
Code / Pro Status) · Review Publisher via server proxy · License Manager
(dev) via server · 429 unit tests + 2 known pre-existing LocalBundleServer
failures · analyzer clean.

### Portal (Web) — v1.111
Homepage hub v1.111 (hero, live data strip, AI widget, ecosystem links) ·
Analytics dashboard (year-in-review, trips, maintenance, boat health) ·
Smart Planner · Diagnostics via Ask AftLog · Manual Extraction (manual
generator) · Imports page · Ask AftLog widget · Review badge · Portal
login · canonical Portal DS · 141 server tests green.

### Website (aftlog.com) — v1.111
8 SEO pages (home, features, ai, portal, pricing, faq, support, privacy,
terms) · 4 blog articles · Ask AftLog widget (`/ai/gemini`) · Review badge
(`/admin/publish`) · lifetime pricing page · sitemap.xml + robots.txt ·
shared nav/footer · 134-check test matrix green.

### Server (aftlog_server) — v1.111
AI proxy · Publisher proxy · License manager (lifetime-only) ·
`/ai/health` + `/status` · CORS middleware · `start-dev-server.sh` ·
**141 tests green.**

---

## 3. Version lock (Section 7 of the block)

| Component | Version | Where it lives |
|-----------|---------|----------------|
| Portal | v1.111 | `web/portal/index.html` (hub badge + `/status`) |
| Server | v1.111 | `GET /status` → `portalVersion: v1.111` |
| Website | v1.111 | site footer ("Platform v1.111") |
| App | v1.111 (internal label) | app 1.108.7+154 — see note |

> **Note:** the app keeps its feature-based semver (`1.108.7`, per
> Decision #11 amended: minor = FEATURES.md count). "App v1.111" is the
> platform label for this manifest; the app's own version is authoritative
> for builds/installs.

---

## 4. Security freeze (verified)

- `GEMINI_API_KEY` / `GITHUB_TOKEN` / `AFTLOG_SA_JSON`: **absent from
  app, portal, website** (probed APK: 0 hits; greps: 0 hits).
- No secrets in build pipelines (`build.sh` injects nothing secret).
- No direct external API calls from any client (app: 0 `generativelanguage`
  / 0 `api.github.com`; website: 0; portal web/: 0).
- All AI/publish/license traffic goes through the server proxies.

## 5. SEO freeze (verified)

- `sitemap.xml` lists all 15 pages · `robots.txt` allows indexing ·
  canonical tags on all SEO pages · unique title/description per page ·
  blog pages indexed. (Lighthouse ≥95: run manually in Chrome DevTools —
  browser-only.)
