"""SMS provider abstraction (SPEC §11.4, §18.1).

The provider is chosen by settings.SMS_PROVIDER so infrastructure stays swappable
(DECISIONS D10: env-driven). Dev uses the console provider; production uses Eskiz.
Credentials come from the environment only, never from code.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from django.conf import settings

logger = logging.getLogger("elat.sms")


class SmsProvider(ABC):
    @abstractmethod
    def send(self, phone: str, message: str) -> None:  # pragma: no cover - interface
        ...


class ConsoleSmsProvider(SmsProvider):
    """Writes the SMS to the log. Used in dev/test; never in production."""

    def send(self, phone: str, message: str) -> None:
        logger.info("SMS to %s: %s", phone, message)


class EskizSmsProvider(SmsProvider):
    """Eskiz.uz provider. Networking is added when real credentials are configured.

    Intentionally fails loudly if used without credentials so we never silently drop
    a production login SMS.
    """

    def __init__(self) -> None:
        self.base_url = settings.SMS_ESKIZ_BASE_URL
        self.email = settings.SMS_ESKIZ_EMAIL
        self.password = settings.SMS_ESKIZ_PASSWORD
        self.sender = settings.SMS_SENDER

    def send(self, phone: str, message: str) -> None:
        if not (self.email and self.password):
            raise RuntimeError("Eskiz SMS credentials are not configured")
        # Real HTTP integration is wired in Phase 1 hardening once credentials exist.
        raise NotImplementedError("Eskiz HTTP send is not wired yet (needs credentials)")


_PROVIDERS: dict[str, type[SmsProvider]] = {
    "console": ConsoleSmsProvider,
    "eskiz": EskizSmsProvider,
}


def get_sms_provider() -> SmsProvider:
    name = getattr(settings, "SMS_PROVIDER", "console")
    provider_cls = _PROVIDERS.get(name, ConsoleSmsProvider)
    return provider_cls()
