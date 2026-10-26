"""Auth and profile API views (SPEC §13, §18.1, §18.2). Views are thin; logic is in services."""

from __future__ import annotations

from typing import Any, cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.throttling import AnonBurstThrottle, SmsSendThrottle

from . import services
from .models import User
from .permissions import IsNotBlocked
from .serializers import (
    DeleteAccountSerializer,
    DeviceSerializer,
    ProfileUpdateSerializer,
    RefreshSerializer,
    SmsSendResponseSerializer,
    SmsSendSerializer,
    SmsVerifySerializer,
    TokenPairSerializer,
    UserSerializer,
)


def _client_ip(request: Request) -> str | None:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _device_meta(request: Request, extra: dict[str, Any] | None) -> dict[str, Any]:
    extra = extra or {}
    return {
        "platform": extra.get("platform", ""),
        "app_version": extra.get("app_version", ""),
        "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        "ip": _client_ip(request),
    }


class SmsSendView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonBurstThrottle, SmsSendThrottle]

    @extend_schema(
        request=SmsSendSerializer,
        responses={200: SmsSendResponseSerializer},
        summary="Send SMS login code",
        tags=["auth"],
    )
    def post(self, request: Request) -> Response:
        serializer = SmsSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = services.request_code(serializer.validated_data["phone"])
        return Response(
            {"phone": result.phone, "resend_after_seconds": result.resend_after_seconds}
        )


class SmsVerifyView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonBurstThrottle]

    @extend_schema(
        request=SmsVerifySerializer,
        responses={200: TokenPairSerializer},
        summary="Verify SMS code and get tokens",
        tags=["auth"],
    )
    def post(self, request: Request) -> Response:
        serializer = SmsVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = services.verify_code(
            data["phone"], data["code"], _device_meta(request, data.get("device"))
        )
        payload = {
            "access": result.access,
            "refresh": result.refresh,
            "is_new": result.is_new,
            "user": UserSerializer(result.user).data,
        }
        return Response(payload)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=RefreshSerializer, responses={204: None}, tags=["auth"])
    def post(self, request: Request) -> Response:
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.logout(serializer.validated_data["refresh"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes = [IsAuthenticated, IsNotBlocked]

    @extend_schema(responses={200: UserSerializer}, summary="Current profile", tags=["users"])
    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data)

    @extend_schema(
        request=ProfileUpdateSerializer,
        responses={200: UserSerializer},
        summary="Update profile",
        tags=["users"],
    )
    def patch(self, request: Request) -> Response:
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = services.update_profile(cast(User, request.user), serializer.validated_data)
        return Response(UserSerializer(user).data)


class DeviceView(APIView):
    permission_classes = [IsAuthenticated, IsNotBlocked]

    @extend_schema(request=DeviceSerializer, responses={201: DeviceSerializer}, tags=["users"])
    def post(self, request: Request) -> Response:
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        device = services.register_device(
            cast(User, request.user),
            data["fcm_token"],
            data["platform"],
            data.get("app_version", ""),
        )
        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=DeleteAccountSerializer,
        responses={204: None},
        summary="Delete account (SMS-confirmed, irreversible)",
        tags=["users"],
    )
    def post(self, request: Request) -> Response:
        serializer = DeleteAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.delete_account(cast(User, request.user), serializer.validated_data["code"])
        return Response(status=status.HTTP_204_NO_CONTENT)
