# AftLog — Session Log

> Read `AFTLOG-CODING-STANDARDS.md` + `DECISIONS.md` first every session.

---

## ⚠️ REMINDERS FOR NEXT SESSION

- **🔴 OPEN ITEMS (see Session 4 for full log):**
  1. **Hotspot alignment:** current 79 hotspots are knowledge-based — align via the editor (`tools/aftlog-diagram-editor.html`): Import JSON from `tools/hotspots/`, load the WebP, drag into place, Export → `python3 tools/hotspots_to_dart.py` → rebuild with plain `./build.sh`.
  2. **Review backlog (Session 4 findings, cheap fixes):** daily check-in dies on reboot (`RECEIVE_BOOT_COMPLETED` missing) · onboarding flag written before onboarding finishes · free-tier gating not enforced (AI + reminders should be Pro per Decision #3) · Boats tab stale (listen to `BoatEvents`) · `Units` service dead code (metric toggle half-wired)
  3. **Data blanks:** interval amounts per engine · glossary check (29 terms) · boat-style prices · buying-quiz weights · calculator assumptions (placeholders in `reference_data.dart`) — incl. boat-style prices/running costs (16 styles), buying-quiz weights, calculator assumptions (default 30 km/h cruise, 30 L tank examples)
  4. **Translations:** core strings only; deep screens still EN (Rule 3 pass at release)
  5. **Pro purchase wiring:** `pro_service.dart` is just a flag — the $29 unlock isn't purchasable yet
  6. **Scheduled interval notifications:** daily check-in works; per-interval due-soon push not wired
- **Gate 0 waitlist running** — landing live at aftlog.com (formspree `xoeaezwv`). 2-week countdown from 2026-08-10 → decision ~Aug 24. Landing already refreshed with the beginner angle.
- **AI is LIVE:** `GEMINI_API_KEY` in env (AQ.Ab8RN6…, same as CatchTales) — builds embed it. Ask AftLog grounded with boat context, brevity enforced, "continue" works, error taxonomy in. Gemini Flash kept (no o3-mini — truncation was our prompt/cap bug; provider switch designed-not-built).
- **Repo hygiene DONE 2026-08-12:** purged 136MB of stray build/APK-extraction junk (lib/*.so dumps + root dex/arsc/META-INF/res); gitignore patterns added; tracked size 153MB→17MB. (History still holds old blobs — optional rewrite like CatchTales later.)
- **CoPilot review workflow:** full code bundle at Windows Desktop `aftlog-review/` (OneDrive Desktop; also `\wsl$` → home/louis/Desktop) + `aftlog-codebase.zip` (3.4MB, secrets-excluded). Paste/upload with the guardrails in `00b-overview.md`/`ARCHITECTURE.md`.
- **Versioning (Decision #11 AMENDED 2026-08-13):** minor = number of shipped features per `FEATURES.md` (currently 50 → **1.50.0+40**). `./build.sh` = patch+1 (1.50.1+41) · `./build.sh --feature` = minor+1, patch→0 (1.51.0+41) — MUST be used for new features with FEATURES.md updated first. Release builds signed with aftlog-release.keystore. Never raw flutter build.
- **Diagram background inconsistency:** Motor = white, Boat/Lower Unit = dark navy, a few gray — Louis to standardize (app is dark `#0B0B0D`) if desired.
- **Editor dropdown sync:** `tools/aftlog-diagram-editor.html` has a hardcoded symptom list — update when flows are added to `symptoms.dart`.

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
