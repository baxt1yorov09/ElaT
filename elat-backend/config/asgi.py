"""ASGI entrypoint.

HTTP is served by Django; WebSocket routing is added in Phase 2 (chat) and Phase 4 (auctions)
via channels ProtocolTypeRouter. For now only the HTTP application is wired up.
"""

from __future__ import annotations

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # "websocket": ... added in Phase 2
    }
)
