# Features Implemented

## Feature #1: Real-Time Chat via WebSockets (Completed)
**Goal:** Add real-time messaging using Django Channels without breaking existing HTTP endpoints.
- Installed `channels==4.3.2`, `daphne`, `channels_redis`
- Created `base/consumers.py` — `ChatConsumer` (async connect/disconnect/receive/typing)
- Created `base/routing.py` — WebSocket URL routing
- Updated `settings.py` — `ASGI_APPLICATION`, `CHANNEL_LAYERS`
- Updated `asgi.py` — `ProtocolTypeRouter` for HTTP + WebSocket
- Updated `room.html` — WebSocket JS client with reconnect, typing indicator, HTTP fallback
- Added 8 WebSocket consumer tests
- Total tests: 22 → 30

## Feature #2: Avatar Upload + Rich Profiles (Completed)
**Goal:** Replace hardcoded `randomuser.me` avatar URLs with real uploaded avatars and initials fallback. Add bio field to user profiles.
- Created `Profile` model (OneToOneField → User, `avatar` ImageField, `bio` TextField)
- Added `post_save` signal to auto-create Profile on User creation
- Created and ran migration `base.0002_profile`
- Added `ProfileForm` with avatar + bio fields
- Updated `views.py` — `userProfile` uses `get_or_create` for Profile; `updateUser` handles both `UserForm` + `ProfileForm`
- Added `MEDIA_URL`/`MEDIA_ROOT` to settings; dev media serving in `studybud/urls.py`
- Installed `Pillow`; added to `requirements.txt`
- Updated all templates (`profile.html`, `navbar.html`, `feed_component.html`, `activity_component.html`, `room.html`, `update-user.html`) to use `user.profile.avatar.url` or initials fallback
- Added avatar upload preview JS in `script.js`
- Updated `ChatConsumer` to broadcast `avatar_url` in messages
- Added CSS for `.avatar__initials` (gradient background, centered initial letter) and `.avatar-upload` overlay
- Registered `Profile` in admin
- Added 9 new tests (model, form, view, consumer)
- Total tests: 30 → 39

## Planned Features
- Feature #3: (not yet started)
