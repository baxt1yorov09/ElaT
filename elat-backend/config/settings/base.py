"""Base settings shared by all environments.

Values are read from the environment (see .env.example). Secrets never live in code.
Numeric product limits (SPEC §18) live in ELAT_LIMITS as defaults and are overridable at
runtime by the admin-editable config model in apps.core (see apps.core.config).
"""

from __future__ import annotations

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CORS_ALLOWED_ORIGINS=(list, []),
    USE_S3=(bool, False),
)

# Read .env if present (dev/local); in prod the environment is injected directly.
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

SECRET_KEY = env("SECRET_KEY", default="insecure-dev-key-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    "unfold",  # must precede django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # per-device refresh revocation (§18.1)
    "drf_spectacular",
    "corsheaders",
    "channels",
    "django_celery_beat",
]

LOCAL_APPS = [
    "apps.core",
    "apps.users",
    "apps.catalog",
    "apps.listings",
    "apps.requests",
    "apps.auctions",
    "apps.chat",
    "apps.search",
    "apps.reviews",
    "apps.notifications",
    "apps.payments",
    "apps.ads",
    "apps.moderation",
    "apps.organizations",
    "apps.masters",
    "apps.campaigns",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Accept-Language -> request language
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Database (PostgreSQL + PostGIS)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgis://elat:elat@localhost:5432/elat"),
}

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization (uz-Latn, uz-Cyrl, ru)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "uz"
LANGUAGES = [
    ("uz", "O'zbekcha (lotin)"),
    ("uz-cyrl", "Ўзбекча (кирилл)"),
    ("ru", "Русский"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media / object storage (S3-compatible; env-driven, see DECISIONS D10)
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_collected"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

USE_S3 = env("USE_S3")
if USE_S3:
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="elat-media")
    AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default="") or None
    AWS_QUERYSTRING_AUTH = True
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3.S3Storage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Cache & Channels (Redis)
# ---------------------------------------------------------------------------
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    },
}

# ---------------------------------------------------------------------------
# Celery
# ---------------------------------------------------------------------------
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=REDIS_URL)
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 10 * 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_TIMEZONE = TIME_ZONE

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": (
        "apps.core.throttling.AnonBurstThrottle",
        "apps.core.throttling.UserBurstThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/min",
        "user": "240/min",
        "sms": "3/hour",
    },
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.CursorPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "apps.core.exceptions.elat_exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ---------------------------------------------------------------------------
# JWT (SPEC §18.1: access 15 min, refresh 30 days)
# ---------------------------------------------------------------------------
from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# ---------------------------------------------------------------------------
# OpenAPI (drf-spectacular)
# ---------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Elat API",
    "DESCRIPTION": "Elat marketplace API. See docs/SPEC.md §13.",
    "VERSION": "0.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]+",
    "COMPONENT_SPLIT_REQUEST": True,
}

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")

# ---------------------------------------------------------------------------
# Elat product limits (SPEC §18 defaults). Overridable at runtime via apps.core.config.
# ---------------------------------------------------------------------------
ELAT_LIMITS: dict[str, int] = {
    # Auth (§18.1)
    "sms_code_ttl_seconds": 5 * 60,
    "sms_resend_cooldown_seconds": 60,
    "sms_per_phone_per_hour": 3,
    "sms_per_phone_per_day": 10,
    "sms_max_wrong_attempts": 5,
    "sms_lockout_minutes": 15,
    # Listings (§18.3)
    "listing_images_min": 1,
    "listing_images_max": 10,
    "listing_title_min": 5,
    "listing_title_max": 70,
    "listing_description_min": 20,
    "listing_description_max": 2000,
    "listing_expiry_days": 30,
    "listing_expiry_reminder_days": 3,
    "listing_daily_limit_new_user": 5,
    "listing_daily_limit_verified": 20,
    "listing_location_hidden_radius_m": 300,
    "draft_ttl_days": 7,
    # Saxovat requests (§18.4)
    "gift_request_reason_min": 10,
    "gift_request_reason_max": 300,
    "gift_request_daily_limit": 10,
    "gift_chosen_confirm_hours": 48,
    # Search (§18.9)
    "search_query_min": 2,
    "search_query_max": 100,
    "saved_searches_max": 20,
    "recent_searches_max": 10,
    "page_size": 20,
}

SMS_PROVIDER = env("SMS_PROVIDER", default="console")
# Eskiz / Playmobile credentials (env only; never in code). See .env.example.
SMS_ESKIZ_EMAIL = env("SMS_ESKIZ_EMAIL", default="")
SMS_ESKIZ_PASSWORD = env("SMS_ESKIZ_PASSWORD", default="")
SMS_ESKIZ_BASE_URL = env("SMS_ESKIZ_BASE_URL", default="https://notify.eskiz.uz/api")
SMS_SENDER = env("SMS_SENDER", default="4546")

# Uzbek mobile operator codes (the 2 digits after +998). SPEC §18.1 validates these.
UZ_PHONE_OPERATOR_CODES: list[str] = env(
    "UZ_PHONE_OPERATOR_CODES",
    default=["20", "33", "50", "55", "77", "88", "90", "91", "93", "94", "95", "97", "98", "99"],
)
