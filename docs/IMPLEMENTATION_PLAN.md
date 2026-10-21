# Elat — Implementation Plan

Status: Draft for approval · Owner: lead engineer (AI-assisted) · Source of truth: `docs/SPEC.md`

This plan is the "first action" required by the master prompt: no application code is written yet.
It defines the monorepo structure, the phase-by-phase plan mapped to SPEC section 16,
a data-model overview, the risk list, the third-party accounts and credentials needed from the
product owner, and the open questions / assumptions that must be resolved before Phase 1.

All numeric limits referenced here are SPEC section 18 defaults and MUST live in configuration
(Django settings + admin-editable `settings`/config models), never hardcoded in business logic.

---

## 0. Monorepo layout and shared docs

A single git repository `elat` at the workspace root holds the backend, the app and the shared
docs side by side:

```
elat/                           # one git repo (monorepo)
  docs/                         # shared spec + design, single source of truth
    SPEC.md                     # full spec (Uzbek)
    design.pdf                  # mockups (Navy + Coral)
    IMPLEMENTATION_PLAN.md      # this file
    DECISIONS.md                # decisions + open assumptions
    DEMO.md                     # per-phase demo script (created in Phase 1)
    CHANGELOG.md                # created in Phase 0
  elat-backend/                 # Django modular monolith
  elat-app/                     # Flutter app
  .github/workflows/            # CI with separate backend + app jobs
```

One `docs/` lives at the repo root and is referenced by both `elat-backend` and `elat-app` (no
duplication). CI is a single GitHub Actions workflow with independent jobs per sub-project, each
triggered by path filters so a backend change does not rebuild the app and vice versa.

### 0.1 Backend sub-project structure (`elat-backend/`)

```
elat-backend/
  config/                       # django project (not an app)
    settings/
      base.py  dev.py  prod.py  test.py
    urls.py  asgi.py  wsgi.py  celery.py
  apps/
    core/            # base model (timestamps, soft-delete), error format, i18n,
                     # throttling, audit log, config/limits model, utils
    users/           # SMS auth, JWT, sessions/devices, profile, roles, badges, account deletion
    catalog/         # cities, districts, categories tree, category attribute schemas
    listings/        # listings (all sections), images (3 sizes), statuses, expiry, limits, dedupe
    requests/        # Saxovat gift requests, swap offers
    auctions/        # auctions, bids, anti-sniping, closing
    chat/            # conversations, messages, Channels consumer, offers
    search/          # full-text (Latin/Cyrillic translit), filters, favorites, saved searches, map
    reviews/         # ratings, reviews, badges, impact stats, monthly top
    notifications/   # FCM/APNs, catalog (SPEC 19), prefs, quiet hours, digests
    payments/        # wallet, transactions ledger, providers (Click/Payme/Uzum), webhooks, promotions
    ads/             # local advertiser placements, ad config flags
    moderation/      # banned words, auto filters, queue, reports, blocks, appeals
    organizations/   # Ehtiyojmandlar: orgs, verification, need-lists
    masters/         # repair masters directory
    campaigns/       # seasonal campaigns, top lists, neighborhood notifications
  deploy/            # Dockerfile, docker-compose.yml, nginx, entrypoints
  manage.py  pyproject.toml  .env.example  .pre-commit-config.yaml  pytest.ini
```
(CI lives in the root `.github/workflows/`, not inside the sub-project.)

Per-app layout (enforced): `models.py, serializers.py, views.py, services.py (business logic),
selectors.py (queries), permissions.py, tasks.py, urls.py, admin.py, apps.py, migrations/, tests/`.
Business logic lives in `services.py`/`selectors.py`, never in views or serializers.

### 0.2 Flutter app structure (`elat-app/`)

