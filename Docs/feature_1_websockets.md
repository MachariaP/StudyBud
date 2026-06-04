# Feature #1: WebSockets + Real-time Chat

## What it does
Replaces the HTTP POST + page redirect message flow with a persistent WebSocket connection. When a user sends a message in a room, it appears instantly in all connected clients without a page reload.

## Why it matters
- Transforms StudyBud from a forum-style app into a live collaboration platform.
- Enables real-time study sessions where participants see messages as they're typed.
- Increases engagement by removing the friction of manual page refreshes.
- Foundation for future features: typing indicators, online presence, live notifications.

## High-level Architecture

```
Browser (JS WebSocket)  ←→  Daphne (ASGI)  ←→  Channel Layer (Redis/In-Memory)
                                │
                                ▼
                         ChatConsumer
                         (auth, save, broadcast)
                                │
                                ▼
                         PostgreSQL / SQLite
```

### Components
1. **Daphne** — ASGI HTTP/WebSocket server. Replaces the WSGI server for development (`runserver` with Channels).
2. **Channel Layer** — In-memory (dev) or Redis (prod) pub/sub backbone that routes messages between consumers.
3. **ChatConsumer** — Django Channels `WebsocketConsumer` (sync, simpler) handling:
   - `connect`: Authenticate user via session, add to room group.
   - `receive`: Parse JSON, save `Message` to DB, broadcast to group.
   - `disconnect`: Remove from room group.
   - `typing` event: Broadcast typing indicator to group.
4. **Room Group** — A Channels group per room, named `chat_{room_id}`. All WebSocket connections in the same room join this group.
5. **JavaScript Client** — Native WebSocket in `room.html` with reconnect logic, message send/receive, typing indicator debounce.

## Database Changes
None. Reuses the existing `Message` model (`base/models.py`).

## API Flow (JSON over WebSocket)

### Client → Server
```json
{"type": "message", "body": "Hello!"}
{"type": "typing", "typing": true}
{"type": "typing", "typing": false}
```

### Server → Client
```json
{"type": "new_message", "id": 42, "user": "alice", "user_id": 1, "body": "Hello!", "created": "2 minutes ago"}
{"type": "user_typing", "user": "bob", "typing": true}
{"type": "user_typing", "user": "bob", "typing": false}
```

## Settings & Configuration
- `CHANNEL_LAYERS`: In-memory for dev (`channels.layers.InMemoryChannelLayer`), Redis for prod.
- `ASGI_APPLICATION`: `studybud.asgi.application`
- Add `channels` to `INSTALLED_APPS`.

## Files to create/modify
| File | Change |
|------|--------|
| `requirements.txt` | Add `channels`, `channels_redis`, `daphne` |
| `studybud/settings.py` | Add `channels` to INSTALLED_APPS, add `CHANNEL_LAYERS`, set `ASGI_APPLICATION` |
| `studybud/asgi.py` | Add `ProtocolTypeRouter` + `AuthMiddlewareStack` |
| `base/consumers.py` | New — `ChatConsumer` class |
| `base/routing.py` | New — WebSocket URL routing |
| `base/room.html` | Add WebSocket JS client, override form submit |
| `base/tests.py` | Add consumer unit/integration tests |

## Testing Strategy
1. **Unit test `ChatConsumer`** — Test `connect`, `receive`, `disconnect` using Channels test utilities.
2. **Integration test** — Use `channels.testing.HttpCommunicator` / `WebsocketCommunicator` to simulate two clients in a room, send message, verify broadcast.
3. **Manual test** — Open two browser tabs in different users, send message, verify instant delivery. Test typing indicator. Test disconnect/reconnect.
4. **Regression** — All 22 existing tests must pass unchanged.

## Edge Cases & Limitations
- **Auth**: WebSocket connections require an authenticated session. If unauthenticated, connection is rejected.
- **Reconnect**: JS client retries every 3 seconds on disconnect, keeps message input enabled.
- **Race condition**: Two messages sent simultaneously — both saved independently (SQLite handles concurrency at row level). Order is maintained by DB auto-increment.
- **Channel layer**: In-memory layer doesn't survive server restart. Not an issue for dev. Prod uses Redis.
- **No CSRF**: WebSockets are not subject to CSRF; authentication is session-based.

## Rollback Plan
Set an environment variable `WS_DISABLE=1` and fall back to HTTP POST only (keep existing view). The JS client checks a data attribute on the chat element.
