from __future__ import annotations

from django.urls import include, path

from apps.core.api import PingView

app_name = "core"

urlpatterns = [
    path("ping", PingView.as_view(), name="ping"),
    # Feature routers (mounted under /api/v1/).
    path("", include("apps.users.urls")),
]
