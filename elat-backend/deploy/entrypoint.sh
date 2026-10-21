#!/usr/bin/env bash
# Entrypoint dispatches on the first argument: web | worker | beat.
set -euo pipefail

wait_for_db() {
  echo "Waiting for database..."
  python - <<'PY'
import os, time
import environ
import psycopg

env = environ.Env()
url = os.environ.get("DATABASE_URL", "postgis://elat:elat@db:5432/elat")
# psycopg understands postgresql:// — strip the GeoDjango postgis:// prefix.
dsn = url.replace("postgis://", "postgresql://", 1)
for _ in range(60):
    try:
        with psycopg.connect(dsn, connect_timeout=2):
            break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("Database not reachable")
print("Database is up.")
PY
}

case "${1:-web}" in
  web)
    wait_for_db
    python manage.py migrate --noinput
    python manage.py seed_catalog || true
    exec python manage.py runserver 0.0.0.0:8000
    ;;
  worker)
    wait_for_db
    exec celery -A config worker -l info
    ;;
  beat)
    wait_for_db
    exec celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ;;
  *)
    exec "$@"
    ;;
esac
