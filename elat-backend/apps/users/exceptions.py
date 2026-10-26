"""Auth domain errors with SPEC §18.1 exact messages (uz-Latn source).

Each maps to the unified {code, message, details} envelope via default_code.
uz-Cyrl and ru come from the gettext catalogs.
"""

from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidPhone(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Telefon raqami noto'g'ri")
    default_code = "invalid_phone"


class InvalidCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Kod noto'g'ri")
    default_code = "invalid_code"


class CodeExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Kod muddati tugadi. Yangisini oling")
    default_code = "code_expired"


class TooManyAttempts(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _("Juda ko'p urinish. 15 daqiqadan keyin urinib ko'ring")
    default_code = "too_many_attempts"


class ResendTooSoon(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _("Qayta yuborishdan oldin biroz kuting")
    default_code = "resend_too_soon"


class AccountBlocked(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("Akkauntingiz bloklangan")
    default_code = "account_blocked"
