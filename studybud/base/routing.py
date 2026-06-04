"""WebSocket URL routing for the base app.

Maps WebSocket URL patterns to their corresponding consumers.
"""

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/chat/(?P<room_id>\d+)/$',
        consumers.ChatConsumer.as_asgi(),
    ),
]
