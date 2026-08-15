# AftLog — Coding & Operations Standards

> **Read this + `DECISIONS.md` before EVERY app session.** The rules below exist because the AftLog owner (Louis) paid for them in another project (CatchTales). Don't re-learn them.

---

## 0. How pi Must Operate

| Rule | Details |
|------|---------|
| **Read the standards on repeat** | Before ANY action (build, install, edit, feature), re-read the relevant section. Start of every session: `DECISIONS.md` + `AFTLOG-SPEC.md` + this file. |
| **Work step by step** | Propose → confirm → act → verify. One screen / one slice at a time. No charging ahead. |
| **Locked decisions** | Anything in `DECISIONS.md` is LOCKED. Change only by deliberate amendment with Louis's approval. Never silently. |
| **Verify on the phone** | After building, install on the real device and confirm before calling it done. |
| **Ask when unsure** | If a change might violate a rule, stop and ask. |

## 1. Brand rules (non-negotiable)

- **Palette (from the website):** background `#0B0B0D` · cards `#141417` · lines `#232329` · accent red `#E02020` · bright red `#FF4B4B` · text white `#FFFFFF` · muted `#9A9AA3`
- **NO EMOJIS. NO GRADIENTS.** App UI, screenshots, help text, translations, site — nowhere.
- **Logo + illustrations** come from Louis (`~/aftlog/images/`); never substitute emoji or scraped images.
- Tagline: "Keeping your boat shipshape!"

### Canonical palette (locked 2026-08-15 — grounded in aftlog-app code, Session 37 corrections)

Dark-mode only — AftLog does **not** implement a light theme. Status colors are the real app values (`#2ECC71`/`#F5B041`), **not** Material defaults (`#4CAF50`/`#FFC107`). No accent blue (`#2196F3` is NOT in the app — brand is red-only). No `#B00020`, `#121212`, `#1E1E1E`, `#303030`.

```dart
import 'package:flutter/material.dart';

/// AftLog — Canonical Color Palette
/// Grounded in the actual aftlog-app codebase (Session 37 corrections).
/// Dark-mode only — AftLog does not implement a light theme.

class AftLogColors {
  // ------------------------------------------------------------
  // BRAND
  // ------------------------------------------------------------
  static const Color brandRed = Color(0xFFE02020);       // primary accent / danger
  static const Color brandRedBright = Color(0xFFFF4B4B); // highlight / active

  // ------------------------------------------------------------
  // SURFACES (dark theme only)
  // ------------------------------------------------------------
  static const Color bg = Color(0xFF0B0B0D);             // main background
  static const Color card = Color(0xFF141417);           // cards, panels
  static const Color bgAlt = Color(0xFF0D0D10);          // dashboard alt background
  static const Color surfaceHigh = Color(0xFF1D1D22);    // elevated surfaces
  static const Color line = Color(0xFF232329);           // dividers, strokes
  static const Color muted = Color(0xFF9A9AA3);          // muted text

  // ------------------------------------------------------------
  // STATUS COLORS (actual app usage)
  // ------------------------------------------------------------
  static const Color healthy = Color(0xFF2ECC71);        // green (health score, checklists)
  static const Color warning = Color(0xFFF5B041);        // amber (due soon)
  static const Color danger = Color(0xFFE02020);         // due / overdue
  static const Color error = Color(0xFFFF6B6B);          // error states

  // ------------------------------------------------------------
  // TEXT
  // ------------------------------------------------------------
  static const Color textPrimary = Colors.white;
  static const Color textSecondary = muted;

  // ------------------------------------------------------------
  // OPTIONAL: Portal Light Theme (for future cross-platform alignment)
  // ------------------------------------------------------------
  static const Color portalLightBg = Color(0xFFEDEDF2);
  static const Color portalLightCard = Colors.white;
  static const Color portalLightLine = Color(0xFFD8D8E0);
  static const Color portalLightMuted = Color(0xFF5C5C6A);
}
```

### Canonical theme (locked 2026-08-15 — replaces `AftLogApp._buildTheme()`)

Material 3, dark-only, no gradients, no emojis. Validated against the app's Flutter 3.44.4 — the app already uses `CardThemeData` + `WidgetStateProperty`, so use those (NOT the deprecated `CardTheme`/`MaterialStateProperty`). Ready to drop in as `lib/theme/aftlog_theme.dart` (needs `aftlog_colors.dart` from the palette block above).

