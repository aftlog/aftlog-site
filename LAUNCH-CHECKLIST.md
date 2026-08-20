# AftLog Platform v1.112 — Launch Checklist + Rollback + Monitoring

Companion to `RELEASE-MANIFEST-v1.112.md` and `INTEGRATION-SPEC.md`
(single source of truth). Run top to bottom before the public launch.

## A. Launch checklist (DEEPSEEK Step 10, Section 8)

| # | Item | Status |
|---|------|--------|
| 1 | URLs swapped — site `PORTAL_BASE=https://portal.aftlog.com`; app default `https://portal.aftlog.com`; no `dev.*` URLs anywhere (audited 2026-08-17) | ✅ |
| 2 | Lighthouse SEO ≥ 95 — **manual, browser** (site + portal; see D below) | ⏳ Louis |
| 3 | Privacy/Terms reviewed — plain-language coverage of data storage, offline-first, AI usage, license (one-time lifetime), user rights, contact. Legal sign-off | ⏳ Louis |
| 4 | Play Store release prepared — `PLAY-STORE-RELEASE.md` (notes + tracks) | ✅ |
| 5 | Portal homepage verified — `tools/portal_check.py` ALL PASS | ✅ |
| 6 | Website pages verified — `tools/site_check.py` ALL PASS (~150 checks) | ✅ |
| 7 | Server proxies verified — live sweep: `/ai/gemini`, `/admin/publish`, `/admin/licenses`, `/ai/health`, `/status` | ✅ |
| 8 | No forbidden tokens — app lib 0, site 0, portal web/ 0, APK probe 0 | ✅ |
| 9 | No direct Gemini/GitHub calls — only `ai_proxy.dart` / `github_proxy.dart` | ✅ |
| 10 | All nav/footer links work — site_check + portal_check | ✅ |
| 11 | All metadata correct — unique titles/descriptions/canonical per page | ✅ |
| 12 | All version numbers correct — Portal/Server/Website v1.112; App 1.109.0+166 (internal) | ✅ |
| 13 | All tests green — server 141, app 429 (+2 known), site 150+, portal 40+ | ✅ |
| 14 | All pages 200 OK — live sweep (site + portal) | ✅ |
| 15 | All proxies online — live sweep | ✅ |

## B. Rollback plan (Section 9)

If production issues occur after launch, in order:

1. **Revert DNS** to the previous portal/dev endpoint (`portal.aftlog.com` → old).
2. **Revert the website** to the previous static build: `git checkout <prev-tag> -- . && git push` (Pages redeploys in ~1 min). Tags exist at every release.
3. **Revert the app** on the Play track: re-release the previous APK on the same track (Play keeps prior releases; promote the last known-good).
4. **Revert the server** to the previous tag (`git checkout v1.110 … && ./start-dev-server.sh`).
5. **Notify users** via the website (banner on `/`) and the portal (hub banner) — one sentence: "AftLog is temporarily degraded; we're rolling back a release."
6. **Fix** the issue on a branch; verify with the full test matrix.
7. **Redeploy** as `v1.112.1` (patch) following this same checklist.

## C. Post-release monitoring (Section 10)

| What | How |
|------|-----|
| Server logs | `/tmp/aftlog-server.log`; grep `[ai-proxy]` / `[publisher-proxy]` |
| AI proxy latency | log lines `latencyMs=` — alert if p90 > 40s |
| Publisher errors | `[publisher-proxy] ok=0` count |
| License activations | `pro_licenses` Firestore writes; `/admin/licenses` list |
| Website traffic | Google Analytics / Plausible (or Pages insights) — **pending: no analytics account yet** |
| Portal usage | server request logs |
| App crash-free rate | Play Console crash reporting |
| SEO indexing | Search Console — submit sitemap after launch |
| Blog traffic | same analytics as website |
| Review count | `GET /admin/publish` → `reviewCount` (also on the portal hub) |

## D. Lighthouse runs (manual — no browser in the dev environment)

Run in Chrome DevTools (Lighthouse tab) on:
- `https://aftlog.com/`, `/features.html`, `/ai.html`, `/portal.html`,
  `/pricing.html`, `/blog/` (targets: Perf ≥ 90, A11y ≥ 95, BP ≥ 95, SEO ≥ 95)
- `https://portal.aftlog.com/` (once deployed)

Known pre-audit notes: hero PNGs are large (~0.2–0.5 MB) — if Performance
dips, convert to WebP/AVIF or add `loading="lazy"` (no palette change).
