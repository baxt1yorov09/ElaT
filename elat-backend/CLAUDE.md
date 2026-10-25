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