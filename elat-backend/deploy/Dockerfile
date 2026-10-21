# Elat backend image (Python 3.12 per SPEC / DECISIONS D13).
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# GeoDjango + psycopg system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
        gdal-bin libgdal-dev binutils libproj-dev \
        libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (layer cache). dev extra is included for tests/lint in CI + local.
COPY pyproject.toml ./
RUN python -m pip install --upgrade pip && pip install -e '.[dev]'

# App source.
COPY . .

COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["web"]