```
elat-app/
  lib/
    main_dev.dart  main_staging.dart  main_prod.dart   # flavors
    bootstrap.dart
    core/
      theme/      # color tokens, typography (Manrope), spacing, radii, light+dark
      motion/     # durations + curves from SPEC 17.1
      router/     # go_router shell, 5-tab bottom nav with raised center "+"
      network/    # dio, interceptors, auth, error mapping
      errors/     # failure types, error -> message mapping
      l10n/       # arb files uz-Latn, uz-Cyrl, ru
      config/     # env/flavor config, remote config
    data/         # generated OpenAPI client, DTOs, repositories, local db (Drift/Isar)
    features/
      auth/ home/ listings/ search/ map/ chat/ requests/ auctions/
      profile/ payments/ organizations/ notifications/ ads/
        each: presentation/ domain/ data/
    shared/       # ListingCard, SectionChip, PrimaryButton, SecondaryButton, TextField,
                  # FilterSheet, ChatBubble, OfferCard, Badge, SkeletonBox, EmptyState, Snackbar
  test/           # unit + widget tests
  test/golden/    # golden tests for key screens
  integration_test/
  pubspec.yaml  analysis_options.yaml  l10n.yaml
```
(CI lives in the root `.github/workflows/`, not inside the sub-project.)

State: Riverpod (chosen, consistent). Navigation: go_router. HTTP: dio with OpenAPI-generated client.
Local cache/drafts: Drift (SQLite) — chosen over Isar for maturity and SQL querying (see §8, Q7).

---

## 1. Technology decisions (fixed by SPEC, confirmed here)

| Layer | Choice | Notes |
| --- | --- | --- |
| Backend | Python 3.12, Django 5, DRF | Modular monolith |
| Real-time | Django Channels + Redis | Chat, auctions, notifications |
| Tasks | Celery + Celery Beat + Redis | Expiry, image processing, auction close, digests |
| DB | PostgreSQL 16 + PostGIS | Geo queries, GiST index |
| Search | PostgreSQL full-text first → Meilisearch later | Latin/Cyrillic transliteration |
| Storage | S3-compatible (MinIO dev / local cloud prod) + CDN | Presigned uploads, 3 image sizes |
| Auth | JWT (access 15 min, refresh 30 days) | Per-device revocation |
| API docs | drf-spectacular | `/api/schema`, `/api/docs` |
| Push | FCM (Android), APNs (iOS) | |
| SMS | Eskiz.uz / Playmobile behind an interface + console provider for dev | |
| Payments | Click, Payme, Uzum Pay behind a provider interface | Webhooks + idempotency |
| Ads | AdMob + Yandex Ads (mediation) | |
| Mobile | Flutter 3, Riverpod, go_router, dio, Drift, flutter_secure_storage | |
| Maps | Yandex MapKit preferred (better UZ coverage); Google Maps fallback | Decision in §8, Q6 |
| CI/CD | GitHub Actions + Docker; Fastlane for store builds | |

---

## 2. Phase plan (mapped to SPEC §16)

Gate rule: proceed to the next phase only after the current phase passes SPEC §20.2 acceptance and
the human review checklist in the prompt package. Tag git after each phase (`v0.0-foundations`,
`v0.1-mvp`, ...).

### Phase 0 — Foundations (≈ 1–2 weeks of agent time)
SPEC: 11, 12, 15, 17.
- Backend: project skeleton + all 16 apps; split settings; env config; Dockerfile +
  docker-compose (django, postgres+postgis, redis, celery worker, celery beat, minio); health
  endpoint; tooling (ruff, mypy, pytest, pytest-django, factory_boy, coverage, pre-commit); CI.
- Core: `{code,message,details}` error format; Accept-Language i18n; throttling classes; audit log
  model; soft-delete + timestamp base model; admin-editable limits/config model; drf-spectacular.
- Seed command: cities, districts, categories tree + category attribute schemas (car: year,
  mileage, fuel; property: rooms, area).
- App: Flutter skeleton, flavors (dev/staging/prod), l10n scaffold, go_router 5-tab shell;
  `core/theme` + `core/motion` tokens; shared widgets + a gallery screen; CI.
- **Acceptance:** `docker compose up` works from scratch; CI green (both jobs); OpenAPI docs open;
  gallery screen matches design colors/sizes in light + dark.

