from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PingView(APIView):
    """Public liveness endpoint for the versioned API."""

    permission_classes = [AllowAny]
    throttle_classes = []

    @extend_schema(
        summary="Ping",
        responses={200: {"type": "object", "properties": {"pong": {"type": "boolean"}}}},
        tags=["core"],
    )
    def get(self, request: Request) -> Response:
        return Response({"pong": True})
