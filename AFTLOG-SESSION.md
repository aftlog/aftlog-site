# AftLog — Session Log

> Read `AFTLOG-CODING-STANDARDS.md` + `DECISIONS.md` first every session.

---

## ⚠️ REMINDERS FOR NEXT SESSION

- **Keystore USB backup DONE 2026-08-11** — copied to USB drive `F:` (label AFTLOG-KEYS). Verified: SHA-256 identical across all 3 copies, opens with pass password, alias `aftlog`, fingerprint matches DECISIONS.md. Off-machine copy exists ✅. Password also written on paper with the USB. Full redundancy: key×3 + password×3 (pass/paper/USB).
- **Keystore password ROTATED 2026-08-11 (was exposed in a session transcript)** — new password in `pass` (`aftlog/keystore-password`), fingerprint unchanged (3C:B3:FD:...:01:DF, key untouched). All 3 copies (working/Desktop/USB F:) refreshed + hash-verified (bbecb5a1...) + open with the new password. Paper note updated with the new password 2026-08-11 — rotation FULLY COMPLETE (key×3 + password×3 consistent).
- **Gate 0 waitlist running** — landing page live at aftlog.com (waitlist formspree `xoeaezwv`). 2-week email count decides MVP go/no-go. Countdown started 2026-08-10.
- **Version discipline not yet applied** — app still `1.0.0+1` after many dev iterations. Per standards every change bumps; decide the AftLog release versioning approach before the first release build (suggest: keep dev iteration at 1.0.x, bump when features settle).
- **AI needs a key** — real Gemini answers require `--dart-define=GEMINI_API_KEY=...` at build (same pass entry as CatchTales). Offline fallback answers work without it.
- **Full translation pass pending** — translation service has core strings only; deep screens still EN. Rule 3 pass at release.
- **Push notifications**: in-app reminders + "Test reminder" button work; scheduled due-soon notifications not yet wired (NotificationService has the plumbing).
- **Blanks for Louis to fill** (drafted placeholders, flagged in code/data):
  - Interval amounts (oil/impeller/lower unit/etc. per engine)
  - Checklist item lists (launch/retrieve/towing/winterize/spring prep/used boat)
  - Symptom-decoder causes (8 symptoms)
  - Glossary (15 terms), Compliance rules, Manual links, DIY steps
  - Boat-style prices/running costs (16 styles), buying-quiz weights
  - Calculator assumptions (default 30 km/h cruise, 30 L tank examples)

---

## 2026-08-12 — Session 2 — Advisor input triaged + decisions locked

### What we did
- **5 real fishermen ("the advisors") reviewed the concept** (met 2026-08-11); their full pitch-style doc pasted into session. Raw reference saved at `~/aftlog/ADVISOR-INPUT-2026-08-12.md` (de-duplicated).
- **Triage (Decision #9, LOCKED):** most of their proposal already exists in AftLog (profiles, checklists, symptom decoder, AI assistant, intervals, winterization, cost insights — they validated the roadmap). **6 genuinely-new ideas adopted into MVP:** Beginner Mode (mode choice + simplified dashboard + toggle), Emergency "What to do if…" button with GPS share, Boat Health Score, behavior-based nudges, progress tracker — and first-time Launch Helper folded into ramp mode. **Rejected:** subscription pricing (kept $29 one-time per Decision #3), revenue projections/"$500K buyer" framing (unverified template claims), weather risk level.
- **Feature lane rule (Decision #10, LOCKED — Louis's call):** the two apps advertise each other; no duplicate features. CatchTales lane = weather/maps/lakes/launches/regulations; AftLog lane = boat care/maintenance/safety/ownership. AftLog hands off weather via CTA ("Check conditions before you launch →") instead of building it.
- Spec updated: new §5.31–5.34 (Beginner Mode, Emergency, Health Score, Progress tracker), nudges in §5.7, weather risk removed, Phase 1 MVP = 5–7 weeks with beginner layer, §6 out-of-scope + Phase 2 updated for the lane rule.
- "Ask a Mechanic" bounty marketplace: researched (JustAnswer is the existing analog); **deferred** — marketplace chicken-and-egg, revisit post-traction.

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
