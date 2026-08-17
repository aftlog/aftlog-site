# AftLog Integration Spec — v1.111 (single source of truth)

> Frozen with Release Manifest v1.111. Every client (App, Portal, Website)
> talks to the server through the contracts below. The server owns all
> credentials. Changes require a new manifest version.

## 0. Conventions

- Base URL: dev server `http://localhost:8080` (app: portal URL from
  More → Link to Portal; website: `PORTAL_BASE`, default
  `https://portal.aftlog.com`).
- Auth: `X-Aftlog-Dev-Key: aftlog-dev` header (lab default; server env
  `AFTLOG_DEV_KEY`). Gate: 403 when missing/wrong.
- Errors: proxy endpoints return `{ok:false, error:"…"}` with a 200/503
  status; clients map:
  - `network` → "Portal server unreachable — is the dev server running?"
    (web: "Portal server unreachable — check server status.")
  - `gemini_unavailable` / `github_unavailable` → "… is temporarily
    offline — portal server or <AI|GitHub> service unavailable."

## 1. AI Proxy — `POST /ai/gemini`

```
Headers: content-type: application/json
         X-Aftlog-Dev-Key: <dev key>
Body:
{
  "prompt": "string (required)",
  "mode": "ask | diagnostic | planner (default ask)",
  "boat": "string (optional boat context)",
  "manual": "string (optional manual page references)",
  "imageBase64": "string (optional vision)",
  "imageMimeType": "image/jpeg | image/png (default jpeg)",
  "extra": { ... }  // optional context; injected into the prompt
                    // (symptom/logs/stats/history…)
}
Response 200:
{ "ok": true, "mode": "…", "answer": "…",
  "details": { "truncated": bool, "finishReason": "…" }, "error": null }
Failure (AI down): 503 or 200 { "ok": false, "error": "gemini_unavailable" }
```

- Server side: `AiProxyService` (in-process for the Portal), Gemini
  `gemini-3.6-flash`, 45s timeout, `AFTLOG_GEMINI_KEY` env.
- Consumers: App `AiService` (Ask AftLog, VEA vision), Portal hub widget +
  Portal `AskAftLogAi` (in-process), Website `/ai` widget.

## 2. Publisher Proxy — `POST /admin/publish` (+ `GET` count)

```
POST /admin/publish
Headers: content-type: application/json, X-Aftlog-Dev-Key
Body: { "type": "review_publish", "review": { name?, boat?, rating, text, preview } }
Response 200:
{ "ok": true, "type": "review_publish",
  "result": { "commit": "sha", "message": "…", "reviewCount": n }, "error": null }
Failure: 200 { "ok": false, "error": "github_unavailable" } | 503 (no token)

GET /admin/publish → { "ok": true, "result": { "reviewCount": n }, "error": null }
```

- Server side: `GithubProxyService`, `AFTLOG_GITHUB_TOKEN` env, writes
  `aftlog/aftlog-site · data/reviews.json`.
- Consumers: App `PublisherService` (dev Review Publisher), Website
  `/portal.html` review badge (GET), Portal hub badge (GET).

## 3. License Manager — server-only, lifetime-only

```
POST /admin/licenses
Headers: content-type: application/json, X-Aftlog-Dev-Key
Body: { "type": "lifetime (ONLY — yearly is refused 400)", "issuedBy": "…" }
Response 200: { "code": "PRO-XXXX-XXXX-XXXX" }

GET /admin/licenses → { "codes": [ { "_id", type, issuedAt, issuedBy, used, usedBy, expiresAt } ] }
```

- Server side: `LicenseService` (single writer), lifetime-only per
  Decision #3. Consumers: App dev License Manager, portal (future).
- Redemption (users): `POST /redeem` (portal session) and
  `POST /redeem/app` (device-linked) — unchanged.

## 4. Portal health — `GET /ai/health` · `GET /status`

```
GET /ai/health → { "ok": true, "available": bool, "message": "online|offline" }
GET /status    → { "ok": true, "name": "AftLog Web Portal",
                   "portalVersion": "v1.111",
                   "aiAvailable": bool, "publisherAvailable": bool }
```

- Unauthenticated, read-only, no secrets. Used by the Portal hub data
  strip and the Website/Portal check matrices.

## 5. Website integration (static, GitHub Pages)

- Ask AftLog widget → `POST <PORTAL_BASE>/ai/gemini` (same body as §1).
- Review badge → `GET <PORTAL_BASE>/admin/publish` (`result.reviewCount`).
- Pricing → lifetime-only messaging (no subscriptions, no expiry).
- Internal links: explicit `.html` URLs (GitHub Pages has no clean URLs);
  `/blog/` and `/updates/` are directories.
- Portal links: `https://portal.aftlog.com/{login,portal/,portal/…}`.

## 6. App integration

- `AiService.ask()` / `analyzeImage()` → `POST <portal>/ai/gemini`
  (mode ask; offline → canned on-device guidance, never key logic).
- `PublisherService.publishReview()` → `POST <portal>/admin/publish`;
  `reviewCount()` → `GET <portal>/admin/publish`.
- `AdminLicenseService` → `POST/GET <portal>/admin/licenses`.
- Portal URL: `PortalLinkService.portalUrl()` (dev: `adb reverse
  tcp:8080 tcp:8080` or the machine's LAN IP).
- The APK must never contain: `GEMINI_API_KEY`, `GITHUB_TOKEN`,
  `generativelanguage`, `api.github.com` (probe-verified per release).

## 7. CORS

- `server.dart` adds `Access-Control-Allow-Origin: *` (GET/POST/OPTIONS)
  and answers OPTIONS preflights with 204 — required for the static
  website's cross-origin proxy calls.