```dart
import 'package:flutter/material.dart';
import 'aftlog_colors.dart';

/// AftLog — Unified Theme (Dark-only)
/// Grounded in the actual app palette and Material 3.
/// Replaces AftLogApp._buildTheme() with a clean, centralized theme.

class AftLogTheme {
  static ThemeData build() {
    const scheme = ColorScheme(
      brightness: Brightness.dark,

      // Brand
      primary: AftLogColors.brandRed,
      onPrimary: Colors.white,
      secondary: AftLogColors.brandRedBright,
      onSecondary: Colors.white,

      // Error
      error: AftLogColors.error,
      onError: Colors.black,

      // Surfaces
      surface: AftLogColors.card,
      onSurface: Colors.white,
      surfaceContainerHighest: AftLogColors.surfaceHigh,

      // Tertiary / outline
      tertiary: AftLogColors.muted,
      onTertiary: Colors.white,
      outline: AftLogColors.line,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      // background/onBackground are deprecated in Flutter 3.18+ — surfaces cover this.
      scaffoldBackgroundColor: AftLogColors.bg,
      canvasColor: AftLogColors.bg,

      // ------------------------------------------------------------
      // TEXT
      // ------------------------------------------------------------
      textTheme: const TextTheme(
        bodyLarge: TextStyle(fontSize: 15, height: 1.45),
        bodyMedium: TextStyle(fontSize: 14, height: 1.45),
        bodySmall: TextStyle(fontSize: 12.5, height: 1.45, color: AftLogColors.muted),

        titleLarge: TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
        titleMedium: TextStyle(fontSize: 17, fontWeight: FontWeight.w700),
        titleSmall: TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
      ),

      // ------------------------------------------------------------
      // CARDS
      // ------------------------------------------------------------
      cardTheme: const CardThemeData(
        color: AftLogColors.card,
        elevation: 0,
        margin: EdgeInsets.symmetric(vertical: 8),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(12)),
        ),
      ),

      // ------------------------------------------------------------
      // DIVIDERS
      // ------------------------------------------------------------
      dividerColor: AftLogColors.line,
      dividerTheme: const DividerThemeData(
        thickness: 1,
        color: AftLogColors.line,
      ),

      // ------------------------------------------------------------
      // BUTTONS
      // ------------------------------------------------------------
      filledButtonTheme: FilledButtonThemeData(
        style: ButtonStyle(
          backgroundColor: WidgetStateProperty.all(AftLogColors.brandRed),
          foregroundColor: WidgetStateProperty.all(Colors.white),
          padding: WidgetStateProperty.all(
            const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          ),
        ),
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ButtonStyle(
          backgroundColor: WidgetStateProperty.all(AftLogColors.brandRedBright),
          foregroundColor: WidgetStateProperty.all(Colors.white),
          padding: WidgetStateProperty.all(
            const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          ),
        ),
      ),

      // ------------------------------------------------------------
      // INPUTS
      // ------------------------------------------------------------
      inputDecorationTheme: const InputDecorationTheme(
        filled: true,
        fillColor: AftLogColors.card,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.all(Radius.circular(10)),
          borderSide: BorderSide(color: AftLogColors.line),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.all(Radius.circular(10)),
          borderSide: BorderSide(color: AftLogColors.line),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.all(Radius.circular(10)),
          borderSide: BorderSide(color: AftLogColors.brandRedBright, width: 1.4),
        ),
        labelStyle: TextStyle(color: AftLogColors.muted),
        hintStyle: TextStyle(color: AftLogColors.muted),
      ),

      // ------------------------------------------------------------
      // ICONS
      // ------------------------------------------------------------
      iconTheme: const IconThemeData(
        color: Colors.white,
        size: 20,
      ),

      // ------------------------------------------------------------
      // LIST TILES
      // ------------------------------------------------------------
      listTileTheme: const ListTileThemeData(
        iconColor: Colors.white,
        textColor: Colors.white,
        tileColor: AftLogColors.card,
      ),

      // ------------------------------------------------------------
      // APP BAR
      // ------------------------------------------------------------
      appBarTheme: const AppBarTheme(
        backgroundColor: AftLogColors.bg,
        elevation: 0,
        titleTextStyle: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w700,
          color: Colors.white,
        ),
      ),
    );
  }
}
```

## 2. Version & release discipline

