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