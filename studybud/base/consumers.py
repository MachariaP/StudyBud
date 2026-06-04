"""WebSocket consumers for real-time chat functionality.

Provides ChatConsumer for handling WebSocket connections in study rooms,
enabling real-time messaging and typing indicators without page reloads.
"""

import json

from typing import Any, Optional

from django.contrib.auth.models import User
from django.utils import timesince
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """Async WebSocket consumer for room-based chat.

    Handles connect, disconnect, receive, and custom event handlers for
    broadcasting messages and typing indicators within a room group.

    Attributes:
        room_id: The database ID of the room this consumer is connected to.
        room_group_name: The Channels group name for this room (e.g. 'chat_42').
        user: The authenticated Django User instance.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the consumer with no room context; set during connect."""
        super().__init__(*args, **kwargs)
        self.room_id: Optional[str] = None
        self.room_group_name: Optional[str] = None
        self.user: Optional[User] = None

    async def connect(self) -> None:
        """Authenticate user and join the room group.

        Validates that:
        1. The user is authenticated.
        2. The room ID from the URL path exists in the database.

        On success, accepts the WebSocket and adds the user to the room group.
        On failure, closes the connection with a 4000 close code.
        """
        self.user = self.scope.get('user')
        if not self.user or not self.user.is_authenticated:
            await self.close(code=4000)
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        room_exists = await self._room_exists(self.room_id)
        if not room_exists:
            await self.close(code=4004)
            return

        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """Leave the room group on disconnect.

        Args:
            close_code: WebSocket close code indicating reason for disconnect.
        """
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data: Optional[str] = None) -> None:
        """Handle an incoming WebSocket message from the client.

        Parses JSON payload and dispatches to the appropriate handler based
        on the ``type`` field.

        Supported types:
            - ``message``: Persist and broadcast a new chat message.
            - ``typing``: Broadcast typing indicator state to the room.

        Args:
            text_data: Raw JSON string from the WebSocket.
        """
        if not text_data:
            return

        data = json.loads(text_data)
        event_type = data.get('type')

        if event_type == 'message':
            await self._handle_message(data)
        elif event_type == 'typing':
            await self._handle_typing(data)

    async def _handle_message(self, data: dict[str, Any]) -> None:
        """Persist a message to the database and broadcast it to the room group.

        Args:
            data: Parsed JSON dict with keys:
                - body: The message text content.
        """
        body: str = data.get('body', '').strip()
        if not body:
            return

        message = await self._save_message(
            room_id=self.room_id,
            user=self.user,
            body=body,
        )

        avatar_url = await self._get_avatar_url(self.user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': message.id,
                'user': self.user.username,
                'user_id': self.user.id,
                'body': message.body,
                'created': timesince.timesince(message.created) + ' ago',
                'created_raw': message.created.isoformat(),
                'avatar_url': avatar_url,
            },
        )

    async def _handle_typing(self, data: dict[str, Any]) -> None:
        """Broadcast typing indicator state to the room group.

        Args:
            data: Parsed JSON dict with keys:
                - typing: Boolean indicating if user is currently typing.
        """
        is_typing: bool = data.get('typing', False)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user': self.user.username,
                'typing': is_typing,
            },
        )

    async def chat_message(self, event: dict[str, Any]) -> None:
        """Send a new_message event to the WebSocket client.

        Called by the channel layer when another consumer in the group
        broadcasts a ``chat_message`` event.

        Args:
            event: Dict containing message fields (id, user, user_id, body,
                   created, created_raw).
        """
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'id': event['id'],
            'user': event['user'],
            'user_id': event['user_id'],
            'body': event['body'],
            'created': event['created'],
            'created_raw': event['created_raw'],
            'avatar_url': event.get('avatar_url'),
        }))

    async def typing_indicator(self, event: dict[str, Any]) -> None:
        """Send a user_typing event to the WebSocket client.

        Args:
            event: Dict with keys ``user`` (str) and ``typing`` (bool).
        """
        await self.send(text_data=json.dumps({
            'type': 'user_typing',
            'user': event['user'],
            'typing': event['typing'],
        }))

    @database_sync_to_async
    def _get_avatar_url(self, user):
        """Get the user's avatar URL or None if not set.

        Args:
            user: The Django User instance.

        Returns:
            str or None: Absolute URL to the avatar image, or None.
        """
        try:
            profile = user.profile
            if profile.avatar:
                return profile.avatar.url
        except user._meta.model.profile.RelatedObjectDoesNotExist:
            pass
        return None

    @database_sync_to_async
    def _room_exists(self, room_id: str) -> bool:
        """Check if a room with the given ID exists in the database.

        Args:
            room_id: The room's primary key as a string.

        Returns:
            True if the room exists, False otherwise.
        """
        return Room.objects.filter(id=room_id).exists()

    @database_sync_to_async
    def _save_message(self, room_id: str, user: User, body: str) -> Message:
        """Create and persist a new Message instance.

        Also adds the user to the room's participants if not already present.

        Args:
            room_id: The room's primary key.
            user: The authenticated user sending the message.
            body: The message text content.

        Returns:
            The newly created Message instance.
        """
        room = Room.objects.get(id=room_id)
        message = Message.objects.create(
            user=user,
            room=room,
            body=body,
        )
        room.participants.add(user)
        return message
