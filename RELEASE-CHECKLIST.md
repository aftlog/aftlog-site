# AftLog Release Checklist

> Repeatable pre-release process (locked 2026-08-16). Run top to bottom for
> every feature release. Cross-repo: app (aftlog-app), portal
> (aftlog_server), website (aftlog-site).

## 1. Code & features
- [ ] Feature blocks complete (e.g., SMP-1 → SMP-Final) — shipped + reconciled.
- [ ] No forbidden refactors/renames outside planned blocks.
- [ ] Tests pass (note any known, pre-existing failures).
- [ ] Analyzer clean.

## 2. App
- [ ] Version bump: pubspec.yaml + FEATURES.md (e.g., 1.105.x).
- [ ] What's New: written using the template (version/title/description +
      Free/Pro/Improvements); passes `tools/lint_release_notes.py`.
- [ ] Screenshots: free-tier and Pro-tier updated if needed (match tier).
- [ ] Pro flags set correctly for release; free vs Pro behavior verified.

## 3. Portal
- [ ] Changelog updated using the portal changelog template
      (aftlog_server/CHANGELOG.md) — no developer jargon.
- [ ] Docs reflect new features (user-facing language).

## 4. Website
- [ ] Landing page updated using the landing template (hero / overview /
      free vs Pro / how it helps you).
- [ ] FAQ add/updated for new features.
- [ ] Changelog updated (version + bullets).

## 5. Help / knowledge base
- [ ] Help topics added/updated (overview, how-to, troubleshooting).
- [ ] Walkthrough/onboarding updated if the feature is major.
- [ ] Tooltips verified where relevant.

## 6. Language & quality
- [ ] Text lint run (forbidden terms: gating, flags, scaffold, migration,
      DB vX, pipeline, embeddings, confidence score, fallback, etc.).
- [ ] Marketing voice: benefit-focused, user-facing, Free vs Pro labeled.

## 7. Build & install
- [ ] Signed builds generated.
- [ ] Integrity verified (md5).
- [ ] Single install to device (dev/pro flavor as appropriate).
- [ ] Smoke test: new feature flows on device (free + Pro if enabled).

## 8. Logging
- [ ] AFTLOG-SESSION.md updated: features shipped, commits, version
      numbers, flags left off (e.g., Pro features gated for later).
