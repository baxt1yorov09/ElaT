# Changelog

All notable changes to Elat are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); the project uses conventional commits and phase
tags (`v0.0-foundations`, `v0.1-mvp`, …).

## [Unreleased]

### Phase 0 — Foundations (in progress)
- Monorepo initialized (`elat-backend/`, `elat-app/`, shared `docs/`).
- Planning docs: `IMPLEMENTATION_PLAN.md`, `DECISIONS.md`.
- Root tooling: `.gitignore`, `README.md`, CI workflow (path-filtered backend + app jobs).
- Backend skeleton: Django project, 16 modular apps, core (base model, error format, i18n,
  throttling, audit log, config/limits), health endpoint, drf-spectacular OpenAPI.
- Backend tooling: ruff, mypy, pytest + pytest-django, factory_boy, coverage, pre-commit.
- Backend infra: Dockerfile, docker-compose (django, postgres+postgis, redis, celery worker+beat,
  minio), `.env.example`.
- Backend data: `seed_catalog` command (cities, districts, categories tree + attribute schemas).
- App skeleton: Flutter project, dev/staging/prod flavors, l10n (uz-Latn, uz-Cyrl, ru),
  go_router 5-tab shell with raised center "+" button.
- App design tokens: `core/theme` (colors incl. Navy/Coral + section colors, typography, spacing,
  radii, light + dark) and `core/motion` (durations + curves from SPEC §17.1).
- App shared widgets + gallery screen with widget tests.
