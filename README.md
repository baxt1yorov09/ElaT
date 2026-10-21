# Elat

Elat is a multi-section marketplace for Uzbekistan built around the idea of giving things a
"second life": free items (Saxovat), normal sales (Savdo), a flea market with auctions (Baraholka),
swaps, wanted posts, and charity need-lists. iOS + Android app, Django backend, admin panel.

This is a **monorepo**:

| Path | What |
| --- | --- |
| `docs/` | Source of truth: `SPEC.md` (full spec, Uzbek), `design.pdf` (mockups), `IMPLEMENTATION_PLAN.md`, `DECISIONS.md`, `CHANGELOG.md` |
| `elat-backend/` | Python 3.12 · Django 5 · DRF · Channels · Celery · PostgreSQL/PostGIS · Redis |
| `elat-app/` | Flutter 3 · Riverpod · go_router · dio |
| `.github/workflows/` | CI (separate, path-filtered backend + app jobs) |

## Quick start (backend)

```bash
cd elat-backend
cp .env.example .env            # fill in secrets locally; never commit .env
docker compose up               # django, postgres+postgis, redis, celery worker+beat, minio
# API docs: http://localhost:8000/api/docs
# Health:   http://localhost:8000/healthz
```

Common commands:

```bash
pytest -q --cov=apps            # tests + coverage
ruff check . && ruff format .   # lint + format
mypy apps                       # type check
python manage.py migrate
python manage.py seed_catalog   # cities, districts, categories + attributes
```

## Quick start (app)

```bash
cd elat-app
flutter pub get
dart run build_runner build --delete-conflicting-outputs
flutter gen-l10n
flutter run --flavor dev -t lib/main_dev.dart
flutter test
```

## Development status

Phase 0 (foundations) in progress. See `docs/IMPLEMENTATION_PLAN.md` for the full phased plan and
`docs/DECISIONS.md` for resolved decisions and open assumptions.

> Security: never commit secrets. Keep `.env` local and `.env.example` up to date. Exact user
> coordinates never leave the server. Payments and personal data follow `docs/SPEC.md` §10, §15, §18.