### Phase 1 — MVP (longest phase, ≈ 3 months human-scale)
SPEC: 4.1, 4.2, 5.1–5.3, 8.1–8.3, 18.1–18.4, 18.9, 14 (basic). Contact via phone/Telegram only (no in-app chat yet).
- Backend: users (SMS login per 18.1, JWT, device sessions, profile 18.2, account deletion, block
  checks); catalog; listings (model per §12, statuses, CRUD/extend/status per 18.3, presigned
  upload, 3-size + EXIF-strip task, displaced public location, 30-day expiry + reminder, daily
  limits, duplicate check, Saxovat price=NULL); search (full-text translit, filters, sorting,
  cursor pagination 20, TOP ordering placeholder, favorites, saved searches storage); map endpoint
  with clustering; requests/Saxovat (send/choose/give per 18.4); moderation v1 (auto filters,
  queue, reports, blocks); Django admin (unfold) with moderation, categories, banned words, limits,
  dashboard counters.
- App: onboarding/language/city/phone/SMS; home; search + filter sheet + results (grid/list) + map;
  listing detail (Savdo + Saxovat with request sheet), favorites, share, report, phone/Telegram
  contact; create-listing 5-step flow with compression, reorder, dynamic attributes, location
  picker, preview, draft autosave + offline queue; profile (my listings tabs, favorites, saved
  searches, settings incl. delete account).
- **Acceptance:** SPEC §20.2 stage 1; register by SMS; post Saxovat + Savdo in < 60 s; find via
  search + map; send Saxovat request; admin moderates; all strings in 3 languages; `docs/DEMO.md`.

### Phase 2 — Chat and trust (≈ 2 months)
SPEC: 5.4, 5.5, 18.5, 18.7, 18.8, 18.10, 18.12, 19, 8.4, 17.3/17.5.
- Backend: chat (conversations per listing, authed Channels consumer, message types, delivery
  states, unread counters, spam + risky-phrase warnings 18.10, block handling, push fallback);
  offers (price offers/counter per 18.5, expiry task, system messages); swap (18.7) + wanted
  (18.8 with capped matching notifications); reviews/ratings/badges/impact/monthly top (18.12);
  notifications service (FCM/APNs, catalog §19 in 3 languages, prefs, quiet hours, daily caps,
  saved-search digest, price-drop + expiry reminders); security review of chat.
- App: chats list + conversation (bubbles, offer cards, quick replies, typing, image send,
  report/block, safety notice); notification center + deep-link push; ratings/reviews/badges/
  impact share card; swap + wanted flows; Saxovat request management for giver; motion 17.3/17.5.
- **Acceptance:** real-time chat between two accounts, offers accepted, correct deep-linked push;
  swap/wanted/ratings pass tests; chat load test 500 concurrent connections documented; §20.2 st.2.

### Phase 3 — Monetization (≈ 2 months, extra care on money code)
SPEC: 5.6, 9, 18.11, 7.10, 15.3.
- Backend: payments (immutable double-entry-style ledger, provider interface + Click/Payme/Uzum
  adapters, create-payment, webhooks with signature verification + idempotency, reconciliation
  task, refunds 18.11, receipts); promotions (TOP 1/3/7d, highlight, auto-boost via Beat,
  category+city ranking into search, expiry + reminders, admin-editable prices); listing packages
  (cars/real estate), daily free limits, business profiles + subscriptions; ads placements +
  remote-config frequency flags; admin finance dashboard + export + refund (finance role only).
- App: wallet + top-up (provider redirect/return) + history; promote-listing flow + success
  animation; AdMob + Yandex Ads mediation (banner on search bottom + profile, native every 8th
  card with "Reklama" label, consent/ATT, frequency caps; never in create/chat); store-compliance
  notes `docs/STORE_PAYMENT_NOTES.md`; do NOT ship iOS payments until owner decides (SPEC 9.4).
- **Acceptance:** sandbox payments all 3 providers happy path; duplicate webhooks don't
  double-credit; failed/delayed handled; refunds work; TOP appears + expires on time; ads only in
  allowed places; §20.2 st.3.

