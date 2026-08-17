# AftLog — Play Store Release (Platform v1.111)

App internal version: **1.108.7 (versionCode 154)** · Platform release: **v1.111**
Bundle ID: `com.aftlog.app` · Signing: `aftlog-release.keystore` (see
DECISIONS.md / keystore notes; password in `pass`)

## 1. Release notes (What's New — user-facing, copy-linted)

**v1.111 — the AftLog platform**

- **Smarter AI everywhere.** Ask AftLog now runs through the AftLog
  server — faster, more reliable answers grounded in your boat. Smart
  Planner, diagnostics, manual extraction, and photo assist all use the
  same secure pipeline.
- **Web Portal integration.** Send your log to the portal, see Year in
  Review, planner windows, and boat health in your browser, and link your
  device with a one-time code.
- **Lifetime Pro.** Enter a Pro code once — it's yours forever. AftLog
  Pro is a one-time purchase, no subscription.
- **Review Publisher (dev).** Publish a review straight from your phone to
  aftlog.com.
- **Stability improvements** across logging, checklists, and offline
  storage.

## 2. Tracks (release order)

1. **Internal track** — every dev build (current phone: 1.108.7+154).
2. **Closed track** — invite testers (Louis's S23 Ultra + the advisors).
3. **Production track** — public release, gated on Louis's sign-off and
   the Aug 24 gate decision.

## 3. Store assets

- **Privacy policy URL:** https://aftlog.com/privacy.html
- **Terms:** https://aftlog.com/terms.html
- **Support:** https://aftlog.com/support.html
- **Website:** https://aftlog.com
- **Screenshots** (required on Play, from the phone — existing captures in
  `aftlog-site/images/`: `screen-app-dashboard.png`,
  `screen-app-checklists.png`, `screen-smp-plan.png`,
  `screen-vea-result.png`, `screen-portal-year.png`,
  `screen-portal-health.png`). Recapture on 1.108.7 if any UI changed.

## 4. Pre-upload checks

- [ ] `./build.sh --feature dev`? No — for Play: signed **release** build
      (`./build.sh` default = pro flavor) — never the dev flavor (no dev
      tooling/tokens).
- [ ] APK/AAB probe: no `GEMINI_API_KEY`, no `GITHUB_TOKEN`, no
      `generativelanguage`, no `api.github.com` (verified on the dev build;
      re-verify the pro build).
- [ ] md5 recorded + backed up (keystore + password redundancy per
      DECISIONS.md).
- [ ] What's New copy run through `tools/lint_release_notes.py`.
- [ ] Data safety form (Play Console): no data collected by default;
      optional portal sync; AI questions sent to AftLog server.

## 5. Post-upload monitoring

- Crash-free rate (Play Console).
- License activations (`pro_licenses`).
- Review count (`GET /admin/publish`).