| Rule | Details |
|------|---------|
| **Every change bumps the version** | No exceptions. One `pubspec.yaml`, one version (`X.Y.Z+N`). **`./build.sh` auto-bumps patch + build number on every build** — never hand-bump; never raw `flutter build` for anything real. |
| **Features = minor bump** | e.g. 1.0.x → 1.1.0 (manual). Patch bumps are automatic via build.sh. MVP public launch = 1.1.0 (DECISIONS.md #11). |
| **Rule 3 — always together** | Every app change also updates: What's New, Help text, Translations (en/fr/es/de/uk), Version, Website. |
| **Distribution** | Direct APK + Play internal/closed testing track ONLY. Public Play launch is gated on Louis's sign-off — never a date. |
| **gh release from the RIGHT repo** | `cd ~/aftlog-site` for site releases; `cd ~/aftlog-app` for app. (CatchTales scar: released into the wrong repo once.) |

## 3. Build workflow

- **Always `./build.sh`** — auto-bumps version, injects Gemini key (env → pass → .env), obfuscates, signs with `aftlog-release.keystore` (key.properties, gitignored), renames APK to `AftLog-vX.Y.Z.apk`. Never raw `flutter build` for anything real.
- Debug signing is FORBIDDEN for release builds (aftlog-release.keystore only — Play updates require it).
- Obfuscate + split-debug-info on release builds (Crashlytics symbol upload).
- Verify version in the built APK (`aapt dump badging`).
- Install via adb chunked push (Samsung stall fix) when sideloading.

## 4. Database rules

- **Offline-first SQLite always works with zero signal** — the core. Cloud sync is optional, never required.
- **Tables complete in EVERY creation path** — onCreate AND onUpgrade migrations must both create full tables (CatchTales Session 32 scar: `<4`-only migration silently missed fresh installs).
- Every migration: version bump + new columns added via ALTER with try/catch, and the base CREATE updated too.

## 5. Security & secrets

- API keys in `pass`; never in code, env commits, or .bashrc exports that get committed.
- Keystore: `~/aftlog/keystore/` — gitignored, password in pass, backup off-machine. NEVER commit `*.keystore`, `key.properties`.
- No forced login. Optional account for sync. Security-hardened patterns from day one (server-owned fields, callable functions, rate limits).

## 6. Monetization (locked)

- Free tier: 1 boat, capped entries, no reminders, no AI (AI teaser with daily limit).
- **$29 one-time Pro**, 30-day money-back. No ads, no subscription.
- Unlock layer ABSTRACTED so Play Billing can be added later without a rewrite.

## 7. Crash reporting

- Crashlytics wired from the FIRST build. Never retrofitted after launch.

## 8. Repos

- `aftlog/aftlog-app` — Flutter app (clone at `~/aftlog-app`)
- `aftlog/aftlog-site` — site (clone at `~/aftlog-site`)
- Docs: `~/aftlog/` (spec, decisions, images, keystore)
- Never mix products or release artifacts across repos.

## 9. Lessons learned — Session 1 (2026-08-10)

| Rule | Why (what happened) |
|------|---------------------|
| **Verify in the BUILT artifact, never source-only** | Location permissions were added to the manifest via an edit that targeted a nonexistent INTERNET line — source "looked" right but the APK had no permissions. GPS permission took 3 rounds to find. After ANY manifest/gradle/pubspec change: `aapt dump permissions <apk>` (or inspect the build output) before testing the feature. |
| **Check what you're staging** (`git diff --cached --stat`) | `git add -A` swept an 80MB debug `kernel_blob.bin` into the repo (the CatchTales bloat scar, again). Keep `assets/flutter_assets/` + `build/` gitignored; glance at staged sizes before committing. |
| **Ask Louis what he wants to SEE on a screen before building it** | The Log tab was built 3 times (input-only, then stats, then fuel-brain) before asking. Rule: propose the screen's purpose/contents, get his answer, THEN build. (This is Rule-0 "propose → confirm" applied to UX, and it was violated today.) |
| **Scroll-view hygiene** | Recurring RenderFlex overflows (dashboard card, checklist cards, dialog, bottom clipping). Default: variable-length text in Rows goes in Flexible/ellipsis; scrollable screens end with >=80px bottom padding; dialog forms use fixed-width Dialogs, not AlertDialogs with long fields. |
| **Shared-data screens listen to BoatEvents** | Dashboard showed a stale boat list after deletes in another tab (IndexedStack keeps tabs alive). Any screen displaying boats (or counts) must listen to `BoatEvents.instance`, not load once. |
| **Fight plugin versions, or drop the plugin** | share_plus 10.1.4 / 11.x / 12.x all failed Android builds (broken Kotlin refs); fixed by REMOVING share_plus and writing exports to Downloads instead. When a plugin's recent versions won't compile, removing it can be the right answer. |
| **Scripted edits need a verification step** | A python replace of pubspec assets landed in the wrong section (corrupted YAML); a manifest replace silently no-op'd. After any scripted file edit: re-read the result, `flutter analyze`, and confirm the build. |
| **Version bump on every change** | App is still 1.0.0+1 after many builds. From now: every change bumps pubspec (dev = patch 1.0.x; feature = minor). Do it at the END of each working session at minimum, before any build that leaves the machine. |
