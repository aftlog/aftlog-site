# AftLog Platform — Release Manifest v1.112

**Platform release:** v1.112 · **Date:** 2026-08-18 · **Status:** FROZEN
**Supersedes:** RELEASE-MANIFEST-v1.111.md (2026-08-17, DEEPSEEK Steps 1–8).

This manifest re-freezes the AftLog architecture after the P0 security
hardening and P1 maintainability pass. It is the authority for what ships
and how the four components connect. Changes to anything listed here
require a new manifest version.

---

## 1. Architecture freeze (unchanged from v1.111)

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
- **Lifetime-only** — one-time $29 purchase, no subscriptions (Decision #3).
- App + Portal + Website never hold or see any license credential.

### 1.4 Design system
- **Portal DS = canonical**: dark `#0B0B0D`, accents `#E02020`/`#FF4B4B`,
  portal light surface `#EDEDF2`, `portal.css` tokens.
- **Website DS aligned** (`aftlog.css` + `aftlog-pages.css`), light surface `#F5F5F7`.
- **App DS unchanged** (Flutter `AftLogTheme`, dark-only). No new colors; no redesigns.

### 1.5 Routing
- **Website:** multi-page static (GitHub Pages, `.html` URLs, `/blog/` + `/updates/`).
- **Portal:** multi-page dynamic (Dart shelf + `web/portal/*.html` shell pages).
- **App:** Flutter screens (SQLite offline-first).
- **Server:** REST endpoints (shelf), single process, dev server on :8080.

### 1.6 Server layout (NEW in v1.112)
`handlers.dart` is now a thin assembler; route handlers live in domain
modules under `lib/api/` (`routes_{imports,analytics,portal,auth,link,
licenses,ai,publish,boats,manual}.dart`), sharing `RouteContext`
(gates/parsers/static files) and module-level rate limiters
(`rate_limits.dart`).

---

## 2. What's new in v1.112

### P0 — Security hardening (2026-08-18)
- **Dev gate deny-by-default** (`lib/api/dev_gate.dart`): `/ai/gemini`,
  `/admin/licenses`, `/admin/publish` are DISABLED unless `AFTLOG_DEV_KEY`
  is a real secret — unset and the old `aftlog-dev` default both deny.
  Same-origin portal pages pass once armed; cross-origin callers (app,
  website) present `X-Aftlog-Dev-Key`. `start-dev-server.sh` mints a
  per-machine key at `~/.config/aftlog/dev-key` (chmod 600); `build.sh dev`
  injects the same key via `--dart-define=AFTLOG_DEV_KEY`.
- **Session cookies:** `Secure` added (browsers exempt localhost, so the
  lab keeps working over HTTP).
- **Rate limits** (`lib/api/rate_limit.dart`): per-IP fixed windows on the
  unauthenticated app routes — `/link-code/create` 10/min,
  `/boats/upload` 20/min. Module-level so they survive the per-request
  `buildRouter()` in `bin/server.dart`'s CORS handler.

### P1 — Maintainability
- `handlers.dart` split into 10 domain route modules (see §1.6).
- This manifest (v1.112) resolves the version drift: app is now frozen at
  **1.108.18+165** (was 1.108.7+154 in v1.111).

---

## 3. What's in v1.112 (cumulative)

### App (Android) — internal label: app 1.108.18 (versionCode 165)
All v1.111 features (AI proxy, Smart Planner, Diagnostics, manual
extraction, offline-first logging, checklists, wizards, emergency,
lifetime Pro, Review Publisher, License Manager) · dev tools read
`AFTLOG_DEV_KEY` dart-define (deny-by-default gate) · **462 unit/widget
tests green** · analyzer clean.

### Portal (Web) — v1.112
Homepage hub · analytics dashboards (year-in-review, trips, maintenance,
boat health, planner) · imports · Ask AftLog widget · review badge · login
/ redeem / Pro dashboard · canonical Portal DS · hub fetches are
same-origin (no embedded key) · **151 server tests green**.

### Website (aftlog.com) — v1.112
SEO pages · blog (17 articles) · tools (21) · help (18) · checklists ·
Ask AftLog widget · review badge · sitemap.xml + robots.txt · shared
nav/footer · ~330-check `site_check.py` matrix green.

### Server (aftlog_server) — v1.112
AI proxy · Publisher proxy · License manager (lifetime-only) · auth
(login/signup/reset/logout + session cookies) · app linking · boats ·
manual generator · `/ai/health` + `/status` · CORS middleware ·
`start-dev-server.sh` (key minting) · **151 tests green**.

---

## 4. Version lock

| Component | Version | Where it lives |
|-----------|---------|----------------|
| Portal | v1.112 | `web/portal/index.html` (hub badge + `/status`) |
| Server | v1.112 | `GET /status` → `portalVersion: v1.112` |
| Website | v1.112 | site footer ("Platform v1.112") |
| App | v1.112 (platform label) | app **1.108.18+165** — see note |

> **Note:** the app keeps its feature-based semver (`1.108.18`, per
> Decision #11 amended: minor = FEATURES.md count). "App v1.112" is the
> platform label for this manifest; the app's own version is authoritative
> for builds/installs. FEATURES.md count stays 108 until the next feature.

---

## 5. Security freeze (verified)

- `GEMINI_API_KEY` / `GITHUB_TOKEN` / `AFTLOG_DEV_KEY`: absent from app,
  portal, website (APK probe: 0 hits; greps: 0 hits).
- No secrets in build pipelines (`build.sh` injects only the dev key for
  dev builds; pro builds carry none).
- No direct external API calls from any client — all AI/publish/license
  traffic goes through the server proxies.
- Dev admin/AI routes deny by default (P0) — a public server cannot run
  with the lab default.
- Session cookie: `HttpOnly; SameSite=Lax; Secure`.

## 6. SEO freeze (verified)

- `sitemap.xml` lists all pages · `robots.txt` allows indexing · canonical
  tags on all SEO pages · unique title/description per page.
- (Lighthouse ≥95: run manually in Chrome DevTools — browser-only.)

## 7. Known follow-ups (not in this freeze)

- **Deploy:** the 5 unpushed site commits behind `origin/main` (Marine
  Suite / CatchTales + blog screenshots) must be pushed; `portal.aftlog.com`
  is not yet live; the site's review badge points at the un-deployed portal.
- **Visual Engine Assist:** `data/vea.json` diagram paths carry a spurious
  `assets/` segment — all 19 diagrams 404 on the live site (and locally).
- **Portal rendering:** trip-heatmap (`METRIC` vs `METRICS`), trip-calendar
  (string-slice `<td>` corruption), clustering + boat-health tables
  (`undefined` cells), hub review-badge 403 (missing dev-key header on
  `fetchJSON`), duplicate H1s on `/portal/` and `/portal/imports`.
