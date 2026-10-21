from __future__ import annotations

from django.urls import path

from apps.core.api import PingView

app_name = "core"

urlpatterns = [
    path("ping", PingView.as_view(), name="ping"),
    # Feature routers are included from here as phases land, e.g.:
    # path("", include("apps.users.urls")),
]
