from __future__ import annotations

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    DeleteAccountView,
    DeviceView,
    LogoutView,
    MeView,
    SmsSendView,
    SmsVerifyView,
)

app_name = "users"

urlpatterns = [
    # Auth (§13, §18.1)
    path("auth/sms/send", SmsSendView.as_view(), name="sms-send"),
    path("auth/sms/verify", SmsVerifyView.as_view(), name="sms-verify"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    # Profile (§18.2)
    path("users/me", MeView.as_view(), name="me"),
    path("users/me/delete", DeleteAccountView.as_view(), name="delete-account"),
    path("devices", DeviceView.as_view(), name="devices"),
]