### Phase 4 — Baraholka and community (≈ 2 months)
SPEC: 4.3, 4.6, 5.5, 18.6, 18.13, 18.14, 8.5, 17.5.
- Backend: auctions (durations, start price, step bands, bid validation, 5-min anti-sniping,
  exact Celery close + crash-safe recovery, second-bidder fallback after 48h, race-safe bidding
  with DB locking + concurrency tests, WS live updates); organizations (application + doc upload,
  admin verification workflow, need-lists with priorities, help offers, stale reminders, abuse);
  masters directory; Baraholka condition labels + daily finds feed + editor picks; campaigns
  (seasonal banners, top lists, segmented push) + neighborhood notifications (consent + caps);
  moderation v2 (severity queue, appeals, moderator performance report, duplicate-image detection).
- App: auction screen (live timer, stepper bid, confirmation, history, extension animation, outbid
  handling); Baraholka feed + finds feed + masters directory; Ehtiyojmandlar screens; impact share
  card, seasonal banners, neighborhood notification settings.
- **Acceptance:** 100 concurrent bids → correct winner; auctions close exactly + extend correctly;
  org verification end-to-end; §20.2 st.4.

### Phase 5 — Hardening, release, expansion (ongoing)
SPEC: 15, 16 (phase 5), 10.4.
- Security (dependency audit, OWASP checklists, rate-limit + secrets review, pentest prep, admin
  2FA + IP restriction, backup/restore drill); performance (slow-query profiling, indexes,
  caching, CDN, k6/Locust load test to SPEC 11.5 targets); observability (Sentry, structured logs,
  Prometheus + Grafana, Telegram alerts); release engineering (Fastlane AAB + TestFlight, staged
  rollout, forced-update HTTP 426, maintenance screen, remote config); store readiness (privacy
  policy + terms, data-safety/privacy labels, account-deletion web page, UGC evidence, ASO
  screenshots/descriptions uz+ru, age rating); business features (subscriptions UI, delivery
  partner adapter, Telegram channel autoposting + bot, image-based category suggestion behind flag,
  basic price suggestion); multi-city config (per-city pricing + TOP slots).
- **Acceptance:** §20.2 "every stage"; `docs/RUNBOOK.md`; zero open critical/high findings; beta on
  TestFlight + Google Play internal testing.

---

## 3. Data-model overview (SPEC §12)

Common to all tables: `id`, `created_at`, `updated_at`, soft delete via `deleted_at`.

Core clusters:
- **Identity/users:** `users` (phone unique, name, avatar, city, language, role, is_verified,
  is_blocked, rating_avg, last_seen), `devices` (fcm_token, platform), `sessions` (refresh hash,
  device, expiry → per-device revoke), `badges` + `user_badges`.
- **Catalog:** `cities`, `districts` (geo), `categories` (self-tree, section_mask,
  attributes_schema JSON), `category_attributes` (key, type, options, required).
- **Listings:** `listings` (user, section in {gift/sale/flea/swap/need}, category, title,
  description, price nullable, currency, condition, status, location PostGIS point,
  location_hidden_radius, district, expires_at, is_top, top_until, views_count, attributes JSON),
  `listing_images` (url_small/medium/large, thumb, order, hash, moderation_status).
- **Interactions:** `gift_requests` (listing, requester, reason, status), `swap_offers`
  (listing, offered_listing, extra_money, status), `wanted_posts` (or section=need),
  `favorites` (unique user+listing), `saved_searches` (query, filters JSON, notify).
- **Auctions:** `auctions` (listing, start_price, min_step, ends_at, status, winner),
  `bids` (auction, user, amount) index `(auction_id, amount DESC)`.
- **Chat:** `conversations` (listing, buyer, seller, last_message_at),
  `messages` (conversation, sender, type in {text/image/offer/location/system}, body, read_at)
  index `(conversation_id, created_at)`, `offers` (or messages.type=offer).
- **Trust/moderation:** `reviews` (listing, author, target, rating, text), `reports`
  (reporter, target_type, target_id, reason, status, resolved_by), `blocks`, `banned_words`,
  `audit_logs` (actor, action, object, ip).
