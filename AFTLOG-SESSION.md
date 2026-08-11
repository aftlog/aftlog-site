# AftLog — Session Log

> Read `AFTLOG-CODING-STANDARDS.md` + `DECISIONS.md` first every session.

---

## ⚠️ REMINDERS FOR NEXT SESSION

- **Keystore USB backup DONE 2026-08-11** — copied to USB drive `F:` (label AFTLOG-KEYS). Verified: SHA-256 identical across all 3 copies, opens with pass password, alias `aftlog`, fingerprint matches DECISIONS.md. Off-machine copy exists ✅. Password also written on paper with the USB. Full redundancy: key×3 + password×3 (pass/paper/USB).
- **Keystore password ROTATED 2026-08-11 (was exposed in a session transcript)** — new password in `pass` (`aftlog/keystore-password`), fingerprint unchanged (3C:B3:FD:...:01:DF, key untouched). All 3 copies (working/Desktop/USB F:) refreshed + hash-verified (bbecb5a1...) + open with the new password. ⚠️ REMAINING: update the PAPER NOTE to the new password (`pass show aftlog/keystore-password`).
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
