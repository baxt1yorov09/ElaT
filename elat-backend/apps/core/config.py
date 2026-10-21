"""Access to SPEC §18 numeric limits.

Resolution order: RuntimeConfig row (admin-editable) -> settings.ELAT_LIMITS default.
Business logic must call get_limit(); limits are never hardcoded (CLAUDE.md rule).
"""

from __future__ import annotations

from django.conf import settings
from django.core.cache import cache

_CACHE_PREFIX = "elat:limit:"
_CACHE_TTL = 60  # seconds; admin edits take effect within a minute


def get_limit(key: str) -> int:
    """Return the effective value for a limit key."""
    if key not in settings.ELAT_LIMITS:
        raise KeyError(f"Unknown Elat limit: {key!r}")

    cache_key = f"{_CACHE_PREFIX}{key}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    value = settings.ELAT_LIMITS[key]
    # Local import to avoid AppRegistryNotReady at import time.
    from apps.core.models import RuntimeConfig

    try:
        value = RuntimeConfig.objects.get(key=key).value
    except RuntimeConfig.DoesNotExist:
        pass

    cache.set(cache_key, value, _CACHE_TTL)
    return value


def clear_limit_cache(key: str | None = None) -> None:
    if key is None:
        for k in settings.ELAT_LIMITS:
            cache.delete(f"{_CACHE_PREFIX}{k}")
    else:
        cache.delete(f"{_CACHE_PREFIX}{key}")