- **Social/org:** `organizations` (owner, name, type, document_url, is_verified), `org_needs`
  (org, title, description, priority, status), `masters` (user, categories, service_area,
  price_from, rating).
- **Money:** `wallets` (user, balance), `transactions` (wallet, provider, amount, status,
  external_id, purpose), `promotions` (listing, type in {top/highlight/boost}, starts/ends, price),
  `subscriptions` (user, plan, dates), `business_profiles`.
- **Growth:** `ad_placements`, `campaigns`, `notifications` (user, type, payload JSON, read_at).

Key indexes: GiST on `listings.location`; composite `(section, category_id, status, created_at)`;
full-text on title+description (Latin+Cyrillic translit); `messages (conversation_id, created_at)`;
`bids (auction_id, amount DESC)`; unique `favorites (user_id, listing_id)`.

Data rules (enforced in model/service): Saxovat `price` always NULL; statuses
`draft, pending, active, reserved, given_sold, expired, rejected, deleted`; exact coordinates never
leave the server (clients get a displaced approximate point).

---

## 4. Cross-cutting engineering standards

- **Security:** HTTPS only; no secrets in code/git (`.env` + `.env.example`); server-side
  validation on every input; per-endpoint + object-level permissions; throttling (anon 60/min,
  user 240/min, SMS 3/hour/phone); EXIF stripped on upload; payment idempotency + webhook signature
  verification; audit log for admin actions; soft delete where specified; OWASP API Top 10.
- **Privacy:** displaced coordinates only; phone hidden unless owner allows; full account deletion;
  configurable storage provider for data-residency (Uzbekistan where required).
- **Quality:** every feature ships with tests (backend unit + API integration ≥ 70% coverage;
  Flutter unit + widget + golden for key screens); ruff/ruff-format/mypy and dart analyze/format
  must pass; no undocumented TODOs; small readable functions; docstrings on public APIs.
- **Performance:** list endpoints p95 < 300 ms (select_related/prefetch_related, indexes, cursor
  pagination 20); 3 image sizes via CDN; app cold start < 2.5 s; lists 60 FPS.
- **API:** versioned `/api/v1/`; error `{code, message, details}` localized by Accept-Language;
  OpenAPI always current.
- **Localization:** no hardcoded user strings; uz-Latn uses exact SPEC §18/§19 texts; uz-Cyrl + ru
  equivalents provided.
- **Git:** conventional commits; one feature per branch/PR with description, UI screenshots, test
  summary; phase tags.

---

## 5. Risk list

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| Chicken-and-egg empty marketplace | High | Start in one pilot city; manually seed first ~500 listings; lead with Saxovat for organic traffic |
| Store digital-goods payment rules (TOP as digital good) | Medium | Verify Apple/Google rules early; `docs/STORE_PAYMENT_NOTES.md`; route payment to web if needed; gate iOS payments on owner decision |
| Fraud / fake listings | High | Phone verification, new-account daily limits, auto filters, reports, duplicate-image hash, chat warnings |
| Low ad revenue | High | Rely on paid promotions + local ads, not ad network alone |
| Scope too large | High | Strict phase gates; one feature per PR; MVP excludes chat |
| Personal-data law (data residency) | Medium | Configurable in-country storage; legal review before launch |
| Moderator capacity | Medium | Auto filters, severity-based queue, grow team ahead of launch |
| Auction race conditions / sniping | Medium | DB locking/atomic bids + concurrency tests; server-side exact close with crash recovery |
| Payment correctness | High | Immutable ledger, idempotency keys, webhook signatures, never trust client amounts, extra tests, human review |
| Latin/Cyrillic search quality | Medium | Transliteration layer; move to Meilisearch if PG full-text insufficient |
| Key engineer leaves | Medium | Docs, code review, CI/CD |
| iOS build cannot be produced in this environment | Medium | Be explicit when a step (e.g. iOS build) can't be run locally; document it |

---

## 6. Third-party accounts & credentials needed from the owner

