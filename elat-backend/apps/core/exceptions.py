"""Unified API error format: {code, message, details}.

`code` is a stable machine string (e.g. "not_found", "throttled", "validation_error").
`message` is a human, localized summary (Accept-Language via LocaleMiddleware).
`details` carries field-level errors or extra context (may be empty).
"""

from __future__ import annotations

from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def _code_for(exc: Any, response: Response) -> str:
    default_code = getattr(exc, "default_code", None)
    if default_code:
        return str(default_code)
    return {
        status.HTTP_400_BAD_REQUEST: "bad_request",
        status.HTTP_401_UNAUTHORIZED: "not_authenticated",
        status.HTTP_403_FORBIDDEN: "permission_denied",
        status.HTTP_404_NOT_FOUND: "not_found",
        status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
        status.HTTP_429_TOO_MANY_REQUESTS: "throttled",
    }.get(response.status_code, "error")


def _message_and_details(data: Any) -> tuple[str, Any]:
    """Split DRF error payload into a top-level message and structured details."""
    if isinstance(data, dict):
        if "detail" in data and len(data) == 1:
            return str(data["detail"]), {}
        return str(_("Request could not be processed.")), data
    if isinstance(data, list):
        first = str(data[0]) if data else str(_("Error."))
        return first, {"errors": data}
    return str(data), {}


def elat_exception_handler(exc: Any, context: Any) -> Response | None:
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    message, details = _message_and_details(response.data)
    response.data = {
        "code": _code_for(exc, response),
        "message": message,
        "details": details,
    }
    return response
