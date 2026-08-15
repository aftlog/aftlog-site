# AftLog — Session Log

> Read `AFTLOG-CODING-STANDARDS.md` + `DECISIONS.md` first every session.

---

## ⚠️ REMINDERS FOR NEXT SESSION

- **🔜 NEXT UP (updated 2026-08-15):** MAINTENANCE PLANNER **is SHIPPED** (features #71–77 + #86, 1.71.0–1.86.0 — More → Maintenance Planner; tabs, seasons/analytics/predictive/export Pro-gated). The session-log note from 08-14 saying it was missing was STALE. Real open frontier: server spec slices (trip-heatmap/clustering/forecast done on portal; maintenance/planner/boat-health dashboards remain) · portal deployment decision (Aug 24 gate) · free-tier gating not enforced · Pro purchase wiring · per-interval due-soon notifications · hotpot alignment. Candidate enhancement if desired: explicit 30/90/365-day bucket view on the existing planner (a team-spec PlannerScreen was reviewed 08-15 — 5 API mismatches, does NOT compile; only new idea worth keeping is the 30/90/365 buckets).
- **🔴 adb stall (Samsung):** plain `adb push` can wedge or silently drop big files. Reliable: chunked push (8MB parts) → verify chunk count (10) → cat on device → md5sum match → pm install. Seen many times 2026-08-14. Also in CODING-STANDARDS §3.
- **Email convention (LOCKED 2026-08-14):** ALL mailtos = `aftlog@yahoo.com` + context-specific subject (CatchTales pattern). Never a second address.
- **Open (parked):** hotspot visual alignment (79 knowledge-based hotspots, editor at tools/aftlog-diagram-editor.html) · deep-screen translations (Rule 3 pass at release) · site rollout (analytics → beta CTA → distribution; Aug 24 gate) · MLD logo spacing done 5j.
- **🔴 OPEN ITEMS (see Session 4 for full log):**
  1. **Hotspot alignment:** current 79 hotspots are knowledge-based — align via the editor (`tools/aftlog-diagram-editor.html`): Import JSON from `tools/hotspots/`, load the WebP, drag into place, Export → `python3 tools/hotspots_to_dart.py` → rebuild with plain `./build.sh`.
  2. **Review backlog (Session 4 findings, cheap fixes):** daily check-in dies on reboot (`RECEIVE_BOOT_COMPLETED` missing) · onboarding flag written before onboarding finishes · free-tier gating not enforced (AI + reminders should be Pro per Decision #3) · Boats tab stale (listen to `BoatEvents`) · `Units` service dead code (metric toggle half-wired)
  3. **Data blanks:** interval amounts per engine · glossary check (29 terms) · boat-style prices · buying-quiz weights · calculator assumptions (placeholders in `reference_data.dart`) — incl. boat-style prices/running costs (16 styles), buying-quiz weights, calculator assumptions (default 30 km/h cruise, 30 L tank examples)
  4. **Translations:** core strings only; deep screens still EN (Rule 3 pass at release)
  5. **Pro purchase wiring:** `pro_service.dart` is just a flag — the $29 unlock isn't purchasable yet
  6. **Scheduled interval notifications:** daily check-in works; per-interval due-soon push not wired
- **Gate 0 waitlist running** — landing live at aftlog.com (formspree `xoeaezwv`). 2-week countdown from 2026-08-10 → decision ~Aug 24. Landing already refreshed with the beginner angle.
- **AI is LIVE:** `GEMINI_API_KEY` in env (key in pass, same as CatchTales) — builds embed it. Ask AftLog grounded with boat context, brevity enforced, "continue" works, error taxonomy in. Gemini Flash kept (no o3-mini — truncation was our prompt/cap bug; provider switch designed-not-built).
- **Repo hygiene DONE 2026-08-12:** purged 136MB of stray build/APK-extraction junk (lib/*.so dumps + root dex/arsc/META-INF/res); gitignore patterns added; tracked size 153MB→17MB. (History still holds old blobs — optional rewrite like CatchTales later.)
- **CoPilot review workflow:** full code bundle at Windows Desktop `aftlog-review/` (OneDrive Desktop; also `\wsl$` → home/louis/Desktop) + `aftlog-codebase.zip` (3.4MB, secrets-excluded). Paste/upload with the guardrails in `00b-overview.md`/`ARCHITECTURE.md`.
- **Versioning (Decision #11 AMENDED 2026-08-13):** minor = number of shipped features per `FEATURES.md` (currently 50 → **1.50.0+40**). `./build.sh` = patch+1 (1.50.1+41) · `./build.sh --feature` = minor+1, patch→0 (1.51.0+41) — MUST be used for new features with FEATURES.md updated first. Release builds signed with aftlog-release.keystore. Never raw flutter build.
- **Diagram background inconsistency:** Motor = white, Boat/Lower Unit = dark navy, a few gray — Louis to standardize (app is dark `#0B0B0D`) if desired.
- **Editor dropdown sync:** `tools/aftlog-diagram-editor.html` has a hardcoded symptom list — update when flows are added to `symptoms.dart`.

---

## 2026-08-15 — Session 38 — Portal brand polish + site HTTPS + canonical palette

**Portal (aftlog-server v1.118–v1.121, all 22 tests green):**
- **v1.118** — portal was broken out of the box: `--bg/--card/…` only existed under `[data-theme]` so fresh browsers rendered it WHITE; sidebar showed text not the logo; `var(--accent2)` was never defined; `/portal/assets/*` 500'd on binary files (`readAsStringSync` on a PNG). Fixed all four; logo added (trimmed 400px copy of the site logo).
- **v1.119** — red was too faint vs the site (~13–20× less strong red). Red kickers on sidebar group labels, red edge on active nav, red bars on page titles/section h2s, chart bars brightened to `#FF4B4B`, heatmap mids brightened.
- **v1.120** — "faded" + light mode lost detail: dark mode got bigger red stats (34px), red stat-card tops, red table headers, inset card highlights (solid — no gradients), brighter ramps (`#1A1A1F→#FF4B4B`); light mode swapped `#FF4B4B`→`#E02020` (2.6:1 contrast fix), sidebar/topbar follow theme (were hardcoded `#141417`), theme-aware chart colors (`isLight()`), structural contrast (bg `#EDEDF2`, cards white, lines `#D8D8E0`); year-in-review (self-contained page) got the theme system + toggle + logo; removed duplicated `fetchJSON`/theme block.
- **v1.121** — portal logo +25% (sidebar 95px, topbar 48px, year header 65px).

**Site (aftlog-site):**
- `#pain` on load was browser autofill of a previously-clicked anchor — not site code. Added a head script that strips stale hashes on arrival (nav clicks still keep theirs). Deployed.
- **HTTPS was never set up** — GitHub Pages `https_enforced:false`, no cert for `aftlog.com` (edge served `*.github.io`). Louis enabled custom domain in Settings → DNS check passed → cert issued within seconds → **Enforce HTTPS on**. Verified: valid cert on `https://aftlog.com`, www redirects to apex, HTTP→HTTPS redirect propagating (up to an hour).

**Canonical palette LOCKED** (this session): `AftLogColors` Dart class — dark-only, real status colors (`#2ECC71`/`#F5B041`), no Material defaults (`#4CAF50`/`#FFC107`), no accent blue (`#2196F3` NOT in app), no `#B00020`/`#121212`/`#1E1E1E`/`#303030`. Full block added to AFTLOG-CODING-STANDARDS §1. Portal light-theme values documented there as optional cross-platform reference.

**Canonical theme LOCKED** (this session): `AftLogTheme.build()` (Material 3, dark-only) added to standards §1, ready to drop in as `lib/theme/aftlog_theme.dart` + `aftlog_colors.dart`. **Verified compiles on Flutter 3.44.4** (`flutter analyze` clean — after correcting `CardTheme`→`CardThemeData` and dropping deprecated `background`/`onBackground` ColorScheme params).

**Feature #101 SHIPPED** (aftlog-app 1.101.0, signed APK `AftLog-v1.101.0.apk`): Planner Timeline tab with 30/90/365-day bucket windows. Team spec targeted nonexistent `planner_screen.dart`/`planner_logic.dart` (Session 37 rule #1 in action — applied the intent adaptively to `maintenance_planner_screen.dart`): `plannerWindowItems()` pure fn + Timeline tab (This Month | Upcoming | **Timeline** | Seasons), 6 unit tests, analyze clean, full suite 277 pass (2 pre-existing LocalBundleServer localhost failures). FEATURES.md #101 + count→101.

**Still open (unchanged):** MAINTENANCE PLANNER is the next feature · server spec slices (heatmap/clustering/forecast/maintenance/planner/boat-health) · portal deployment decision (Louis) · seed newer portal screenshots into landing site · Aug 24 waitlist gate.

---

## 2026-08-14 — Session 37 — Day-end review + rules locked

**State at end of day (all three repos clean + pushed):**
- aftlog-server @ v1.117 (Trip Patterns) · 22 tests green · CONTRACT.md authoritative for portal codegen
- aftlog-site @ session log current · aftlog-app @ 1.100.0 (untouched today, phone idle)

**NEW RULES LOCKED (from today's sessions):**
1. **Team patches target a template architecture, not this repo** — always `git apply --check` + grep the context before applying; apply the intent adaptively (v1.114 lesson). Generated code must target CONTRACT.md.
2. **Never trust "already exists" in team specs** — v1.116 trip-calendar and v1.117 trip-patterns both claimed an alias already existed; neither did. Check the route table first.
3. **Headless dump-dom hangs XHR under virtual-time-budget** — post-fetch pages (all analytics pages) verify by SCREENSHOT; the homepage is dump-friendly (synchronous skeleton). Don't burn time on dump-dom for analytics pages.
4. **Model may not support images in a session** — pixel/color analysis is the fallback for visual checks; flag "eyeball on phone/desktop" for the human.
5. **CONTRACT.md is the authoritative portal contract** (aftlog-server) — keep in sync with architecture; it documents shell-only portal.js + inline page renderers + URL/API aliases.

**Cleanup done:** lab server stopped; test aftlog.db removed (gitignored, regenerable from test/fixtures/sample_bundle.json).

**Open items (next sessions):**
- Remaining spec slices: trip-heatmap, trip-clustering, trip-forecast, maintenance, planner, boat-health — pattern proven (API → contract containers → portal.js renderers → CSS).
- Portal screenshots for the landing site: today's /tmp/tc-shot.png + /tmp/tp-shot.png can seed screen-portal-* files in ~/aftlog-site/images/ (Louis's call).
- Portal deployment (Render/Railway/Fly/VPS) — still open, Louis's decision.

---

## 2026-08-14 — Session 36 — v1.117: Trip Patterns full spec

**Delivered on aftlog-server, contract-correct (spec said the alias "already exists" — it didn't; created it):**
- **API:** GET /api/v1/aftlog/trip-patterns — frequency (Mon–Sun), timing (0–23 hourly), patterns (early_morning 05–08, late_evening 20+, weekend+weekday = 100).
- **portal.js:** spec renderers (renderFrequencyChart, renderTimingChart via intensityToColor, renderPatternSummary, renderTripPatterns, initTripPatterns). Page: spec sections first, richer existing charts kept below.
- **Verified:** API shape (7+24 entries, pcts sum 100); screenshot rich render + red-fill pixel analysis (model can't view images, so pixel-count check instead).
- Tests: +1 → **22 total green.** Pushed.

---

## 2026-08-14 — Session 35 — v1.116: Trip Calendar full spec

**Delivered on aftlog-server (the team's spec, adapted to the real architecture):**
- **API:** GET /api/v1/aftlog/trip-calendar — 365/366 zero-filled day series + summary (total_trips/hours/distance_km, busiest_day, max_trips_in_a_day). Pure function + route + test.
- **Page:** contract containers tc-calendar + tc-summary added; the spec's 31-column intensity grid + summary card render via new portal.js helpers (intensityToColor, renderTripCalendar, initTripCalendar — with year param); the existing richer 12-month view kept below.
- **Verified via screenshot** (37KB/2145 colors = rich render). NOTE: headless dump-dom hangs on XHR under virtual-time-budget, so post-fetch pages verify by screenshot, not dump — a harness artifact, not a bug (the homepage only looked dump-friendly because its skeleton is synchronous).
- Tests: +1 → **21 total green.** Pushed. SERVER_FEATURES.md updated (116).

---

## 2026-08-14 — Session 34 — v1.114: team ID-rename patch (adaptive)

- **The team's v1.114.patch does NOT apply to this repo** — it was generated against their template architecture, but this repo has a different structure (no per-section containers/init*() functions in portal.js; page logic is inline per HTML file; filenames differ). Verified the mismatch with grep evidence.
- **Applied the intent adaptively:** homepage ids renamed to the contract (home-stats/home-imports/home-boats + JS refs), verified rendering via headless DOM.
- **Wrote CONTRACT.md** in the repo — the definitive frontend contract for generators/team: exact URLs, flat file layout, portal.js = shell only + per-page inline render(), state/chart helpers, theme system, "rules for generated code". Saved v1.114.patch for reference.
- Tests: 20 green. Pushed.
- **Lesson:** before the team generates another patch, point them at CONTRACT.md — patches against the template will keep failing; patches against the contract won't.

---

## 2026-08-14 — Session 33 — v1.113: Unified portal contract (team bundle)

**Applied the team's cut-and-paste bundle against the exact contract** (/portal/assets/, /portal/<name>, /api/v1/aftlog/...):
- **Theme system:** dark/light via data-theme + ☾ toggle + localStorage persistence (brand accents unchanged).
- **Contract aliases added (read-only):** /api/v1/aftlog/stats (year totals) + /api/v1/aftlog/boats (= analytics/boats) + page aliases /portal/maintenance + /portal/planner (bundle nav names).
- **Kept my filled renderers** — the bundle's per-page wiring templates are empty shells; my pages already wire their sections to the API. Flagged.
- Tests: +1 → **20 total green.** Verified live: stats {trips 4, hours 10, 55 km, 19 L}; all alias routes + pages 200; homepage DOM renders grouped sidebar + theme button + boats.
- **Where the portal lives (answered for the team):** local lab only (aftlog-server, dart run → localhost:8080/portal/). NOT on aftlog.com — the landing page is static GitHub Pages and only *describes* the portal. Deploy is the open gap.

---

## 2026-08-14 — Session 32 — v1.112: Sidebar redesign + states + CRITICAL assets fix

**Applied the team's sidebar/state/folder block, with two deviations flagged:**
1. **Icons: emojis rejected** (🏠📊🗓️… — AftLog brand rule: no emojis). Used lightweight inline SVG icons instead.
2. **Folder structure kept flat** — the /portal/<page>/index.html subdir layout is equivalent churn against the current routes; same URLs, same result. Revisit only if deploy-portability demands it.
- **Built:** grouped sidebar (Overview/Trips/Maintenance/Boats) · mobile off-canvas + hamburger topbar · shared showLoading/showEmpty/showError + spinner · initShell wraps every page render in try/catch → friendly error state (no silent blanks).
- **🔴 CRITICAL LATENT BUG FOUND:** /portal/assets/* was never routed → **every page using portal.css/js rendered BLANK since v1.102** (only the self-contained year-in-review worked). The portal-page test checked the <script> tag, not that it loaded. Fixed the route + added a regression test. Homepage screenshot: 5.8KB blank → 42KB real.
- **Lesson:** a test asserting a tag exists is not a test that the page renders — headless-DOM verification caught what unit tests missed. The small-screenshot mystery from Session 28-31 was this bug.
- Tests: +2 → **19 total green.** SERVER_FEATURES.md updated (112). Pushed.

---

## 2026-08-14 — Session 31 — v1.111: Web Portal Homepage

**Delivered on aftlog-server:** GET /portal/ (and /portal) — the 'Welcome back' dashboard:
- Quick stats (trips/hours/distance/fuel from year-in-review) · recent imports list · 9 analytics quick-link cards · per-boat health cards.
- Shared shell: sidebar nav gained a **Home** entry (NAV refactored to objects with hrefs); page reuses initShell for consistent chrome.
- **Loading → empty → error states per section** (fetch failures show a friendly line, no silent blanks) — the polish item the team flagged.
- Wired to existing read-only endpoints only; no app changes. Fixed the spec's broken `<p` tag + used real no-slash URLs.
- Tests: +2 → **18 total green.** SERVER_FEATURES.md updated. Homepage screenshot captured for marketing at /tmp/portal-home.png (move to aftlog-site/images/screen-portal-home.png if wanted).
- **Lessons re-learned:** appending test groups outside main() — third time; the reliable method is rewriting the tail block, not slicing.

---

## 2026-08-14 — Session 30 — Landing page: Web Portal platform story

**Applied the team's landing-page block (5 new sections) with 5 fixes from my review:**
1. **Real screenshots** — the block referenced 4 images that didn't exist. Captured real ones: app dashboard + checklists via adb screencap (Louis's actual phone data), portal Year-in-Review + Boat Health via headless Playwright Chromium against the local aftlog-server (sample Grady bundle). Saved to aftlog-site/images/.
2. **Copy accuracy** — portal health index is "inspired by" the app's score (server index is a simplified variant) · AI has "offline fallback" (Gemini needs network) · bundle copy no longer says "nothing else" (it carries photos/documents).
3. **Pro-tier story fixed** — the block's "if we ever add a true Pro tier" contradicted the app where **$29 IS Pro**; rewrote: free tier (1 boat) + $29 Pro (unlimited, reminders, AI, PDF, Web Portal). Decision #3/#14 consistent.
4. **Nav extended** (Web Portal / How it works / Pro / FAQ) + **mobile nav now scrolls** instead of hiding (existing display:none quirk).
5. Order per team: portal+screens+how after #features, pro after #price, faq before footer. 570 lines, tags balanced, pushed → auto-deploys to aftlog.com.
- **Note for next sessions:** real portal screenshots require the local server running with imported data (documented procedure above).

---

## 2026-08-14 — Session 29 — v1.103–110: Web Portal Analytics Pack

**Delivered on aftlog-server (pushed):** 4 read-only analytics endpoints + shared portal shell + 8 pages.
- **API:** /analytics/trips (per-day/month, weekday-weekend, time-of-day, seasonal, multi-year) · /maintenance (cost-by-month, parts usage, overdue/on-time, health score) · /planner (planned-vs-completed, checklist gauge, consistency, recurring) · /boats (per-boat hours/fuel/cost/trips/compliance + 0-100 index). Services schema gained 'parts'.
- **Frontend:** portal.css + portal.js (sidebar nav, year+boat selectors, cards/tables/SVG chart helpers) + 8 pages under /portal/ (Trip Calendar, Patterns, Heatmap, Clustering, Forecast, Maintenance, Planner, Boat Health). Hand-rolled SVG — zero external deps.
- **Goof recovery:** the user interrupted the first pass ("oops i goofed") and re-sent the corrected spec — resumed cleanly; the earlier build was 95% reusable. Lessons: (1) quoted heredocs don't expand shell vars → the $P stylesheet link silently vanished (test caught it); (2) test expectations must match the actual fixture (all 4 trips are weekdays).
- Tests: +7 → **16 total green** (import/validation/analytics/router/portal). Verified live: all endpoints + pages 200. SERVER_FEATURES.md updated (103–110).

---

## 2026-08-14 — Session 28 — v1.102: Web Portal Year-in-Review page

**Delivered on the local backend (repo now pushed: aftlog/aftlog-server, PRIVATE):**
- `web/portal/year-in-review.html` — self-contained responsive hero dashboard, inline CSS/JS + hand-rolled SVG charts (zero external deps, brand palette): hero cards · totals/averages · efficiency panel + sparkline · seasonal stacked bars · cluster donut · highlights cards · **milestones & badges grid + Share Badge (SVG download)** · recent-trips table · **multi-year line chart** · CSV export + print-PDF · empty-data state · year selector · Pro footer.
- Shelf serves `GET /portal/year-in-review`; buildRouter accepts an injected DB (testable). Router tests: import→review end-to-end, 400/422 paths, page served → **11 tests green**. Verified live (import 200, portal 200).
- Auth/Pro gating stubbed (lab, user_id=1) — wired at deployment.
- **How to see it:** `cd ~/aftlog_server && dart run bin/server.dart` → `http://localhost:8080/portal/year-in-review` (after importing a bundle).
- **Next layers ready to go:** v1.103–110 analytics pack (all against this server).

---

## 2026-08-14 — Session 27 — v1.101C: Local Backend Prototype (Dart shelf + SQLite)

**Louis chose Option C — a lab backend, zero infra commitment.** New repo `~/aftlog_server` (standalone Dart, NOT the Flutter app):
- **Import API** `POST /api/v1/aftlog/import-bundle` — accepts BOTH the app's real backup shape (boats/log_entries/service_records/service_intervals/checklists — the actual BackupService export) AND the spec's idealized shape; validates (400 invalid/missing, 413 >20MB, 422 bad version); normalizes into SQLite with user_id+import_id on every record; malformed rows skipped; returns importId + summary.
- `GET /imports`, `GET /data?year`, `GET /year-in-review?year` (totals/averages/efficiency/seasonal/clusters/highlights/milestones/timeline + multiYear) — the analytics mirror the app's Dart math 1:1.
- Auth out of scope (user_id=1). sqlite3 loader overridden → libsqlite3.so.0 (this box lacks the dev symlink). **8 tests green.** Verified live with curl: import → ok+summary; 400/422 error paths; year-in-review computed 55 km/10 h/19 L/$36.50 from the fixture.
- **Next layers when ready:** v1.102 web Year-in-Review page (consumes /year-in-review), then v1.103–110 analytics pack — all against this local server with zero guesswork. Server repo is local-only (git committed, not pushed); push to aftlog/aftlog-server when Louis wants.

---

## 2026-08-14 — Session 26 — Send to Web Portal (feature #100) → 1.100.0 🎉

**FEATURE #100 — the century milestone.** Delivered (DeepSeek spec, display-only, Pro):
- One-shot JSON bundle export (existing BackupService, no logic changes) + offline transfer options: QR code (qr package via CustomPainter, small bundles only, else 'too large'), USB path, Bluetooth instructions, local Wi-Fi LAN server (dart:io on :8080, stops on close — nothing sent automatically).
- Pro gate: upgrade note + Unlock Pro button for free users. Entry: More → Pro & data (spec said 'Data section' — flagged).
- qr added as a direct dep. Tests: +6 (gating, QR vs too-large, LAN server 200/404 over localhost via raw sockets — dart's HttpClient fought the test env; raw Socket was the fix) → **273 total green.** Built + installed v1.100.0+110 (chunked + MD5).
- **Session tally: 100 features shipped in ~26 sessions today, 273 tests, 26 releases on the phone.**

---

## 2026-08-14 — Session 25 — Trip Year-in-Review + Milestones & Badges (feature #99) → 1.99.0

**Delivered (DeepSeek spec, in the Insights menu — 13th sheet):** annual totals/averages/efficiency, seasonal, clusters, highlights (longest/highest cost/best km/L/busiest month+day), distance + hours + efficiency + activity milestones ([✓]/[ ] checkboxes), earned badge chips, last-10 timeline, summary cards.
- **Flagged:** spec's `Icons.sunny_snowing` doesn't exist in this Flutter version → used `wb_sunny_outlined` for Season Master.
- Tests: +6 → **267 total green.** Built + installed v1.99.0+109 (chunked + MD5). Insights menu: 13 sheets, one tap.

---

## 2026-08-14 — Session 24 — Trip Patterns + Trip Calendar (features #97–#98) → 1.98.0

**Delivered (two DeepSeek specs, shipped together, both in the Insights menu):**
- **#97 Trip Patterns:** weekend/weekday counts+dist+hours, early(Jan–Jun)/late(Jul–Dec), avg distance/hour/fuel per group, morning/afternoon/evening timing (05–11/12–17/18–22), summary cards.
- **#98 Trip Calendar:** month selector, Mon–Sun grid with marker dots, tap-a-day → trip list sheet, monthly totals, per-day intensity bars, most-active day + busiest week + trips cards.
- Tests: +9 → **261 total green.** Built + installed v1.98.0+108 (chunked + MD5). Insights menu now has 12 sheets — still one tap.
- Note: my test expectations twice reflected bad test data rather than bugs (all-July trips → late season dominates; duplicate label strings) — worth remembering: check the DATA before suspecting the code.

---

## 2026-08-14 — Session 23 — Trip Heatmap + Trip Summary (features #95–#96) → 1.96.0

**Delivered (two DeepSeek specs, shipped together):** both land in the consolidated Insights menu (the v1.95 spec's standalone button predates the consolidation — flagged).
- **#95 Trip Heatmap:** seasonal + monthly usage bars (count/max×10, brandRedBright blocks), peak season/month, distance + hours intensity (avg/max), summary cards.
- **#96 Trip Summary:** totals/averages/efficiency/seasonal/cluster distribution/highlights (longest, highest cost, best km/L)/last-5 mini-timeline, summary cards.
- Both pure models + scrollable sheets; zero service/model/logic changes. Tests: +9 → **252 total green.** Built + installed v1.96.0+106 (chunked + MD5). Insights menu now has 10 sheets.

---

## 2026-08-14 — Session 22b — Log tab insights consolidation (1.94.1)

- **Louis approved the consolidation:** the 8 display-only sheet buttons on the Log tab collapse into a single **Insights** button → bottom-sheet menu (Log Insights, Engine Hour History, Fuel Range Estimator, Fuel Cost Insights, Trip Efficiency, Trip Timeline, Trip Clustering, Trip Forecast). Trip/Fuel wizards stay as buttons; forms untouched.
- Note: relocating the menu handler into the right class took several brace-surgery attempts (my python string edits misfired 4× — lesson: use brace-tracking or the edit tool for class-scope surgery, never blind anchor replaces). Resolved via a proper depth-tracking script. **242 tests green.** Built + installed v1.94.1+104 (chunked + MD5).

---

## 2026-08-14 — Session 22 — Trip trio: Timeline + Clustering + Forecast (features #92–#94) → 1.94.0

**Delivered (three DeepSeek specs, shipped together — 1.92 was built but superseded before install; all land in 1.94.0):**
- **#92 Trip Timeline:** chronological trips with distance/fuel/cost/efficiency/cost-per-km/hours/duration/notes + summary cards.
- **#93 Trip Clustering:** short(0–5)/medium(>5–15)/long(>15) km clusters — per-cluster lists + avg distance/duration/km/L + most-common cluster (tie → first max) + seasonal dominance.
- **#94 Trip Forecast:** base averages (skip missing fields), season-aware forecast, short/medium/long hours + fuel bands, efficiency forecast (km/L + fuel for typical trip), summary cards (typical trip / best season = most-active / fuel per trip).
- All pure models + scrollable sheets; zero service/model/logic changes. Tests: +9 → **242 total green.** Built + installed v1.94.0+103 (chunked + MD5).
- **STILL STANDING (3rd time):** Log tab has **9 tool buttons + forms**. Consolidation into a single 'Insights' menu button strongly recommended before release polish.

---

## 2026-08-14 — Session 21 — Trip Efficiency Insights sheet (feature #91) → 1.91.0

**Delivered (DeepSeek spec, fully isolated, display-only):** TripEfficiencyInsights — trip-by-trip km/L + cost/km (missing fields skipped), best/worst trips (hidden without pairs), average trend, seasonal efficiency (mean km/L + cost/km per season), efficiency-vs-distance list (desc, top 10), summary cards (avg km/L, avg cost/km, total distance). Log tab button.
- Tests: +5 → **227 total green.** Built + installed v1.91.0+100 (chunked + MD5). 100th build number milestone.
- **Log tab now has 6 tool buttons + forms — recommend consolidating** (e.g. one 'Insights' button opening a menu of the 5 sheets) before the tab gets unwieldy; Louis's call.

---

## 2026-08-14 — Session 20 — Fuel Cost Insights sheet (feature #90) → 1.90.0

**Delivered (DeepSeek spec, fully isolated, display-only):** FuelCostInsights — per-trip cost (+cost/km when distance logged), cost per engine hour, seasonal breakdown (Spring/Summer/Fall/Winter cost + litres), fill trends (avg/max/min cost, avg price/L), 3 summary cards (total / avg per trip / avg per hour). cost = litres×price with e.cost fallback per spec. 'Avg per trip' = mean of trips-with-fuel-cost (interpretation — flagged). Log tab button.
- Tests: +6 → **222 total green.** Built + installed v1.90.0+99 (chunked + MD5).
- Note: the Log tab now carries 5 tool buttons (Insights, Engine Hours, Fuel Range, Fuel Cost, wizards) + forms — getting busy; consider a collapsible 'Log tools' group or moving sheets under a single 'Insights' menu at some point (Louis's call).

---

## 2026-08-14 — Session 19 — Fuel Range Estimator sheet (feature #89) → 1.89.0

**Delivered (DeepSeek spec, fully isolated, display-only):** FuelRangeSheet — pure `FuelRangeEstimate.calculate` with the EXACT calculator formulas from `_FuelRangeState` (max/risky/safe), live-recompute inputs (Tank prefilled from boat, Reserve 20, Burn rate prefilled from logbook + 'learned from logbook' suffix, Cruise 30, Wind 10, Waves 10), outputs 'Safe/Risky/Max theoretical: X km' + exact explanation + Done. Metric/imperial conversion mirrors the calculator. Log tab full-width button.
- **Flagged:** spec's `fuelBurnPerHour` doesn't exist → used `fuelPerHour`.
- Tests: +5 (formula parity incl. zero-burn/no-reserve, prefill, blank-when-absent) → **216 total green.** Built + installed v1.89.0+98 (chunked + MD5).

---

## 2026-08-14 — Session 18 — Log Intelligence Pack (feature #88) → 1.88.0

**Delivered (DeepSeek spec, fully isolated, display-only):**
- **Log Insights sheet** (pure model + scrollable sheet): Trip insights (count/avg/longest/shortest/most-common destination/avg GPS distance/trip-hours), Fuel insights (litres/avg per fill/avg cost/full-vs-partial/burn rate = litres÷hours), Usage insights (hours/day, seasonal distribution by month, trips/month).
- **Engine Hour History sheet** (pure model): date-sorted rows with running cumulative ('2026-07-14 · +2.5 hrs · 187.0 total'), optional Destination/Distance lines, header total.
- **Log tab:** two more brandRedBright buttons above the wizards.
- **Flagged:** spec's `entriesByType(boatId, type)` doesn't exist → filtered client-side from getEntries (no service change).
- Tests: +10 → **211 total green.** Built + installed v1.88.0+97 (chunked + MD5).

---

## 2026-08-14 — Session 17b — What's New governance + entries structure (1.87.1)

**PERMANENT RULES (Louis's spec, recorded for every future session — What's New updates):**
1. **NEVER auto-add** — only when Louis explicitly provides content.
2. User-visible features ONLY — no refactors/services/bug-fixes/tests/prefs/scoring/dev-notes.
3. Short, curated, plain language, no emojis/jargon.
4. Group by version; never merge/reorder.
5. Append-only; never rewrite old entries.
6. No other About content changes.
7. Exact tuple shape: (version, title, bullets).
8–11. Use EXACTLY the version/title/bullets Louis provides — no guessing.
12. Display-only.

**Implemented (enabling, zero entries added per Rule 1):** `lib/screens/whats_new/whats_new_entries.dart` — empty const + rules header; screen shows latest group when present, else the existing v1.78 items (UX unchanged). Path note: the spec's `lib/screens/about/whats_new.dart` doesn't exist — entries live at `lib/screens/whats_new/` (flagged). Built + installed v1.87.1+96. 201 tests green.

---

## 2026-08-14 — Session 17 — Log Wizards Pack (feature #87) → 1.87.0

**Delivered (DeepSeek spec, fully isolated):**
- **Trip Log Wizard:** destination → hours → optional GPS page (only when a GPS distance exists; injectable for tests) → notes → summary. Pure `buildEntry()` factory; save writes a trip entry (hours, distanceKm when GPS used, destination, notes).
- **Fuel Log Wizard:** litres → price → fill type (full/partial + exact explanation) → notes → summary. Pure `buildEntry()`; save writes a fuel entry. **Spec's litres/price/fillType don't exist on LogEntry** → mapped to fuelLitres/fuelPrice/isFill (+ cost, as the existing form does) — flagged.
- **Log tab:** two brandRedBright buttons above the forms; tab reloads after the wizard pops (LogScreen doesn't listen to BoatEvents).
- Tests: +7 → **201 total green.** Built + installed v1.87.0+95 (chunked + MD5). No LogService/forms/logic changes.

---

## 2026-08-14 — Session 16 — Smart Maintenance Pack (feature #86) → 1.86.0

**Delivered per confirmed adaptation plan (4 spec assumptions didn't exist — RegionService / SafetyGearService / 'Tools → Safety Gear' screen / health-score hook):**
- **Interval Forecasting:** pure model (usage hrs/day from logs, target, predicted due hours + date, region season window via SettingsService.region + regionSeasons) + sheet with exact spec sections; 'Forecast' button under the interval detail header.
- **Safety Gear Wizard:** 7 checkbox pages + final; saves to prefs. Button on **Compliance** (no 'Tools → Safety Gear' exists). Health-score hook **deferred** (needs a scoring change the spec forbids — flagged for a future pack).
- **Seasonal Prep Wizard:** Spring(6)/Fall(4)/Winter(4) exact pages, region-aware; per-season button on Planner → Seasons (Summer none).
- Tests: +13 → **194 total green**. Built + installed v1.86.0+94 (chunked + MD5). #85 reserved per the spec's numbering.

---

## 2026-08-14 — Session 15 — Dashboard Breakdown Pack (features #83–#84) → 1.84.0

**Delivered (DeepSeek spec) with one correction:** the spec claims `score_breakdown_sheet.dart (from v1.83.0)` — it never shipped. The pack therefore builds BOTH:
- **Fuel Range Breakdown** (#84): pure FuelRangeBreakdown model + scrollable bottom sheet (Tank size / Burn rate / Cruise speed / Remaining / Estimated range / Accuracy with exact spec tier text: ≥10 trips High, 4–9 Medium, 0–3 Low + 3 tips + Done). Values compose existing LogService methods only (fuelSince/efficiencyKmPerL/kmPerHour/fuelPerHour/statsForBoat) — display-only, zero service changes.
- **Boat Health Score Breakdown** (#83, the missing v1.83 item): score/status/overdue + the four documented weights (40/35/15/10) as the explanation — HealthScoreService untouched.
- Beginner dashboard: "Breakdown" TextButton (brandMuted, right-aligned) under the Fuel card subtitle AND the Health card — cards otherwise unchanged. Sheets isScrollControlled + scrollable (small screens).
- Tests: +5 → **182 total green**. Analyzer clean. Built + installed v1.84.0+92 (chunked + MD5).

---

## 2026-08-14 — Session 14b — Buying Advisor quiz fix (1.82.1)

- **Louis's report:** quiz question chips ("How will you use it" etc.) couldn't be selected on the phone. **Root cause: the ChoiceChip callbacks never called setState** — taps updated the state fields silently, so the UI never rebuilt (a latent bug since the advisor was built; the Show button masked it because it reads the fields at submit). All 5 questions now wrap handlers in setState.
- Built + installed v1.82.1+90 (chunked + MD5). 177 tests green. **Lesson: no setState in a tap handler = invisible selection — review other screens for the same pattern.**

---

## 2026-08-14 — Session 14 — Instructional Help Expansion (feature #82) → 1.82.0

**Delivered (DeepSeek spec, fully isolated):** HelpTopic gains nullable howTo/examples/tips/where/affects; all 9 topics ship the exact spec instructional content. HelpScreen renders only-present sections in order (Title, Body, Bullets, Where to find it, How to use it as numbered steps, Examples, Tips, How it affects AftLog, Done).

- Tests: +6 → **177 total green**. Analyzer clean.
- **Install complete:** built v1.82.0+89, installed after reconnect (chunked + MD5) — the phone needed a REBOOT (USB re-enumeration loop: MTP window popup cycling; reboot fixed it — add to adb troubleshooting notes). What's New screen fired on this update (1.79→1.82) — live verification of feature #79.
- Repo committed + pushed (app 94fa38e).

---

## 2026-08-14 — Session 13 — Combined Help + Knowledge Base (feature #81) → 1.81.0

**Delivered (DeepSeek spec, fully isolated):**
- `help_content.dart`: HelpTopic gains microTitle/microBody; all 6 original topics got exact micro text; **3 new dashboard topics** (boat_health / fuel_range / journey) with the spec's EXACT micro wording — their full title/body/bullets composed to match the app (flagged; the spec only supplied micro text for them).
- `help_micro.dart`: MicroHelp.show (bottom sheet: microTitle + microBody + "Learn more" → HelpScreen; brand palette; no dialogs/emojis/external links) + MicroHelpIcon.
- `knowledge_base_screen.dart`: lists all 9 topics → HelpScreen; About gains a **Knowledge Base** tile beside What's New (the only About additions).
- **Dashboard micro-help:** info icons on the beginner dashboard's Boat Health Score / Fuel range / Boating Journey cards ONLY — the spec's forbidden placements untouched.
- Tests: +9 → **171 total green.** Analyzer clean. Built + installed v1.81.0+88 (chunked + MD5).

---

## 2026-08-14 — Session 12 — Contextual Help System (feature #80) → 1.80.0

**Delivered (DeepSeek spec, fully isolated):**
- `lib/help/`: `help_button.dart` (help_outline IconButton, brandMuted, always navigates — never a dialog) · `help_screen.dart` (AppBar "Help — {title}", title/body/bullets, stadium Done; unknown topic falls back to planner so Help never renders empty) · `help_content.dart` (6 exact spec topics: planner/analytics/predictive/seasons/logs/safety).
- **Buttons ONLY on allowed screens:** Planner (⋮ bar) · Analytics · Seasons · interval detail · On-the-Water (safety) · Log tab.
- **Two mapped placements (flagged):** the spec's "IntervalDetailScreen" is the planner's bottom-sheet detail (no AppBar) → help icon in the sheet header; the Log tab has no own AppBar (shell's is shared; HomeScreen is on the forbidden list) → help icon top-right of the tab content. Both deviate from "AppBar actions" but are the only compliant options.
- Forbidden screens untouched. +6 tests (topics map + exact wording, screen content, fallback, Done pop, button → right topic). **162 total green.** Analyzer clean. Built + installed v1.80.0+87 (chunked + MD5).

---

## 2026-08-14 — Session 11 — "What's New" screen (feature #79) → 1.79.0

**Delivered (DeepSeek spec, fully isolated):**
- `lib/screens/whats_new/whats_new_screen.dart` + `whats_new_item.dart`: AppBar "What's New in vX.Y.Z" (live PackageInfo), 4 exact v1.78 items (walkthrough / Planner Pro / notifications / dashboard), stadium Done → pop, brand palette.
- **Version tracking:** `last_seen_version` prefs key; main() post-frame `_maybeShowWhatsNew()` waits 1.6s (past the 1.4s splash) and pushes via a new global `appNavigatorKey` (MaterialApp navigatorKey — no screen logic touched). `shouldShowWhatsNew()` pure decision: fresh install (not onboarded) → nothing; returning + version change → show; same version → nothing.
- **Entry:** More → About → What's New ListTile (the only About addition).
- **Deviation flagged:** the spec's literal "lastSeenVersion == null → do nothing" would hide What's New from EVERY existing user on the first update after this shipped — treated null+onboarded as "show" (matches the GOAL: appears once after an update). Louis's own phone proved it: this install showed the screen.
- **Tests:** +7 (4 decision unit tests, screen render + Done pop, About entry, fresh-install routing). The app-level push couldn't be widget-tested (main() also fires PlannerNotifications.check() → SQLite, unavailable in tests) → verified on device. **156 total green.** Analyzer clean. Built + installed v1.79.0+86 (chunked + MD5).

---

## 2026-08-14 — Session 10 — First-launch walkthrough (feature #78) → 1.78.0

**Delivered (DeepSeek spec, fully isolated):**
- `lib/screens/onboarding/onboarding_tour_screen.dart` + `onboarding_tour_card.dart`: PageView 4 cards (Welcome w/ logo, Planner, Safety tools, Offline-first — exact spec text), dots, Next, always-visible Skip, Done on last, stadium buttons, brand palette, no emojis.
- `_FirstRun` (main.dart): new `onboarding_tour_complete` key — not-onboarded users see the tour once, then the existing OnboardingScreen. Existing `onboarded` flag untouched; onboarded users never see the tour; back exits via root route (same as existing onboarding).
- Tests: +6 widget tests (first launch shows tour; 4-card walkthrough; Skip/Done → complete + existing onboarding; relaunch skips; preset skips; onboarding unaffected). **149 total green.** Analyzer clean. Built + installed v1.78.0+85 (chunked + MD5).
- **Deviations flagged:** (1) spec's FEATURES.md number "60" was stale (taken) → shipped as #78; (2) the onboarded→Splash branch needs SQLite to widget-test, so that pre-existing path is verified manually (tour gates only the not-onboarded path, which IS tested).

---

## 2026-08-14 — Session 9 — Planner Pro slices 2–5 (features #74–77) → 1.77.0

**Delivered all four remaining Pro slices in one pass (Louis: "do them all in order"):**
- **#74 Multi-Season Planning (Pro):** `planner_season_service.dart` (boatSeasons, seasonalChecklistFor, intervalsInSeason — pure) · planner tabs **This Month | Upcoming | Seasons (Pro)** (Seasons gated → ProUpgradeScreen; free tier keeps all buckets on the Upcoming tab) · `planner_seasons_screen.dart` (per-season checklist open + predicted intervals; hours-based items stay in buckets).
- **#75 Analytics (Pro):** `planner_analytics_service.dart` (hours-between gaps, cost per service/season/boat, frequency — pure) · `planner_analytics_screen.dart` (CustomPaint bar charts, zero deps) · planner overflow + Boat detail entries, gated.
- **#76 Predictive (Pro):** `planner_predictive_service.dart` (avg hours/day from logbook, predictedDaysUntilDue, predictedText) · summary-card PRO badge + predicted line · interval-detail Predicted row · Pro-gated **"Predicted due soon"** notification (id 9014, once per item per cycle).
- **#77 Cloud sync seam (Pro):** `planner_sync_service.dart` — buildPayload (intervals/history/logs/boats, deterministic) + disabled no-op sync(); tests assert payload shape + no behavior change.
- Settings → Pro & data gains **"Planner Pro features"** checklist when Pro active. Free-tier behavior untouched throughout.
- Tests: +19 → **143 total green**. Analyzer clean. Built + installed v1.77.0+84 (chunked + MD5).
- **Deviation note:** 1.74.0–1.76.0 were consumed as pre-set bumps (established pattern) — all four features ship in 1.77.0; FEATURES.md audit trail intact.

---

## 2026-08-14 — Session 8 — Planner Pro: Slice 1 Export (feature #73) → 1.73.0

**Delivered (Planner Pro set, slice 1 of 5):**
- `planner_export_service.dart`: collect() multi-boat (boatId optional) · CSV export (labeled sections: Upcoming tasks w/ planner buckets / Completed & service history / Seasonal tasks / Interval table — ExportService write pattern to Downloads) · PDF share (PdfService pattern, default fonts) · `plannerExportAllowed()` gating helper.
- **UI:** Planner overflow (⋮) → Export planner / Export completed — free users see lock + (Pro) label → ProUpgradeScreen upsell → then CSV/PDF chooser sheet for Pro. Boat detail → Maintenance → "Export maintenance (Pro)" (boat-scoped CSV).
- **Documented adaptation:** the spec's "Completed timeline → overflow" is folded into the planner overflow (the Completed section shares the planner screen/app bar — no separate overflow exists).
- Tests: +5 (bucket rows across 2 boats, 4 CSV sections in order, completed-only, gating) → **124 total green**. Analyzer clean. Built + installed v1.73.0+81 (chunked + MD5).
- **Next slices:** 2 Multi-Season · 3 Analytics · 4 Predictive · 5 Cloud-sync seam — awaiting Louis's go.

---

## 2026-08-14 — Session 7c — Settings notifications restyle (skeleton UI) → 1.72.2

- **DeepSeek UI skeleton applied to More → Settings → Maintenance notifications:** per-toggle icons (notifications_active / priority_high / schedule / ac_unit / calendar_today), skeleton labels + subtitles, section header "Maintenance notifications", and ONE "Quiet hours" tile (nights_stay) showing the live range and opening a start→end picker dialog via the new `NotificationService.pickQuietHours(context)` (replaces the two separate picker tiles).
- **New service wrappers:** setMasterEnabled / setDueEnabled / setDueSoonEnabled / setSeasonalEnabled / setMonthlyEnabled → PlannerNotifSettings.
- **Deviations (flagged):** the skeleton's `await` inside build() is invalid Dart — kept the working FutureBuilder pattern with the skeleton's structure/icons/labels. pickQuietHours needed mounted-guards around both async gaps (analyzer).
- 119 tests green, analyzer clean. Built + installed v1.72.2+80 (chunked + MD5).

---

## 2026-08-14 — Session 7b — Notification wrapper layer (DeepSeek skeleton compat) → 1.72.1

- **Louis's wrapper-layer spec applied** — thin API-compat methods on NotificationService so the file shape matches the DeepSeek skeleton. Zero behavior/persistence/lifecycle changes; all wrappers delegate to the shipped logic (settings, quiet hours, queue/dispatch, triggers → deduped global check(), persistence compat accessors on a `planner_ts_*` namespace).
- **Intentional non-adoptions (flagged):** skeleton's in-memory last-fired maps NOT adopted (they'd re-fire every process restart — prefs dedupe stays the active mechanism); sync getter signatures impossible (SharedPreferences is async) → wrappers are Future-based.
- +5 wrapper tests (settings defaults, quiet hours TimeOfDay, overnight check, persistence round-trip, queue) → **119 total green**. Analyzer clean. Built + installed v1.72.1+79 (chunked + MD5).
- Note: trigger wrappers delegate to check() which touches SQLite — not unit-testable; exercised on device.

---

## 2026-08-14 — Session 7 — Planner notifications (feature #72) → 1.72.0

**Delivered (v1.72.x spec):** state-transition local alerts, all logic in notification_service.dart (existing service extended — the spec assumed a new file; it already existed from Sessions 2–4).

- **4 types, once per cycle:** Due (isDue transition) · Due Soon (isDueSoon && !due) · Seasonal (active window OR within-7-days) · Monthly Planner Summary (first launch of month, This Month bucket non-empty). Dedupe keys: last_due_notif_{boat}_{interval} (cleared when no longer due → re-arms after Mark as Done), due-soon twin, last_seasonal_notif_{season}_{year}, last_monthly_notif_{YYYY-MM}.
- **Multi-boat aggregation:** simultaneous items → one alert ("2 items due — Oil change, Gear oil (Bluefin)").
- **Settings → Notifications** (More → Settings, the one allowed screen): master (ON) + 4 sub-toggles (ON) + quiet-hours pickers (22:00–07:00).
- **Quiet hours:** skip delivery + dedupe, queue; next app-open after 07:00 delivers still-due items. DEVIATION (documented): no zoned scheduling — that needs the timezone dep + exact-alarm permission; app-open delivery keeps it offline-first with zero new deps. Flag if Louis wants true 07:00 background delivery later.
- **Trigger:** app launch only (main.dart post-frame — bootstrap, no screen modified per §8). Existing daily digest + Pro daily check-in untouched.
- **Tests:** 15 new (due once, re-arm cycle, due-soon once, due-wins, seasonal once per window, near-season, monthly once per month + empty bucket, quiet hours incl. overnight + defaults, aggregation, master/due/seasonal toggles) → **114 total green**, analyzer clean.
- Built + installed v1.72.0+78 (chunked + MD5).

---

## 2026-08-14 — Session 6 — Maintenance Planner (feature #71) → 1.71.0

**Delivered (Louis's FINAL SPEC):** unified maintenance hub. Menu: More → Logs & maintenance → **Maintenance Planner** (end of section, both modes).

- **Summary header:** Next service (min remaining across boats — "Oil change — due in 12 hrs"), overdue count, next seasonal event ("Winterization starts in 3 weeks" / "Spring prep is in season"), last service (relative).
- **5 buckets:** Due Now / Due Soon / This Month / Seasonal / Later, each with "Nothing here right now" when empty. Active seasonal task also appears in Due Now (per spec). Bucket logic = existing isDue/isDueSoon + 30-hr/30-day This-Month window; no-baseline (never done) → Later.
- **Multi-boat:** All Boats / per-boat filter chips; boat names on every row + completed entries.
- **Detail sheet:** interval/category/threshold/last done/current hours/countdown + **Mark as Done** (writes a ServiceRecord + updates the interval baseline → item leaves Due buckets, Completed timeline gains it) + **View Parts / Manuals / DIY**.
- **Pure logic extracted + 10 unit tests** (bucket assignment, remaining, relative days, season text, month label) → 99 tests green, analyzer clean.
- **Flagged deviation:** spec says don't modify existing screens, but "pre-filtered" navigation needs hooks — added OPTIONAL additive params (default null, zero behavior change): PartsLocatorScreen.initialCategory (highlight + auto-scroll), ManualFinderScreen.initialQuery (pre-fills search), DiyLibraryScreen.initialQuery (filters articles).
- **Observed (not fixed, spec says don't change models):** ServiceInterval.isDue() months path uses DateTime.now() internally, ignoring the now param (latent quirk; harmless in production since the app always uses real now).
- Built + installed v1.71.0+77 (chunked + MD5).

---

## 2026-08-14 — Session 5m — Email: single address + auto subject (CatchTales pattern) (1.70.9)

- **Louis remembered the CatchTales pattern mid-install (stopped me):** one address for everything (`catchtales@yahoo.com`) + **auto pre-filled subject line** per context — yahoo auto-sort filters on the subject, not on separate addresses. Verified in ~/CatchTales: Contact Us (no subject), "Report wrong tackle photo" (subject), "Wrong tackle photo - {name}" (subject), Pro purchase (subject + body).
- **Applied to AftLog:** single inbox `aftlog@yahoo.com` · About → Email Support = `?subject=Support` · Manual Finder = `?subject=Manual%20request`. All concatenated/hyphenated/plus variant addresses (5k–5l) are dead — superseded. Addresses stay hidden in the UI.
- **Rule recorded:** any future mailto in AftLog uses `aftlog@yahoo.com` + a context-specific subject (CatchTales convention), never a second address.
- Built + installed v1.70.9+76 (chunked + MD5). 89 tests green. (1.70.8 was built but superseded before install.)

---

## 2026-08-14 — Session 5l — Email addresses corrected: hyphens not plus-tags (1.70.7)

- **Louis corrected the address format:** the auto-sort addresses are **hyphenated** (`aftlog-support@yahoo.com`), not plus-addresses — my 5k implementation used the plus form he'd given earlier. Both mailto usages updated: About → Email Support + Manual Finder "Can't find it?" → `aftlog-support@yahoo.com`. Addresses stay hidden in the UI.
- **CORRECTED address registry:** `aftlog-support` (in use: About + Manual Finder) · `aftlog-bugs` · `aftlog-diagnostic` · `aftlog-pro` · `aftlog-feedback` · `aftlog-suggestions` · `aftlog-attachments` — all @yahoo.com, hyphenated. (Earlier plus-address version superseded — this is the source of truth.)
- Built + installed v1.70.7+75 (chunked + MD5). 89 tests green.

---

## 2026-08-14 — Session 5k — Manual finder mailto fixed (1.70.6)

- **Louis's catch confirmed:** the Manual Finder's "Can't find it? Ask us" mailed the dead **hello@aftlog.com** (aftlog.com has no mail server). Swapped to **aftlog+support@yahoo.com** (chosen from Louis's list — manual requests = support bucket) with the same hidden mailto pattern: To: + "Manual request" subject pre-filled, address never shown in the UI.
- **Plus-address registry (Louis's yahoo auto-sort):** support ✓ in use (About Email Support + Manual Finder) · bugs / diagnostic / pro / feedback / suggestions / attachments — reserved for future surfaces.
- Built + installed v1.70.6+74 (chunked + MD5). 89 tests green.

---

## 2026-08-14 — Session 5j — Support one-tap + Email Support button (1.70.5)

- **Louis's 3 fixes:**
  1. **One less tap** — More → Support now opens the About screen DIRECTLY (the intermediate "About AftLog" tile is gone). MoreSectionKind.support removed; More tab = 6 sections + Support tile.
  2. **MLD logo buffering** — 12px gap added between "Maison Louis Design" and the logo (was hugging).
  3. **Email Support button** (Icons.mail_outline — first envelope icon in the project) with the **hidden plus-address** mailto:aftlog+support@yahoo.com → opens default mail client, To: pre-filled, empty subject/body, address never shown in UI. Louis's "don't want people to see the address" also removed the visible aftlog@yahoo.com link (his intent overrides the spec's "don't remove items").
- **NOTE flagged to Louis:** manual finder's "Can't find it? Ask us" still mails **hello@aftlog.com** — probably should also become the hidden plus-address; awaiting his call.
- Build quirk: two failed builds (my enum/overload typos) consumed 1.70.3/1.70.4 → shipped as **1.70.5+73**. Installed (chunked + MD5). 89 tests green.

---

## 2026-08-14 — Session 5i — About screen corrections (1.70.2)

- **Louis's fixes to the About screen (his own spec had errors):**
  1. **One window** — AftLog logo (assets/images/aftlog-logo.png, 120px) at the top with the tagline underneath; the big text heading removed.
  2. **Version** — already LIVE via package_info_plus (auto-updates every build); the spec's "1.70.0" was never hardcoded in the app. Confirmed to Louis.
  3. **Company link unseen** — the visible URL text is gone; the **MLD logo** (mld-logo.webp copied from catchtales-site, 72px) is now the clickable link to louismales-a11y.github.io. Name "Maison Louis Design" kept as text.
  4. **Support email corrected** to **aftlog@yahoo.com** (mailto). (The support@aftlog.app address came from Louis's own DeepSeek spec — flagged so he knows it wasn't invented by me.)
- assets/images/ is already fully declared in pubspec so both logos bundle automatically. Built + installed v1.70.2+70 (chunked + MD5). 89 tests green.

---

## 2026-08-14 — Session 5h — Nav label wrap fix + About AftLog screen (1.70.1)

- **Bug (Louis):** bottom-nav item 1 wrapped — "Dashboard" rendered as "Dashboar" + "D". Root cause: S23 has Android **font_scale 1.3**; M3 NavigationBar labels scaled to ~15.6sp and wrapped in the ~90px tab. Fix: clamp the bar's text scale (MediaQuery textScaler) so labels stay one line at any system font size; icons + AppBar title still scale. (Device also has density 450 — noted for future UI checks.)
- **About AftLog (DEEPSEEK FINAL SPEC — exact text):** new `AboutScreen` — tagline, "What AftLog helps you do" (7 items), Offline-first, Privacy, Version, Company (Maison Louis Design + louismales-a11y.github.io link), Support (support@aftlog.app mailto), Legal paragraph. Version renders the LIVE app version via package_info_plus (the old dialog hardcoded 1.0.0 — stale). Support tile now pushes the screen; company/support links tappable (url_launcher). package_info_plus promoted to a direct dependency.
- Built + installed v1.70.1+69 (chunked + MD5). 89 tests green.

---

## 2026-08-14 — Session 5g — Mode-switch onboarding (FINAL SPEC §5–§6, feature #70) → 1.70.0

- **Final More-menu spec delivered.** Checked §1–§4 + §7 against what 5e/5f already shipped: 7 sections, exact order/labels, drill-down, beginner/power variants — ALL already live, zero changes needed.
- **New (Spec §5–§6):** `ModeOnboardingScreen` (full-screen, exact text — Beginner: "AftLog is now in Beginner Mode" / Power: "Full tools unlocked", body, 4 bullets, footer; brand-styled, Continue pops). Trigger logic: toggling Beginner Mode in Settings arms `hasSeenBeginnerOnboarding` / `hasSeenPowerOnboarding` (reset to false); the NEXT More section entered shows it once, then never until the next toggle. Never shown immediately on toggle.
- Files touched: more_section_screen.dart (initState hook + toggle handler), new mode_onboarding_screen.dart. Everything else untouched per §8. Built + installed v1.70.0+68 (chunked + MD5). 89 tests green.

---

## 2026-08-14 — Session 5f — More tab = section index (1.69.1)

- **Louis's handback on 5e:** even the 7-section list was still "long and overwhelming" — he wanted just the section headers visible. More tab is now **7 short tiles** (icon + name + one-line hint); tapping a section opens its items in its own screen (`MoreSectionScreen`).
- New `lib/screens/more_section_screen.dart` (MoreSectionKind enum + per-section item lists, beginner variants, all handlers moved); `more_screen.dart` is now just the index. Emergency contact loads from prefs on open (subtitle now correct on cold start). "Logs (fuel & trips)" pops the section then switches to the Log tab.
- Navigation, icons, gating, seasonal logic unchanged. Built + installed v1.69.1+67 (chunked push + MD5 verify). 89 tests green.

---

## 2026-08-14 — Session 5e — More menu rewrite + standalone Diagnostic report (feature #69) → 1.69.0

- **Louis's DeepSeek spec applied:** 12 sections → 7 (On the water / Checklists & setup / Tools & diagnostics / Logs & maintenance / Settings / Pro & data / Support). Exact labels per spec (Launch/Retrieve/Towing **checklist**, **System diagrams**, **Units & measurement**, **Reset setup**, **Restore backup**, **Seasonal checklists**). Navigation targets, icons, Pro gating, seasonal logic untouched.
- **Beginner Mode rules per spec:** Tools & diagnostics → Symptom decoder / Diagnostic report / Ask AftLog / System diagrams / Handling guides / Glossary; Pro & data → Unlock Pro + Load demo data only.
- **One deviation (flagged to Louis in commit + summary):** the spec lists "Diagnostic report (PDF)" but no such menu item existed — built a standalone `DiagnosticReportScreen` (drive chips + symptom picker + Generate report → summary; PDF still Pro-gated per D14). Only new code in the change.
- **Seasonal checklists:** the dynamic per-season row (Spring prep / Winterization — never both) is now titled "Seasonal checklists" with the season name as subtitle; visibility logic unchanged.
- **Adaptation:** power-user title stays "Pro unlocked" when already Pro (spec's "Unlock Pro" is the free-state label).
- Built + installed v1.69.0+66 (chunked push + MD5 verify — the reliable method now). 89 tests green.

---

## 2026-08-14 — Session 5d — PDF preview on phone (1.68.3)

- **Louis's ask:** generating the PDF jumped straight to the share sheet — he wants to VIEW it on the phone. Now Generate PDF → full-screen `PdfPreview` (printing package, already a dep) with built-in **share + print** actions in its action bar; fixed A4 (no page-format/orientation switching). `DiagnosticPdfService.share()` removed (screen generates bytes → navigates to preview; service is generation+filename only).
- **adb transport lesson (UPDATE the old note):** kill-server alone was NOT enough today — the phone silently dropped full-APK pushes ("1 file pushed" but file never landed; version stayed old). **Reliable path on this S23: chunked push (8MB parts) → verify chunk count (10) → cat on device → md5sum match → pm install.** Small pushes land, big ones vanish. Installed v1.68.3+65, MD5-verified, running.

---

## 2026-08-14 — Session 5c — PDF gated behind Pro (Decision #14 LOCKED) → 1.68.2

- **Louis's call:** summary screen stays FREE (safety & learning, per D12); **PDF generation is PRO-only** — industry-standard diagnostic-report pattern. The on-screen narrative + diagram thumbnail remain the free adoption hook; the shareable artifact is the Pro value.
- Implemented: button shows lock + "Generate PDF (Pro)" when locked; tap → ProUpgradeScreen (existing pattern); upgrade-and-generate in one flow on success. Dev builds auto-unlocked (kDebugMode) so testing is unaffected.
- Recorded: **Decision #14 in DECISIONS.md** (LOCKED), FEATURES.md #68 notes Pro. Built + installed (v1.68.2+64). 89 tests green.
- Revisit only if Gate 0 data suggests free PDF would drive sharing/virality.

---

## 2026-08-14 — Session 5b — Diagnostic Report PDF (Phase 2, feature #68) → 1.68.0+62

**Delivered:** shareable A4 PDF of the Diagnostic Assistant Report. Engine untouched (Phase 1 intact).

- `lib/services/diagnostic_pdf_service.dart`: generate() + share() (Printing.sharePdf — same pattern as PdfService; the spec's `saveAndShare` doesn't exist in this codebase). Exact locked section headers, exact order, diagram thumbnail at top only, footer-only branding. Filename: `diagnostic_report_YYYY-MM-DD_HHMMSS.pdf`.
- **Diagram thumbnail wired from real data:** `diagnosticDiagramMap` built from diagram_data.dart (overview + 63 hotspot symptom links) → symptom → WebP asset (e.g. Overheating → cooling_system.webp). "Won't start" has no system art — correctly absent, PDF renders without diagram.
- Summary screen: **Generate PDF** button (spinner while generating, error SnackBar on failure); screen gained optional `symptomKey` param (the spec's snippet needed a key Phase 1 didn't carry); "PDF coming later" footnote replaced.
- **Spec adaptations (judgment calls, documented):** (1) no `PdfService.saveAndShare` — followed the existing sharePdf pattern instead; (2) NO PdfGoogleFonts — runtime font download breaks offline-first, and no existing report uses it; (3) spec's `_theme()` had `await` in a non-async static — moot without font loading.
- **Font fix:** default PDF fonts can't draw em/en dashes or curly quotes (—, –, “”) — ASCII-sanitized at the PDF boundary so the report renders clean; the on-screen summary keeps the real characters. Verified: WebP embeds fine in pdf 3.13 (test renders the real cooling_system.webp).
- Tests: 89 (5 new — PDF magic bytes, WebP embed, diagram map, filename format). Analyzer clean. Built + installed on phone (v1.68.0+62).
- **Not gated:** PDF is FREE (spec marked Pro gating optional; UI snippet had none). Louis: 3-line add if you want PDF Pro-only — say the word.

---

## 2026-08-14 — Session 5 — Diagnostic Assistant Report (Phase 1, feature #67) → 1.67.0+60

**Delivered (app repo, commit to follow):** narrative engine + summary screen. Phase 1 ONLY — PDF is Phase 2, deliberately not built.

- **Feature spec implemented as given** (Louis's DeepSeek input block): `DiagnosticNarrative` + `DiagnosticInput` models, `DiagnosticEngine` with the 7 section builders, the 7 locked template functions, exact section headers, 1–3 sentence template prose (13 total).
- **Adapted to the real codebase:** the spec assumed `SymptomDecoder.meaning()/causes()/userChecks()/mechanicChecks()/risk()` and a `SymptomEvent` type that don't exist — symptoms are `symptoms.dart` string keys with `startFor/causesFor/fixesFor/stopFor/fallbackFor/mechanicNoteFor` helpers. Engine wires: meaning = category + start line · logs = new `LogAnalyzer.summarize()` (trips/fills/hours/distance, unit-aware) · causes = per-drive list · user checks = start line · mechanic = category + drive label + mechanic note · risk = stop conditions + fallback · photos = gallery snapshot. Data strings get trailing-period-stripped so template punctuation never doubles.
- **Entry point:** "Get a report" button on `SymptomFlowView` → covers Symptom decoder, diagram hotspot sheets, and On-the-Water in one place. Loads primary boat + recent logs/services/photos from local SQLite, builds narrative, pushes `DiagnosticSummaryScreen` (brand-styled cards, exact headers, "PDF coming" footnote).
- **Latent bug found + fixed:** `causesFor`/`fixesFor` in `symptoms.dart` cast `'causes': {}` (the 3 safety-only symptoms — Alarm/beeping, Taking on water, Smells like gas) to `Map<String, List<String>>` and CRASHED at runtime — the decoder would have hit it too. Now null-safe; regression test added.
- **Drive fix:** `boat.driveType` stores the enum NAME (`outboard2Stroke`) but decoder lists are keyed by CATEGORY (`outboard`) — engine converts via `DriveType.fromName().category` before lookup.
- **Tests:** 84 total (was 70) — 13 engine tests (sections non-empty, template prose 2 sentences/section + photos 1 → 13 total within 8–14, friendly openings/closers, no dealership jargon, empty-logbook line, real-log summary, exact photo sentences, safety-symptom fallbacks, drive labels) + 1 symptoms regression.
- **Versioning:** FEATURES.md was stale (said 59, app at 1.66.1) — backfilled 60–66 from git history + added 67, count header fixed → `./build.sh --feature` → **1.67.0+60**, signed release built, badging verified (com.aftlog.app, versionCode 60).
- **Housekeeping:** scrubbed a partial Gemini key fragment (`AQ.Ab8RN6…`) from this public site repo's session file — key stays in pass only. NOTE for Louis: this file is PUBLIC (site repo) — keep it free of secrets.
- **Not done (known state):** deep-screen translations still EN (Rule 3 pass at release, unchanged); PDF = Phase 2; phone install pending (USB).

---

## 2026-08-13 — Session 4 — Diagrams shipped + editor pipeline + versioning overhaul

**Version arc: 1.0.38 → 1.50.0** (versioning scheme changed, Decision #11 amended). Phone on 1.0.38; repo at 1.50.0+40. Committed + pushed (app `0b64b0b`).

### Features shipped
- **Troubleshooting Diagrams (feature #34 — the advisor "wow" item):** 19 generic system diagrams (Motor 7 / Lower unit 4 / Boat 8) with Louis's original art. PNG→WebP q90 (38.6MB → 5.8MB, 85% smaller; masters kept at `~/aftlog/images/diagrams-src/`) · **79 hotspots** (circle + rect shapes, normalized coords, disc hit-testing for circles) · viewer: pan/zoom (InteractiveViewer), runtime aspect-ratio fit (art ships at 3:2, 5:4 and square), no-art fallback canvas, bottom-sheet flows with drive branching · More → Diagnostics & tools → Diagrams.
- **Symptom knowledge base extracted** to `lib/data/symptoms.dart` — shared by decoder + diagrams (decoder slimmed 491→~200 lines, zero behavior change). Flows **19 → 25**: added Air intake, Oil pressure, Freshwater, Livewell, Navigation lights, Trailer wiring (starter content, Louis corrects).
- **Diagram editor (dev tool, not in the app):** single-file HTML `tools/aftlog-diagram-editor.html` (+ Desktop copy) — load WebP/PNG, drag-drop JSON + image, add/move/resize circle+rect hotspots, 10% grid, inspector (name/id/check/flow/shape, normalized coords), import/export JSON, light preview mode.
- **Codegen pipeline:** `tools/dart_to_hotspots.py` ⇄ `tools/hotspots_to_dart.py` (JSON ⇄ `diagram_data.dart`; round-trip verified identical). Editor exports JSON → script regenerates Dart → app stays compile-time-safe, no runtime JSON parsing.
- **Asset fix (CatchTales subdir lesson):** pubspec now declares `assets/images/diagrams/{motor,boat,lower_unit}/` explicitly — nested subdirs are silently skipped otherwise (caught by APK inspection: 0 webp bundled until declared).

### Versioning overhaul (Decision #11 AMENDED — Louis's call)
- **New rule: minor = number of shipped features.** `FEATURES.md` (in app repo) is the canonical inventory — **50 features**, script-verified 1–50. `./build.sh` = patch+1 · `./build.sh --feature` = minor+1, patch→0 · major = main redesign · launch = current version at sign-off (old "launch = 1.1.0" marker dropped).
- App re-versioned **1.0.38 → 1.50.0+40** (Diagrams = feature #34). build.sh bump math verified: 1.50.0 → 1.50.1 (patch) / 1.51.0 (feature).

### Review findings (first full code review, Session 4)
- **Verified:** DB discipline (tables in both creation paths), no secrets in git history, Dart 3 switch = no fall-through (report engine safe), analyzer clean (10 pre-existing infos).
- **Real bugs found (backlog, see reminders):** daily check-in dies on reboot (`RECEIVE_BOOT_COMPLETED` missing from manifest) · onboarding can be permanently skipped (prefs flag written before onboarding completes) · free-tier gating not enforced (AI + reminders ungated vs locked Decision #3) · Boats tab stale (no `BoatEvents` listener — standards §9) · `Units` service is dead code (metric toggle half-wired; Calculators/Cost Insights hardcode L/hr).
- **Minor:** manifest `android:label="aftlog"` lowercase · notification icon = full-color launcher icon (should be monochrome) · "contentt" typo in `reference_data.dart` · `test/` empty (12k lines, zero tests — highest-leverage gap).
- **ChatGPT/DeepSeek suggestion reviewed:** WebP already done (their q85–90 rec), diagram cache = Flutter's built-in ImageCache (nothing to build), per-diagram JSON rejected in favor of typed Dart consts + codegen (their hotspots.json idea would add runtime parsing for zero benefit); circle-first editor = good, built with rect support since existing 79 are rects.

### Open / next
- Hotspot alignment via the editor (see reminders #1). Overlays at `~/Desktop/aftlog-diagram-overlays/` (grid + coords version).
- Diagram background inconsistency (white vs dark navy) — Louis's style call.
- Review backlog fixes (reminders #2) — cheap, then one build (plain `./build.sh` → 1.50.1+41).

### Session 4b (same day, afternoon) — hotspots now do something
- **Guided troubleshooting (feature #51):** decision-tree engine (`flow.dart` / `flows.dart` / `flow_screen.dart`) with Won't-start + Overheating trees authored; pattern ready to extend. Reached from symptom sheets + On-the-Water.
- **On-the-Water mode (feature #52):** big red I'M ON THE WATER button (dashboard + More → Safety) → 8-problem grid → safety-first routing (Taking on water → Emergency; guided flow when authored; else symptom sheet; Other → decoder). No emojis (brand rule).
- **Repair logging (feature #53):** "I fixed it / Log this repair" writes a ServiceRecord to the primary boat → service history + resale report. Closes the troubleshoot→log loop.
- **Component purposes:** all 79 hotspots got "what it does" text (editor schema + codegen + sheet display).
- Version: 3 features → FEATURES.md 53 → **1.53.0+42** (pre-set 1.52.0 → `./build.sh --feature`). Built release; phone NOT installed (disconnected, meeting). Committed + pushed `af86c25`.

### Session 4c (same day, late afternoon) — review-batch features (1.56.0)
- **Emergency +2 (spec 4):** Lost GPS + Smoke from engine scenarios (8 total) — free per D12.
- **Next Best Action (spec 3, feature #54):** NudgeService gains triage categories (today / week / before-next-trip); dashboard card groups under urgency headers ("Do this today…"). Pro (nudges are Pro).
- **Boat Health Score 0–100 (spec 2):** composite = intervals 40 / checklists 35 / logs 15 / battery 10 + trend arrow (vs stored score); beginner shows "Your boat health is X/100", boat cards show score/100. FREE per D12 (spec said Pro — corrected).
- **Fuel Range Estimator (spec 9, feature #55):** 6th calculator — safe/risky/max ranges, reserve %, wind/wave loss %, burn rate prefilled from learned logbook fuel use.
- **Handling guides (spec 10, feature #56):** trim / steering / porpoising text guides with symptom-flow links (More → Reference). No art needed.
- Pro gating deferred (Louis); version 56 features → **1.56.0+43** (pre-set 1.55.0 → --feature). Installed on phone. Committed + pushed `f4c937c`.
- **Deferred (spec 8, buying advisor):** data-blank dependent, Phase 2. **Skipped (spec 5):** tools already categorized.
- **Marketing feature list (28 primary, grouped):** created `~/aftlog/MARKETING-FEATURES.md` — INTERNAL, publish-hold until Gate 0 go / Louis sign-off. NOT the version counter (FEATURES.md stays that).
- **Oil mix calculator + Calculators redesign (1.57.0, feature #57):** 2-stroke premix calc (ratios 25/40/50/100:1 + custom, L/gal → ml/oz, quick-pour table, oil-injection warning — Louis's gap catch, not in any prior spec); Calculators page = card picker grid, one screen per calculator. Installed. Committed + pushed `5b8d6b7`.
- **Parts Locator (1.58.0, feature #58 — the affiliate stream):** 14 part categories · US/CA supplier search links (11 suppliers, spec templates) · keyword builder (free = generic, Pro = brand+HP+keyword) · "recommended for next service" (due intervals → categories) · offline common part numbers per brand (starter data, verify-before-buying) · nearby stores = external maps links (no new GPS permission). Dart consts, not JSON. More → Logs & maintenance. Installed. Committed + pushed `8b8ee5b`.
- **Pro upgrade screen + billing seam (1.59.0, feature #59):** single ProUpgradeScreen (price card, what-you-get, unlock, Restore placeholder, honest note that payments arrive at Play launch); `ProService.purchase()` = the Play Billing seam (Decision #2 — one-method swap); all 5 scattered unlock dialogs now route to it; assistant refreshes free-ask banner after upgrade. Installed. Committed + pushed `2fa5dd5`.

---

## 2026-08-12 — Session 3 — Massive build day: beginner layer → wizards → AI → v1.0.36

**Version arc: 1.0.0 → 1.0.36** (auto-bump per build; phone on v1.0.36). Everything below built, analyzer-clean, installed on S23, committed + pushed.

### Features shipped
- **Beginner layer (Decision #9):** Beginner Mode (onboarding choice + simplified dashboard + toggle via `HomeScreen.tabIndex`) · Boat Health Score (green/yellow/red from intervals) · Emergency "What to do if…" (6 scenarios, GPS copy/maps, haptics, timestamp, Retry, Open Settings via app_settings, user-set emergency contact tap-to-call) · Your Boating Journey (6 data-derived milestones + progress) · Pro-gated nudges (gentle interval/battery/engagement + daily check-in notification) · tips of the day.
- **Setup/reset flows:** Reset — Keep All / Delete All (Pro survives wipe) · run-setup-again with checklist dedupe · onboarding back-nav fix (pushAndRemoveUntil Home + push detail).
- **Buying inspection wizard (the flagship):** 13 sections / ~120 items · STEP N OF M header + per-section progress + complete check · Pass/Attention/Fail ratings with **custom vocab per item** (`Label § opt1/opt2/opt3`) · multi-photo evidence (DB v7 `photo_paths` JSON) · full-screen zoom viewer · inline glossary ? (shared glossary data) · header fields (price/hours/year) · **report engine** (score/stars/risk/heuristic repair buckets/offer range/BUY-CONSIDER-WALK-AWAY) · live summary · shareable PDF · reset between viewings.
- **Post-purchase setup wizard:** 11-step guided flow (add boat → 9 rated sections → real interval schedule → optional full inspection → Finish).
- **Launch/Retrieve/Towing big-button modes:** shared `BigButtonChecklist` engine (haptics, reset, unified "Complete — Well Done, Good to Go!"), conditional Towing (trailer owners), first-class placement (dashboard quick actions, boat profile chips, Checklists primary cards, More → Tools).
- **Dashboard v2:** compact brand header (logo 170→34px, tagline kept; beginner dashboard got its brand row back), summary strip (boats/overdue/upcoming/last trip/fill), per-boat health dot + next task, quick actions, buying-lane cards for zero-boat beginners, seasonal chips (Spring Mar–May / Winter Sep–Nov via `SeasonalService`).
- **Wizards out of Checklists tab** (recurring/operational only there); More → Tools regrouped (Buying & inspection / Operational / Seasonal / Logs & maintenance / Diagnostics / Reference).
- **Symptom decoder:** 8→19 symptoms, drive-type branching (outboard/inboard/jet + default), severity tags, "Start here" + safety fallback per symptom — fully offline.
- **AI (Ask AftLog):** Gemini live (key in env) · **grounding** (boat context in prompt + context line) · 10→15s timeout · error taxonomy (no-net/403/429/5xx) · brevity prompt (≤6 bullets/150 words) · 2048 token cap · MAX_TOKENS detection · real "continue" continuation · thinking bubble · auto-scroll.
- **Calculators:** real-world anchor scope (+bow height), voltage-drop % (12/24V + >3% warn), prop-slip color coding + theoretical speed, fuel-burn cruise+WOT, tongue-weight range warnings, sanitized inputs.
- **Manual finder:** 37 categorized links (OEM/libraries/paid/boat-builders/trailers/electronics+safety), search, "can't find it?" mailto.
- **Content passes:** Spring Prep 15→24 items, Winterization 11→19, used-boat buying checklist content; completion message unity ("Complete — Well Done, Good to Go!").
- **Boat specs:** fuelType + maxPersons + maxWeightLbs (DB v8), shown on detail.

### Bug fixes
- **Android 11+ dead links** — manifest lacked VIEW-intent `<queries>` → manual finder/tel:/geo: all silently dead; fixed app-wide (same CatchTales lesson).
- **Location permission never prompted** — geolocator v14 doesn't auto-request; explicit requestPermission + denied/deniedForever distinction + Open Settings.
- **Onboarding-created checklists trapped users** (no back) — now land in shell with checklist on top.
- **AI truncation** — was our prompt/cap bug, not Gemini (see reminders).
- Duplicated-block + DB CREATE-table slips caught by analyzer.

### Repo hygiene
- Purged 136MB tracked build junk (lib/.*.so dumps + root APK-extraction dump); gitignore patterns; 153MB→17MB. History rewrite optional later.

### CoPilot workflow
- Reviews pasted for every area; applied the good/cheap, rejected the over-engineered (Riverpod, template tables, stored derived values, model swaps). Full code bundle at Windows Desktop `aftlog-review/` + `aftlog-codebase.zip` (3.4MB, secrets excluded) — upload with ARCHITECTURE.md guardrails.

### Decision points held (LOCKED, from Session 2)
- Freemium + $29 one-time, no trial (Decision #12) · Gemini stays (no o3-mini yet) · inspection-v2 deferred (YAGNI) · wizards ≠ checklists · lane rule with CatchTales.

---

## 2026-08-12 — Session 2 — Advisor input triaged + decisions locked

### What we did
- **5 real fishermen ("the advisors") reviewed the concept** (met 2026-08-11); their full pitch-style doc pasted into session. Raw reference saved at `~/aftlog/ADVISOR-INPUT-2026-08-12.md` (de-duplicated).
- **Triage (Decision #9, LOCKED):** most of their proposal already exists in AftLog (profiles, checklists, symptom decoder, AI assistant, intervals, winterization, cost insights — they validated the roadmap). **6 genuinely-new ideas adopted into MVP:** Beginner Mode (mode choice + simplified dashboard + toggle), Emergency "What to do if…" button with GPS share, Boat Health Score, behavior-based nudges, progress tracker — and first-time Launch Helper folded into ramp mode. **Rejected:** subscription pricing (kept $29 one-time per Decision #3), revenue projections/"$500K buyer" framing (unverified template claims), weather risk level.
- **Feature lane rule (Decision #10, LOCKED — Louis's call):** the two apps advertise each other; no duplicate features. CatchTales lane = weather/maps/lakes/launches/regulations; AftLog lane = boat care/maintenance/safety/ownership. AftLog hands off weather via CTA ("Check conditions before you launch →") instead of building it.
- Spec updated: new §5.31–5.34 (Beginner Mode, Emergency, Health Score, Progress tracker), nudges in §5.7, weather risk removed, Phase 1 MVP = 5–7 weeks with beginner layer, §6 out-of-scope + Phase 2 updated for the lane rule.
- "Ask a Mechanic" bounty marketplace: researched (JustAnswer is the existing analog); **deferred** — marketplace chicken-and-egg, revisit post-traction.
- **Used-boat buying inspection built (v1.0.6 → v1.0.10):** onboarding path "I'm buying a used boat" + 13-section template; guided wizard (Step N of M, section progress, Back/Next); Pass/Attention/Fail ratings; multi-photo evidence + full-screen zoom viewer (DB v7); live summary card; report engine (score/stars/risk/heuristic repairs/offer range/BUY-CONSIDER-WALK-AWAY) + shareable PDF + Save to My Boats; reset button; inline glossary ? (shared glossary data, 14 new inspection terms); back-nav fix for onboarding-created checklists; CoPilot review incorporated (step flow, section progress, multi-photo, enlarge viewer, live summary) — deferred: visual examples content, dynamic template table + section columns (logged as inspection v2 in spec §5.35; YAGNI until a second inspection type exists).

### Current state
| Item | Value |
|------|-------|
| Gate 0 waitlist | RUNNING (since 2026-08-10, ~2-week countdown → ~Aug 24) |
| Decisions | #1–#10 (9+10 locked today) |
| MVP scope | 5–7 weeks incl. beginner layer (spec §9) |
| App | v1.0.0+1, skeleton complete, on phone |

### Next steps (suggested order)
1. ~~Landing-page copy refresh~~ ✅ **DONE 2026-08-12** — beginner section live on aftlog.com (Health Score, Emergency, Know Your Boat, pre-departure, launch helper, Beginner Mode)
2. ~~Version discipline~~ ✅ **DONE 2026-08-12** — Decision #11: build.sh auto-bumps patch+build per build; release signing switched debug→aftlog-release.keystore (latent gap fixed); v1.0.0+1 → 1.0.1+2, first properly-signed APK verified (fingerprint match)
3. **Build the beginner layer** — Beginner Mode shell first (mode toggle + simplified dashboard), then Health Score, Emergency button, nudges, progress tracker
4. **Louis's blanks** — intervals, checklist items, symptom causes, glossary, prices, quiz weights (drafted placeholders in code/data)
5. **AI key at build** — verify env/pass path works (`api/gemini`); build.sh falls back to offline answers if missing
6. Full translation pass (Rule 3) at release; scheduled due-soon notifications wiring

---

## 2026-08-10 — Session 1 — AftLog launched: foundations → complete structure

### Stage 0 — Foundations (all locked in DECISIONS.md)
- Name **AftLog** ("Keeping your boat shipshape!"), tagline from Louis
- Domains: aftlog.com (primary) + net/info/xyz/store/ca defensive — all registered, DNS on GitHub Pages, 5 forwards to .com
- Bundle ID `com.aftlog.app`; Play dev account under louis.males (MLD account blocked by Google); public dev name = AftLog
- Keystore generated (RSA 4096, alias aftlog), password in pass, gitignored, Desktop backup
- GitHub org `aftlog` + repos `aftlog-app` (private) + `aftlog-site` (public for Pages)
- Distribution: direct APK + private Play track only; public launch gated on Louis's sign-off
- Monetization: free tier (1 boat) + $29 one-time, no ads; 3 streams (Pro + affiliate + content)
- AFTLOG-CODING-STANDARDS.md written BEFORE app code

### Stage 1 — Validation (Gate 0 LIVE)
- Landing page on aftlog.com (black/red/white brand, logo in white chip → then transparent logo directly, big hero logo 262px, slogan between logo and kicker)
- Waitlist form (Formspree xoeaezwv, Ajax, honeypot, fixed success/error styling)
- Updates page at /updates/ + nav wiring; site clone at ~/aftlog-site
- Logo iterations: transparent version made from Louis's PNG; favicons + og:image generated

### App build (aftlog-app, ~50 Dart files / ~6,500 lines)
- 5-tab shell, brand theme (black/red/white), splash, onboarding first-run (3 paths)
- Data: boats/logs/services/intervals/checklists/photos/docs/parts on SQLite (v1→v5), complete in onCreate AND onUpgrade
- Boat hub: profile+photo, engine, documents (expiry), parts, photos timeline, intervals, service history, cost insights, resale PDF, logbook PDF, CSV import
- Log v3 (user-driven design): season stats, **fuel-range brain** — tank size + Fill up (litres + odometer) + GPS Go/Stop tracking (geolocator) or odometer, real km/L + km/hr learned over fill cycles, "X km / Y hrs to empty" + LOW warning; metric/imperial everywhere
- Tools: reminders, AI assistant (Gemini, offline fallback), symptom decoder, ramp mode, 5 calculators, buying advisor (16 styles + quiz), winterization planner (region), float plan, compliance, manual finder, DIY library, battery/electronics, glossary
- Pro gating, backup/restore (JSON), CSV/JSON export to Downloads, local notifications
- Fixes during walkthrough: dashboard stale-list (BoatEvents notifier), 2.6px overflow, checklist card overflows, GPS permission (manifest had NO permissions — silent edit miss!), fill dialog overflow, checklist bottom clipping, "Spring commissioning"→"Spring Prep", "Used-boat inspection"→"Used Boat / Inspection"
- Repo hygiene: removed 80MB debug kernel_blob from git

### Phone
- S23 Ultra (R5CW6256YKL, USB), installed via chunked push; final build on device with everything above