Provide via `.env` files only — never pasted into chat. Needed roughly in the phase shown.

| Phase | Service | What is needed |
| --- | --- | --- |
| 0 | GitHub | One `elat` monorepo + Actions enabled |
| 0 | Hosting (in-country) | Provider choice; dev/staging/prod environments |
| 1 | SMS (Eskiz.uz / Playmobile) | API credentials + sender name/alpha; (dev uses console provider) |
| 1 | Maps (Yandex MapKit or Google Maps) | API key(s) for iOS + Android |
| 1 | S3-compatible storage | prod bucket + keys (dev uses MinIO) |
| 2 | Firebase | FCM project; APNs auth key (Apple Developer); iOS bundle id |
| 2 | Apple Developer ($99/yr) + Google Play ($25 once) | For APNs, TestFlight, store listings |
| 3 | Click / Payme / Uzum Pay | Merchant/sandbox credentials + webhook secrets per provider |
| 3 | AdMob + Yandex Ads | App/unit ids, mediation config |
| 5 | Sentry, analytics (Firebase/AppMetrica) | DSN / keys |
| 5 | Legal | Privacy policy, terms, data-residency confirmation (lawyer) |

---

## 7. Deliverables per phase

- Running code in both sub-projects with passing CI.
- Updated `docs/`: `DECISIONS.md`, `CHANGELOG.md`, API docs; `DEMO.md` (P1), `STORE_PAYMENT_NOTES.md`
  (P3), `RUNBOOK.md` (P5).
- PR(s) with description, UI screenshots, and real test output.
- End-of-task report: what was done, what was not, known risks, next recommended task.

---

## 8. Open questions and proposed defaults (to confirm → `docs/DECISIONS.md`)

1. **Repo layout:** RESOLVED — single monorepo `elat` (`elat-backend/`, `elat-app/`, `docs/`);
   one canonical root `docs/` (with `design.pdf`, not a `docs/design/` folder).
2. **Pilot city:** which city first (Toshkent / Namangan / other)?
   *Default:* Toshkent, but keep city fully config-driven.
3. **State management:** Riverpod vs Bloc — SPEC allows either.
   *Default:* Riverpod (one choice, consistent).
4. **Font:** Manrope vs Inter.
   *Default:* Manrope (verify full uz Latin + Cyrillic glyph coverage on device).
5. **Icon family:** Lucide vs Phosphor.
   *Default:* Lucide (24 px, 1.75 stroke).
6. **Maps:** Yandex MapKit vs Google Maps.
   *Default:* Yandex MapKit (better UZ coverage); abstract behind a map interface to allow swap.
7. **Local DB:** Drift vs Isar for cache/drafts.
   *Default:* Drift (SQLite, mature, SQL queries).
8. **Search engine timing:** when to move from PG full-text to Meilisearch?
   *Default:* PG full-text through MVP; re-evaluate at Phase 4 or on search-quality complaints.
9. **Store payment policy (SPEC 9.4):** is TOP treated as a digital good requiring Apple/Google
   billing? Blocks shipping iOS payments. *Default:* investigate in Phase 3, do not ship iOS
   payments until owner decides; Android + web flow first.
10. **Data residency:** must all personal data be stored on servers physically in Uzbekistan?
    *Default:* assume yes; keep storage/hosting provider configurable; confirm with lawyer.
11. **Telegram login (P1 optional):** in scope for MVP or deferred?
    *Default:* defer; MVP ships phone/SMS login only.
12. **git init:** the monorepo is currently uninitialized and (aside from `CLAUDE.md` files) empty.
    *Default:* `git init` at the root in Phase 0 with conventional-commit history.

---

## 9. Recommended next step

On approval of this plan: resolve the §8 questions (at least Q2, Q6, Q10 which affect architecture),
create `docs/DECISIONS.md`, then start **Phase 0 — Foundations** (backend skeleton + Docker + CI and
Flutter skeleton + design tokens + widget gallery), ending with a demo of `docker compose up`, green
CI green (both jobs), open OpenAPI docs, and the gallery screen in light + dark mode.
