# Elat — Decisions & open assumptions

This log records resolved decisions and the assumptions still carried as "taxmin" (assumption).
When the spec is ambiguous, the chosen default is written here instead of being guessed silently in
code. Numeric limits from SPEC §18 are defaults and live in configuration, not hardcoded.

Legend: **RESOLVED** = confirmed by product owner · **ASSUMPTION (taxmin)** = agent default, open to change.

---

## Resolved by product owner (2026-10-21)

### D1 — Repository layout · RESOLVED
Single **monorepo** named `elat` containing `elat-backend/`, `elat-app/`, and a single shared
`docs/` at the root. Design mockups are a single file `docs/design.pdf` (not a `docs/design/`
folder). CI is one GitHub Actions workflow at the repo root with independent, path-filtered jobs
for backend and app.

### D2 — Pilot city · RESOLVED
Pilot city is **Toshkent**. City remains fully config/DB-driven so more cities can be added without
code changes (multi-city expansion in Phase 5).

### D6 — Maps provider · RESOLVED
**Yandex MapKit** (better Uzbekistan coverage). Access is wrapped behind a `MapProvider` interface
in the app so the provider can be swapped without touching feature code.

### D10 — Data residency · RESOLVED
In **production**, personal data is stored on servers located in **Uzbekistan**. All infrastructure
endpoints (database, Redis, object storage, SMS, payments, CDN) are configured via environment
variables so hosting can be relocated easily. No hardcoded hosts or regions.

### D9 — Store payments for TOP · RESOLVED
TOP (and other paid promotions) is treated as a **digital good**. Payments sit behind a provider
abstraction, and purchase availability is controlled by a **per-platform feature flag**. In the
**first release, buying TOP is DISABLED on iOS**; enabled on Android (and/or web redirect). Revisit
after store-policy review (`docs/STORE_PAYMENT_NOTES.md` in Phase 3).

---

## Assumptions carried by the agent (taxmin — change anytime)

### D3 — State management · ASSUMPTION
**Riverpod** (SPEC allows Riverpod or Bloc; one choice, used consistently).

### D4 — Font · ASSUMPTION
**Manrope**, verified for full Uzbek Latin + Cyrillic glyph coverage on device. Fallback: Inter.

### D5 — Icon family · ASSUMPTION
**Lucide** style, 24 px, 1.75 stroke, single family. No emoji as icons.

### D7 — Local database (app cache/drafts) · ASSUMPTION
**Drift** (SQLite) over Isar — mature, SQL queries, good for offline drafts + cache.

### D8 — Search engine timing · ASSUMPTION
**PostgreSQL full-text** with Latin/Cyrillic transliteration through the MVP. Re-evaluate moving to
**Meilisearch** at Phase 4 or earlier if search quality complaints arise.

### D11 — Telegram login · ASSUMPTION
**Deferred** past MVP. First release ships phone/SMS login only (SPEC marks Telegram/Apple login P1).

### D12 — Git history · ASSUMPTION
`git init` at the monorepo root in Phase 0; conventional commits; phase tags (`v0.0-foundations`,
`v0.1-mvp`, …).

### D13 — Backend Python version · ASSUMPTION
SPEC fixes **Python 3.12**. All Docker images and CI pin 3.12. (The current local dev machine only
has Python 3.11 and no Docker/Flutter, so the authoritative environment is Docker + CI, not this
machine — see "Environment note" below.)

### D14 — Riverpod/codegen, API client · ASSUMPTION
App consumes a client **generated from the backend OpenAPI** (drf-spectacular schema). The generator
choice (openapi-generator vs swagger_dart_code_generator) is finalized in Phase 1 when the schema
first exists; default: `openapi-generator` (dart-dio). `build_runner` is added to the app CI step in
Phase 1 (omitted in Phase 0 because there are no code generators yet).

### D15 — Phase 0 icon/font placeholders · ASSUMPTION
This workstation has no Flutter SDK, so third-party package versions cannot be resolved here. To keep
Phase 0 buildable without guessing versions, the skeleton uses **Material icons** as temporary
placeholders and the **Manrope** font family name without bundled assets (falls back gracefully).
Phase 1 pins the real Lucide/Phosphor icon package and drops Manrope `.ttf` files into
`assets/fonts/`, declared in `pubspec.yaml`. App dependencies in Phase 0 are kept minimal
(`flutter_riverpod`, `go_router`, `intl`) to avoid unresolved-version CI failures.

---

## Environment note (this workstation)

Observed 2026-10-21 on the dev machine running the agent:
- Python **3.11.8** (SPEC wants 3.12 — Docker/CI provide 3.12).
- **Docker not installed**, **Flutter not installed**.
- Git 2.54, Node 26 available.

Consequence: the agent can author all skeleton code and configuration, but **cannot run
`docker compose up` or Flutter builds on this machine**. Those must be verified by the owner (or CI)
on a machine with Docker Desktop and the Flutter SDK. The agent will clearly mark any step it could
not execute locally.
