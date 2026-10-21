"""Throttling classes (SPEC §13: anon 60/min, user 240/min, SMS separate).

Rates are configured in REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].
SmsSendThrottle is applied per-view on the SMS send endpoint in Phase 1, keyed by phone.
"""

from __future__ import annotations

from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle, UserRateThrottle


class AnonBurstThrottle(AnonRateThrottle):
    scope = "anon"


class UserBurstThrottle(UserRateThrottle):
    scope = "user"


class SmsSendThrottle(SimpleRateThrottle):
    """Keyed by the target phone number (set by the view as request.throttle_phone)."""

    scope = "sms"

    def get_cache_key(self, request, view):
        phone = getattr(request, "throttle_phone", None)
        if not phone:
            return None
        return self.cache_format % {"scope": self.scope, "ident": phone}
