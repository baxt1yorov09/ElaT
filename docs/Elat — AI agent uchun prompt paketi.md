# Elat — AI agent uchun prompt paketi

Oct 20, 2026 · @Sardor

Bu paket Devin yoki Claude Code kabi kod yozuvchi agentga topshiriladi: avval asosiy prompt va qoidalar fayli, keyin bosqichlar bo'yicha vazifalar. Promptlar ingliz tilida yozilgan, chunki agentlar texnik topshiriqni shunda aniqroq bajaradi; ilova matnlari esa o'zbek va rus tilida bo'ladi.

## Qanday ishlatiladi

1. **Hujjatlarni tayyorlang.** "Elat — Loyiha ma'lumotnomasi" hujjatini Markdown (yoki Word) sifatida yuklab oling va repoga `docs/SPEC.md` nomi bilan qo'ying. Dizayn maketlarini PDF yoki rasm sifatida `docs/design/` papkasiga qo'ying.
2. **Ikkita repo oching:** `elat-backend` va `elat-app`. Ikkalasiga ham `docs/` papkasini nusxalang.
3. **Qoidalar faylini qo'ying.** 3-bo'limdagi matnni backend repoga `CLAUDE.md` (Devin uchun "knowledge" yoki `AGENTS.md`) sifatida saqlang; ilova repoga Flutter variantini.
4. **Asosiy promptni bering** (2-bo'lim), agent hujjatlarni o'qib chiqib, reja bersin.
5. **Bosqich promptlarini ketma-ket bering** (4-bo'lim). Keyingisiga faqat oldingisi tekshiruvdan o'tgach (5-bo'lim) o'ting.

**Muhim:** agent ishining har bir qismini siz yoki tajribali dasturchi ko'rib chiqishi kerak, ayniqsa to'lov, xavfsizlik va shaxsiy ma'lumotlar bilan bog'liq qismlarni. Kalitlar va parollarni agentga matn sifatida bermang; `.env` faylida o'zingiz saqlang.

## Asosiy prompt (Master prompt)

Bu matnni agentga birinchi xabar sifatida to'liq nusxalab bering.

```text
YOU ARE the lead engineer of a small AI-assisted team building "Elat", a production-grade mobile marketplace for Uzbekistan (iOS + Android). Your job is to build it professionally, step by step, to the specification in this repository. Quality, security and clarity matter more than speed.

=== 1. PRODUCT IN ONE PARAGRAPH ===
Elat is a multi-section classifieds app built around the idea of "giving things a second life". Sections: (a) Saxovat = free items, pickup only, no price field; (b) Savdo = normal priced marketplace incl. cars and real estate; (c) Baraholka = flea market for old, rare, antique items with optional auctions; plus (d) Almashtirish (swap/barter), (e) Menga kerak (wanted posts), (f) Ehtiyojmandlar (verified charities/organizations publish need-lists). Core systems: SMS phone login, listings with photos and geolocation, search and filters, map, in-app chat with price offers, notifications, ratings and badges, moderation and reporting, paid promotions (TOP/boost), wallet and payments (Click, Payme, Uzum), ads (AdMob + Yandex Ads), admin panel. Languages: Uzbek Latin, Uzbek Cyrillic, Russian. Market: Uzbekistan, one pilot city first.

=== 2. SOURCE OF TRUTH ===
- docs/SPEC.md is the full product, design, technical and business specification (written in Uzbek). Read ALL of it before doing anything. Key sections: 4 sections of the app, 5 functional requirements, 6 roles and flows, 7 design system, 8 screens, 10 security and moderation, 11 architecture, 12 database schema, 13 API, 14 admin, 15 legal and store rules, 16 roadmap, 17 motion spec, 18 exact functional rules (limits, validations, error texts), 19 notification catalog, 20 acceptance criteria.
- docs/design/ contains screen mockups (Navy + Coral brand). Follow them for layout, spacing and components.
- If the spec is ambiguous or contradicts itself, DO NOT guess silently: write the question and your proposed default in docs/DECISIONS.md and ask me. Numeric limits in section 18 are defaults and must live in configuration (settings or admin-editable), never hardcoded in business logic.
- Do not invent features that are not in the spec. Propose them in docs/DECISIONS.md instead.

=== 3. TECHNOLOGY (fixed) ===
Backend: Python 3.12, Django 5, Django REST Framework, Django Channels (WebSocket chat and auctions), Celery + Celery Beat with Redis, PostgreSQL 16 + PostGIS, Redis, drf-spectacular (OpenAPI), JWT auth, S3-compatible storage with presigned uploads, Docker + Docker Compose, GitHub Actions CI. Apps (modular monolith): users, catalog, listings, requests, auctions, chat, search, reviews, notifications, payments, ads, moderation, organizations, masters, campaigns, core.
Mobile: Flutter 3 (Dart), feature-first clean architecture, Riverpod (or Bloc, pick one and stay consistent), go_router, dio with generated API client from OpenAPI, Drift/Isar for cache and drafts, flutter_secure_storage, firebase_messaging, Google Maps or Yandex MapKit, flutter l10n (uz-Latn, uz-Cyrl, ru), Lottie/Rive for key animations.
Do not swap technologies without asking.

=== 4. DESIGN RULES ===
- Brand: Elat Navy #1F2A44 (headings, navigation, logo), Elat Coral #FF6B4A (primary actions). IMPORTANT: text and icons on Coral are Navy #1F2A44, never white (accessibility contrast). Section colors: Saxovat green, Savdo blue, Baraholka amber, Almashtirish purple; use darker tints for small text (see SPEC 7.3 and 7.11).
- Font Manrope or Inter with full Uzbek Latin/Cyrillic coverage. 4 px spacing grid, radius: card 16, button 14, input 12, chip 999. Buttons 52 px high, minimum touch target 48 px. Bottom nav 64 px with raised 56 px center "+" button.
- All colors, text styles, spacing, radii and motion durations/curves live in ONE design-token layer (core/theme and core/motion). No magic numbers in widgets.
- Light and dark themes, large-font accessibility, reduce-motion support, screen-reader labels on icon-only buttons.
- Motion follows SPEC section 17 exactly (durations 100-350 ms, ease-out, hero transitions, skeleton shimmer, confetti only for Saxovat Done, auction timer behavior).

=== 5. NON-NEGOTIABLE ENGINEERING RULES ===
Security: HTTPS only; no secrets in code or git (use environment variables, provide .env.example); validate every input on the server; per-endpoint permissions and object-level authorization; rate limits (SMS: 3/hour/phone, API throttles); strip EXIF from uploaded images; idempotency keys and webhook signature verification for payments; audit log for admin actions; soft delete where specified; follow OWASP API Top 10.
Privacy: exact coordinates never leave the server, clients receive a displaced approximate point; phone numbers hidden unless the owner allows; account deletion fully implemented (store requirement); store personal data on infrastructure located in Uzbekistan where required (keep storage provider configurable).
Quality: every feature ships with automated tests (unit + API integration for backend, unit + widget tests for Flutter, golden tests for key screens where practical); backend coverage target 70 percent or higher; linters and formatters must pass (ruff, black or ruff-format, mypy for backend; dart analyze and dart format for Flutter); no TODOs left without an issue note; no dead code; small readable functions; docstrings on public APIs.
Performance: API p95 under 300 ms for list endpoints (use select_related/prefetch_related, indexes from SPEC section 12, cursor pagination 20 items); images in 3 sizes via CDN; cold start of app under 2.5 s; lists at 60 FPS.
Database: migrations for every schema change, never edit applied migrations; indexes as specified (GiST on location, composite listing indexes, full-text).
API: versioned under /api/v1/, consistent error format {code, message, details}, localized messages by Accept-Language, OpenAPI always up to date.
Localization: no hard-coded user-facing strings; every string exists in uz-Latn, uz-Cyrl and ru. Use the exact error and notification texts from SPEC sections 18 and 19 for Uzbek Latin; provide Cyrillic and Russian equivalents.

=== 6. HOW YOU WORK ===
For every task:
1. Restate the task and list the SPEC sections it implements.
2. Propose a short plan (files, models, endpoints, screens, tests). For anything large, wait for my OK.
3. Implement in small, reviewable commits (conventional commits: feat, fix, test, docs, refactor, chore). One feature per branch and pull request with description, screenshots for UI, and a test summary.
4. Run the tests, linters and the app/server yourself. Show real output. Never claim something works without running it. If you cannot run something (for example iOS build), say so clearly.
5. Update docs: README, docs/DECISIONS.md, API docs, CHANGELOG.
6. End each task with: what was done, what was NOT done, known risks, and the next recommended task.
If you are blocked, stop and ask; do not work around a blocker with hacks or fake data in production code paths. Use seed/fixture data only in dev and tests.

=== 7. DEFINITION OF DONE (per feature) ===
Spec rules implemented exactly (including limits, validations and error texts); tests pass; linters pass; migrations included; permissions and rate limits in place; localized in 3 languages; UI matches docs/design and design tokens; accessibility basics checked; docs updated; PR ready for review.

=== 8. YOUR FIRST ACTION ===
Do NOT write application code yet. First: (1) read docs/SPEC.md and docs/design completely; (2) produce docs/IMPLEMENTATION_PLAN.md with: repository structure for both repos, phase plan mapped to SPEC section 16 (phases 0 to 5), per-phase task breakdown with estimates, data model overview, risk list, third-party accounts and credentials I must provide, and a list of questions and assumptions; (3) reply with a short summary and wait for my approval before starting Phase 1.
```

## Qoidalar fayli (CLAUDE.md / AGENTS.md)

Bu fayl agent har safar ishga tushganda loyihani eslab turishi uchun reponing ildizida turadi. Qisqa va aniq bo'lishi kerak; uzun tavsif `docs/SPEC.md` da.

### Backend repo (elat-backend)

```text
# Elat Backend - agent rules

## Project
Django 5 + DRF + Channels + Celery, PostgreSQL/PostGIS, Redis. Modular monolith. Full spec: docs/SPEC.md (Uzbek). Product: Elat marketplace (Saxovat free items, Savdo, Baraholka, swap, wanted, charities).

## Commands
- Run dev: docker compose up
- Tests: pytest -q --cov=apps
- Lint/format: ruff check . && ruff format .
- Types: mypy apps
- Migrations: python manage.py makemigrations && python manage.py migrate

## Structure
apps/{users,catalog,listings,requests,auctions,chat,search,reviews,notifications,payments,ads,moderation,organizations,masters,campaigns,core}
Each app: models.py, serializers.py, views.py, services.py (business logic), selectors.py (queries), permissions.py, tasks.py, tests/.
Business logic goes in services, NOT in views or serializers.

## Rules
- Follow docs/SPEC.md section 18 exactly: limits, validations, error texts. Limits live in settings/DB config, never hardcoded.
- API under /api/v1/, error format {code, message, details}, messages localized (uz-Latn, uz-Cyrl, ru) by Accept-Language.
- Every endpoint: authentication, object-level permission, throttling, tests.
- Never commit secrets. Use env vars; keep .env.example updated.
- Exact coordinates never returned to clients; return displaced approximate point.
- Payments: idempotency key, verify webhook signatures, store every transaction, never trust client amounts.
- Every schema change = new migration. Never edit applied migrations.
- Listings: Saxovat has price NULL always. Statuses: draft, pending, active, reserved, given_sold, expired, rejected, deleted.
- Write tests with the feature. No feature without tests. No TODO without a note in docs/DECISIONS.md.
- Commits: conventional commits. One feature per branch/PR.

## Do not
- Do not change the tech stack without asking.
- Do not add features not in the spec; propose in docs/DECISIONS.md.
- Do not use real user data in tests; use factories.
- Do not claim something works without running it.
```

### Flutter ilova repo (elat-app)

```text
# Elat App - agent rules

## Project
Flutter 3 app (iOS + Android) for Elat marketplace. Spec: docs/SPEC.md. Mockups: docs/design/. API: generated client from backend OpenAPI.

## Commands
- Run: flutter run
- Tests: flutter test
- Analyze/format: dart analyze && dart format .
- Codegen: dart run build_runner build --delete-conflicting-outputs
- Localization: flutter gen-l10n

## Structure (feature-first)
lib/core (theme, motion, router, network, errors, l10n), lib/data (api clients, DTOs, repositories, local db), lib/features/{auth,home,listings,search,map,chat,requests,auctions,profile,payments,organizations,notifications,ads}/{presentation,domain,data}, lib/shared (widgets).
State: Riverpod. Navigation: go_router. HTTP: dio.

## Design rules
- Brand: Navy #1F2A44, Coral #FF6B4A. Text/icons on Coral are NAVY, never white.
- All colors, text styles, spacing, radii in core/theme; all durations/curves in core/motion. No magic numbers.
- Sizes: card radius 16, button radius 14 and height 52, input radius 12, minimum touch target 48, 16 px screen padding, 4 px grid.
- Reusable widgets in lib/shared: ListingCard (grid and list), SectionChip, PrimaryButton, SecondaryButton, TextField, FilterSheet, ChatBubble, OfferCard, Badge, SkeletonBox, EmptyState, Snackbar.
- Motion exactly per SPEC section 17. Respect disableAnimations.
- Light and dark themes. Support large system fonts.

## Rules
- No hard-coded user strings; use l10n (uz-Latn, uz-Cyrl, ru).
- Follow SPEC section 18 validations and error texts on the client too (but server is the authority).
- Handle loading, empty, error, offline states on every screen (skeleton, EmptyState, retry).
- Compress images before upload (max 1600 px long side, about 1 MB). Use presigned upload.
- Secure tokens in flutter_secure_storage. Never log tokens or phone numbers.
- Every screen: widget test; key screens: golden tests.
- Every icon-only button has a semantic label.

## Do not
- Do not add packages without a reason in the PR description.
- Do not use emoji as icons; use one icon family (Lucide/Phosphor style, 24 px, 1.75 stroke).
- Do not claim a UI is done without running it on an emulator and attaching a screenshot.
```

## Bosqichlar bo'yicha vazifa promptlari

Har bir promptni alohida xabar sifatida bering. Agent oldingi bosqich tekshiruvdan o'tgach keyingisiga o'tadi. Har prompt agentdan avval reja so'raydi, keyin bajaradi.

### Bosqich 0: poydevor (repo, muhit, CI, dizayn tokenlari)

```text
PHASE 0 - FOUNDATIONS. Read docs/SPEC.md sections 11, 12, 15, 17 and docs/IMPLEMENTATION_PLAN.md. Then, in small PRs:

BACKEND (elat-backend):
1. Project skeleton with the apps listed in CLAUDE.md, split settings (base/dev/prod), env-based config, Dockerfile, docker-compose (django, postgres+postgis, redis, celery worker, celery beat, minio), health endpoint.
2. Tooling: ruff, mypy, pytest, pytest-django, factory_boy, coverage, pre-commit, GitHub Actions CI (lint, types, tests, build image).
3. Core: error format {code,message,details}, Accept-Language i18n (uz-Latn, uz-Cyrl, ru), throttling classes, audit log model, soft-delete mixin, base model with timestamps, drf-spectacular schema at /api/schema and /api/docs.
4. Seed command with cities, districts, categories tree (Mebel, Texnika, Kiyim, Kitoblar, Bolalar, Transport, Ko'chmas mulk, Antikvar, etc.) and category attribute schemas (car: year, mileage, fuel; property: rooms, area).

APP (elat-app):
1. Flutter project with feature-first structure from CLAUDE.md, flavors (dev, staging, prod), l10n for uz-Latn, uz-Cyrl, ru, go_router shell with the 5-tab bottom navigation (center raised "+").
2. core/theme: color tokens (Navy, Coral, section colors, neutrals, light and dark), typography (Manrope), spacing, radii; core/motion: durations and curves from SPEC 17.1.
3. Shared widgets with widget tests and a "gallery" screen: PrimaryButton (Coral, Navy text), SecondaryButton, TextField, SectionChip, Badge, ListingCard (grid, list), SkeletonBox, EmptyState, Snackbar.
4. CI: dart analyze, format check, tests.

ACCEPTANCE: docker compose up works from scratch; CI green in both repos; OpenAPI docs open; gallery screen matches docs/design colors and sizes in light and dark mode. Report what you ran.
```

### Bosqich 1: MVP (SMS kirish, e'lonlar, qidiruv, xarita, admin)

```text
PHASE 1 - MVP. Implements SPEC sections 4.1, 4.2, 5.1-5.3, 8.1-8.3, 18.1-18.4, 18.9 (without in-app chat; contact via phone/Telegram link only), 14 (basic admin). Work feature by feature; for each: plan, tests, PR.

BACKEND:
1. users: phone login with SMS code (Eskiz provider behind an interface + console provider for dev), rules exactly per 18.1, JWT access/refresh, device sessions, profile (18.2), account deletion, block checks.
2. catalog: cities, districts, categories with attributes.
3. listings: model per SPEC 12, statuses, create/update/delete/extend/status change per 18.3, presigned image upload, background task that makes 3 image sizes and strips EXIF, displaced public location, expiry after 30 days with reminder task, daily limits, duplicate check, Saxovat price rule.
4. search: PostgreSQL full-text with Latin/Cyrillic transliteration, filters (section, category, attributes, price, condition, district, distance, verified only), sorting, cursor pagination 20, TOP ordering placeholder, favorites, saved searches (storage only).
5. listings/map endpoint with clustering by zoom.
6. requests (Saxovat): send request, choose, give, rules per 18.4.
7. moderation v1: auto filters (banned words, phone/link in text), moderation queue states, reports and blocks endpoints.
8. Django admin (django-unfold): users, listings with moderation actions, reports, categories, banned words, limits settings, dashboard counters.

APP:
1. Onboarding, language, city, phone and SMS screens (see mockup Splash) with exact validation and error texts.
2. Home (mockup Main): location, search bar, section chips, nearby free items row, TOP grid, native ad placeholder, skeleton/empty/error states.
3. Search, filter bottom sheet, results (grid/list), map screen with clusters.
4. Listing detail for Savdo (mockup Listing) and Saxovat (mockup Gift, request sheet), favorites, share, report, contact via phone/Telegram.
5. Create-listing flow (5 steps, mockup Create): section choice, photos (compress, reorder), details with dynamic attributes, location picker, preview, draft autosave and offline queue.
6. Profile: my listings tabs, favorites, saved searches, settings (language, theme, notifications, delete account).

ACCEPTANCE: SPEC section 20.2 criteria for stage 1; a user can register by SMS, post Saxovat and Savdo listings in under 60 seconds, find them by search and on the map, send a Saxovat request; admin can moderate; all strings in 3 languages; tests and CI green; short demo script in docs/DEMO.md.
```

### Bosqich 2: chat va ishonch

```text
PHASE 2 - CHAT AND TRUST. Implements SPEC 5.4, 5.5, 18.5, 18.7, 18.8, 18.10, 18.12, 19 (user-facing notifications), 8.4, 17.3.

BACKEND:
1. chat: conversations per listing, Channels consumer with auth, message types (text, image, location, offer, system), delivery states, unread counters, spam rules and risky-phrase warnings per 18.10, block handling, push fallback when offline.
2. offers: price offers and counter-offers per 18.5, expiry task, system messages.
3. swap: swap listings and offers per 18.7. wanted: wanted posts with matching task and capped notifications per 18.8.
4. reviews: reviews and ratings per 18.12, badges and statistics (impact card data), monthly top.
5. notifications: FCM/APNs service, notification model, catalog from SPEC 19 with templates in 3 languages, user preferences, quiet hours, daily caps, saved-search digest, price-drop and expiry reminders.
6. Security review of all chat endpoints (permissions, rate limits, payload size).

APP:
1. Chats list and conversation screens (mockup Chat): bubbles, offer cards with accept/decline, quick replies, typing indicator, image sending, report/block, safety notice.
2. Notification center and push handling with deep links.
3. Ratings, reviews, badges, impact statistics card with share image (mockup Profile).
4. Swap flow and Wanted flow screens; Saxovat request management for the giver.
5. Motion per SPEC 17.3 and 17.5 (favorite pop, send animation, rolling numbers, Done confetti with reduce-motion fallback).

ACCEPTANCE: two test accounts can chat in real time, exchange and accept offers, receive correct push notifications with deep links; swap, wanted and ratings flows pass tests; load test of chat with 500 concurrent connections documented; SPEC 20.2 stage 2 criteria met.
```

### Bosqich 3: monetizatsiya (to'lov, TOP, reklama)

```text
PHASE 3 - MONETIZATION. Implements SPEC 5.6, 9, 18.11, 7.10, 15.3. Money code needs extra care: write more tests than usual and explain every design decision in the PR.

BACKEND:
1. payments: wallet and transaction ledger (double-entry style, immutable records), provider interface with Click, Payme and Uzum adapters, create-payment, webhook endpoints with signature verification and idempotency, reconciliation task, refunds per 18.11, receipts.
2. promotions: TOP (1/3/7 days), highlight, auto-boost schedule via Celery Beat, category+city ranking integration with search, expiry and reminders, prices editable in admin.
3. Listing packages for cars and real estate, daily free limits, business profiles and subscription plans (data model + enforcement).
4. ads: local advertiser placements (admin-managed), API for placements; remote-config flags for ad frequency.
5. Admin: finance dashboard, transactions with filters and export, refund action (finance role only), promotion management.

APP:
1. Wallet screen, top-up flow with provider redirect and return handling, payments history.
2. Promote-listing flow (mockup in SPEC 8.4 payment step): package choice, payment method, success animation (TOP border and badge).
3. AdMob and Yandex Ads with mediation: banner on search results bottom and profile, native ad every 8th card in lists with clear "Reklama" label, rewarded ad for bonus (if enabled), consent flow (iOS ATT, privacy), frequency caps from remote config; never show ads during listing creation or chat.
4. Store-compliance review: digital-goods payment rules for Apple/Google (SPEC 9.4). Produce docs/STORE_PAYMENT_NOTES.md with the options and your recommendation; do not ship payments in iOS until I decide.

ACCEPTANCE: sandbox payments for all three providers pass the happy path, duplicate webhooks do not double-credit, failed and delayed payments handled, refunds work, TOP appears and expires on time, ads show only in allowed places; SPEC 20.2 stage 3 criteria met.
```

### Bosqich 4: Baraholka va ijtimoiy qism

```text
PHASE 4 - BARAHOLKA AND COMMUNITY. Implements SPEC 4.3, 4.6, 5.5, 18.6, 18.13, 18.14, 8.5, 17.5.

BACKEND:
1. auctions: durations 24h/48h/3d/7d, start price, step rules by price band, bid validation, 5-minute anti-sniping extension, exact closing by Celery task (and safe recovery if a worker was down), second-bidder fallback after 48h, race-condition safe bidding (database locking or atomic update) with concurrency tests, WebSocket live updates.
2. organizations (Ehtiyojmandlar): application with document upload, admin verification workflow, need-lists with priorities, help offers, stale-list reminders, abuse handling.
3. masters directory (repair masters), Baraholka condition labels, daily finds feed, editor picks.
4. campaigns: seasonal banners, top lists, segmented push, admin tools. Neighborhood notifications with consent and daily caps.
5. moderation v2: severity-based queue, appeals, moderator performance report, duplicate-image detection.

APP:
1. Auction screen (mockup Auction): live timer, stepper bid control, confirmation, history, extension animation, outbid notification handling.
2. Baraholka feed with retro stamp labels, finds feed; masters directory.
3. Ehtiyojmandlar screens: organizations list, need-lists, help flow, verified badge.
4. Impact share card, seasonal campaign banners, neighborhood notification settings.

ACCEPTANCE: concurrent bid tests (100 simultaneous bids) produce a correct winner; auctions close at the exact time and extend correctly; organization verification flow works end-to-end; SPEC 20.2 stage 4 criteria met.
```

### Bosqich 5: kengayish va chiqarishga tayyorlash

```text
PHASE 5 - HARDENING, RELEASE AND EXPANSION. Implements SPEC 15, 16 (phase 5), 10.4.

1. Security: dependency audit, OWASP API/Mobile checklist, rate-limit review, secrets review, penetration-test preparation notes, admin 2FA and IP restriction, backup and restore drill documented.
2. Performance: profile slow queries, add missing indexes, caching, image CDN, load test (k6 or Locust) with targets from SPEC 11.5; fix findings.
3. Observability: Sentry, structured logs, Prometheus + Grafana dashboards, alerts via Telegram bot.
4. Release engineering: Fastlane lanes for Android (AAB) and iOS (TestFlight), staged rollout, forced-update mechanism (HTTP 426), maintenance screen, remote config.
5. Store readiness: privacy policy and terms pages, data-safety and privacy-label answers, account deletion web page, UGC moderation evidence, screenshots, descriptions in uz and ru (ASO), age rating.
6. Business features: business subscriptions UI, delivery partner integration (interface + one adapter), Telegram channel autoposting and bot, image-based category suggestion (optional, behind a flag), price suggestion (basic).
7. Multi-city expansion: city configuration, per-city pricing and TOP slots.

ACCEPTANCE: SPEC 20.2 "every stage" criteria; production runbook in docs/RUNBOOK.md; zero critical/high findings open; beta released to TestFlight and Google Play internal testing.
```

## Har bosqichda tekshirish ro'yxati

Agent "tayyor" deganda ham quyidagilarni o'zingiz yoki dasturchi tekshiring. Agent ishini ishonib qabul qilmang, natijani ko'ring.

### Har bosqich tugaganda (umumiy)

- [ ] Barcha testlar va CI yashil; agent test natijasini haqiqiy ko'rsatdi
- [ ] Loyiha toza muhitda `docker compose up` bilan ishga tushadi (backend) va ilova emulyatorda ochiladi
- [ ] Ekranlar maketga (`docs/design/`) mos: ranglar, o'lchamlar, Coral ustida Navy matn
- [ ] Barcha matnlar uch tilda; xato va bildirishnoma matnlari SPEC 18 va 19 bo'yicha
- [ ] Kalit va parollar kodda yoki git tarixida yo'q (`.env.example` bor)
- [ ] Har bir yangi endpointda ruxsat, tezlik cheklovi va test bor
- [ ] `docs/DECISIONS.md` dagi ochiq savollarga javob berdim
- [ ] SPEC 20.2 dagi shu bosqich mezonlari qo'lda sinab ko'rildi
- [ ] Haqiqiy Android va iPhone qurilmada sinab ko'rildi

### Alohida diqqat talab qiladigan joylar (odam ko'rib chiqsin)

| Qism | Nimani tekshirish |
| --- | --- |
| SMS kirish | Urinish chegaralari, kod muddati, bloklash, bir raqamga ko'p SMS yuborilmasligi |
| Ruxsatlar | Boshqa foydalanuvchining e'lon, chat, to'lovini ko'rish yoki o'zgartirish mumkin emasligi |
| Joylashuv | Aniq koordinata hech qaysi API javobida chiqmasligi |
| To'lov | Webhook imzosi, ikki marta hisoblanmasligi, summani mijozdan olmaslik, qaytarish jarayoni |
| Auksion | Bir vaqtdagi stavkalar, yopilish vaqti, vaqt uzayishi |
| Rasm yuklash | Fayl turi va hajmi, EXIF o'chirilishi, zararli fayl |
| Shaxsiy ma'lumot | Akkauntni o'chirish to'liq ishlashi, loglarda telefon va token yo'qligi |
| Moderatsiya | Taqiqlangan tovar filtri, shikoyat navbati, apellyatsiya |
| Do'kon qoidalari | Akkaunt o'chirish, UGC shikoyat/bloklash, maxfiylik siyosati, to'lov siyosati (SPEC 15.3) |

### Agent bilan ishlash bo'yicha amaliy maslahatlar

- Bitta xabarda bitta bosqich yoki bitta funksiya bering. "Hammasini yoz" demang.
- Agent chalkashsa yoki xato qilsa, vazifani qisqartiring va aniq SPEC bo'limini ko'rsating.
- Har hafta oxirida agentdan "nima qilindi, nima qolgan, xavflar nima" hisobotini so'rang.
- Agent SPEC'ga zid narsa yozsa, "SPEC 18.x bo'yicha tuzat" deb aniq raqam bilan ayting.
- Muhim qismlar (to'lov, xavfsizlik, ma'lumotlar bazasi sxemasi) uchun ikkinchi bir agent yoki dasturchi "kod ko'rigi" (review) qilsin.
- Har bosqichdan keyin git teg qo'ying (`v0.1-mvp` va h.k.), muammo bo'lsa orqaga qaytish oson bo'ladi.
