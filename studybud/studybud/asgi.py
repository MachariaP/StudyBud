"""ASGI configuration for studybud project.

Exposes the ASGI application as a module-level variable named ``application``,
supporting both HTTP (Django) and WebSocket (Channels) protocols.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')

django_asgi_app = get_asgi_application()

from base.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
