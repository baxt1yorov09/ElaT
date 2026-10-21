"""Development settings: verbose, permissive hosts, console SMS."""

from __future__ import annotations

from .base import *  # noqa: F401,F403
from .base import INSTALLED_APPS, env

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Browsable API is handy in dev.
from .base import REST_FRAMEWORK  # noqa: E402

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if env.bool("DEBUG_TOOLBAR", default=False):  # optional, only if installed
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
