# StudyBud - AI Agent Reference Guide

## Project Overview
Collaborative learning platform (Django 5.1.2, Channels 4.3.2). Users create topic-based study rooms, post messages via WebSocket, and participate in real-time discussions. Frontend fully redesigned with glassmorphism dark theme.

## Quick Start
```bash
cd studybud
python -m venv .venv && .venv\Scripts\Activate
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

## Project Structure
```
StudyBud/
├── requirements.txt              # Django, channels, sqlparse, asgiref
├── AGENTS.md                     # THIS FILE
├── studybud/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── templates/                # Global templates
│   │   ├── main.html             # Base: Inter font, Material Symbols, toast system, page wrapper
│   │   ├── navbar.html           # Fixed glass header, dropdown, mobile search toggle
│   │   └── login.html            # STALE - standalone login with anime.js, not used
│   ├── static/
│   │   ├── styles/
│   │   │   ├── style.css         # 3574 lines - COMPLETE glassmorphism design system
│   │   │   └── main.css          # STALE - 3 lines, body bisque
│   │   ├── js/
│   │   │   ├── script.js         # Dropdown, avatar preview, toast, password toggle,
│   │   │   │                     # strength indicator, mobile search, char counter,
│   │   │   │                     # press-down, IntersectionObserver stagger, topic chips
│   │   │   └── login.js          # STALE - anime.js SVG path (unused)
│   │   └── images/ + icons/      # SVG assets + favicon.ico
│   ├── base/                     # Main app
│   │   ├── models.py             # Topic, Room, Message, Profile (with post_save signal)
│   │   ├── views.py              # 14 views (250 lines)
│   │   ├── urls.py               # 15 URL patterns
│   │   ├── forms.py              # RoomForm, UserForm, ProfileForm
│   │   ├── consumers.py          # ChatConsumer - WebSocket chat + typing indicators
│   │   ├── routing.py            # WebSocket URL routes
│   │   ├── admin.py              # Registers Room, Topic, Message, Profile
│   │   ├── tests.py              # 43 tests (model + view + WebSocket consumer)
│   │   └── templates/base/       # 16 template files (10 active, 6 stale)
│   └── studybud/                 # Django settings
│       ├── settings.py           # env vars for SECRET_KEY, DEBUG, ALLOWED_HOSTS
│       ├── urls.py               # Routes /admin/, /, + media in DEBUG
│       └── asgi.py               # ProtocolTypeRouter: HTTP + WebSocket
```

## Models (`base/models.py`)
| Model | Fields | Relationships | Notes |
|-------|--------|---------------|-------|
| **Profile** | `user` (OneToOne→User), `avatar` (ImageField, nullable), `bio` (TextField) | CASCADE on user delete | Auto-created via `post_save` signal on User |
| **Topic** | `name` (CharField 200) | 1:M to Room | |
| **Room** | `host` (FK→User, SET_NULL), `topic` (FK→Topic, SET_NULL), `name` (CharField 200), `description` (TextField, nullable), `participants` (M2M→User), `updated`, `created` | Ordered by `[-updated, -created]` | |
| **Message** | `user` (FK→User, CASCADE), `room` (FK→Room, CASCADE), `body` (TextField), `updated`, `created` | Ordered by `[-updated, -created]` | |

## URL Patterns (`base/urls.py`)
| URL | View | Name | Auth |
|-----|------|------|------|
| `/login/` | `loginPage` | `login` | No |
| `/logout/` | `logoutUser` | `logout` | No |
| `/register/` | `registerPage` | `register` | No |
| `/` | `home` | `home` | No |
| `/room/<pk>/` | `room` | `room` | No (POST redirects if unauthenticated) |
| `/profile/<pk>/` | `userProfile` | `user-profile` | No |
| `/create-room/` | `createRoom` | `create-room` | `@login_required` |
| `/update-room/<pk>/` | `updateRoom` | `update-room` | `@login_required` + host check |
| `/delete-room/<pk>/` | `deleteRoom` | `delete-room` | `@login_required` + host check |
| `/delete-message/<pk>/` | `deleteMessage` | `delete-message` | `@login_required` + owner check |
| `/update-user/` | `updateUser` | `update-user` | `@login_required` |
| `/topics/` | `topicsPage` | `topics` | No |
| `/forgot-password/` | `forgotPassword` | `forgot-password` | No |
| `/reset/<uidb64>/<token>/` | `resetPassword` | `reset-password` | No |

## View Logic (`base/views.py`)
- **loginPage**: GET renders form, POST authenticates. Redirects if already logged in.
- **registerPage**: Uses `UserCreationForm`. Saves with lowercase username, auto-login.
- **home**: Search via `?q=` param filters rooms by topic/name/description (icontains). Topics limited to 5.
- **room**: GET shows room with messages + participants. POST with auth check creates message, adds user to participants.
- **userProfile**: Uses `get_object_or_404(User, pk=pk)` → Profile via `get_or_create`.
- **createRoom**: Creates topic via `get_or_create`, then Room with host=request.user.
- **updateRoom**: Uses `get_object_or_404(Room)`, host check via `HttpResponseForbidden`.
- **deleteRoom / deleteMessage**: `get_object_or_404` + owner check via `HttpResponseForbidden`.
- **updateUser**: Dual-form: `UserForm` (username, email) + `ProfileForm` (avatar, bio).
- **forgotPassword**: Token generation via `default_token_generator`, email via `send_mail` (if `EMAIL_HOST_USER` set). Always shows same success message (security: don't reveal if email exists).
- **resetPassword**: Validates token via `default_token_generator.check_token`, sets new password, validates min 8 chars + match.

## Template Files - Current State
### Active Templates (all redesigned):
| Template | View(s) | Key Features |
|----------|---------|--------------|
| `main.html` | Global | Inter + Material Symbols fonts, toast system (color-coded, auto-dismiss), semantic `<main>`, meta description, fixed favicon |
| `navbar.html` | Global | Fixed glass header, backdrop-filter blur, avatar with initials fallback, dropdown menu, Sign In pill button, mobile search toggle |
| `base/home.html` | home | 3-column grid, hero for unauthenticated, gradient CTA buttons, empty state with icon + "Create Room" CTA, room count gradient badge, stagger animations |
| `base/room.html` | room | 3-column layout (280px info sidebar, flex chat, 300px participants), chat bubbles (own=indigo solid right, others=glass left), avatar rings with status dots, typing indicator, scroll-to-bottom FAB, gradient participant borders, send button, WebSocket JS (auto-reconnect, typing broadcast, escape HTML) |
| `base/profile.html` | userProfile | Mobile-first centered, gradient-ring avatar, stats grid (Rooms/Messages/Member Since), "Currently Learning" horizontal scroll with progress bars, Recent Activity + Your Rooms sections |
| `base/login_register.html` | loginPage/registerPage | 2-column split (branding left, form right), glass feature cards, password toggle, remember me checkbox, Google social button (UI only), password strength bar (register), social proof avatars, collapse to single column ≤1100px |
| `base/update-user.html` | updateUser | Glass profile summary, grouped glass card sections (Account + About), photo upload hidden input, inline username/email editing, bio textarea, gradient save + error-color logout |
| `base/forgot_password.html` | forgotPassword | Centered glass card with gradient top border, email input with mail icon, "Send Reset Link" button |
| `base/reset_password.html` | resetPassword | Same card style, password1 + password2 fields with icons, minlength validation |
| `base/room_form.html` | createRoom/updateRoom | Topic datalist + suggestion chips, character counter on description, focus glow, gradient headers |
| `base/delete.html` | deleteRoom/deleteMessage | Warning icon, danger badge ("Room"/"Message"), shake animation on hover, object name display |
| `base/topics.html` | topicsPage | Search input, room count badges, stagger animation on topic cards |
| `base/feed_component.html` | Included by home/profile | Glass cards with backdrop blur, hover lift, participant avatar stack (+N more), gradient topic pills, online dot on host avatar, 2-line description truncation |
| `base/activity_component.html` | Included by home/profile | Gradient-left border, gradient ring avatars, hover-to-reveal delete, 3-line body truncation, empty state |
| `base/topics_component.html` | Included by home/profile | SVG icons per topic, active highlight with left accent, room count badges, "More" link to full topics page |

### Stale/Unused Templates (safe to delete):
| Template | Notes |
|----------|-------|
| `base/home_old.html` | Pre-redesign layout |
| `base/room_old.html` | Pre-redesign layout |
| `base/login_register_old.html` | Pre-redesign layout |
| `base/room_form_old.html` | Pre-redesign layout |
| `base/profile_old.html` | Pre-redesign layout |
| `base/delete_old.html` | Pre-redesign layout |
| `base/activity.html` | Hardcoded demo data, no view renders it |
| `login.html` | Standalone with anime.js, no view renders it |

### New Templates (this session):
| Template | Purpose |
|----------|---------|
| `base/forgot_password.html` | Email input for password reset |
| `base/reset_password.html` | New password form with validation |
| `base/password_reset_email.html` | Plain-text email template for reset link |

## CSS Design System (`static/styles/style.css` - 3574 lines)
### Architecture:
- **`:root` custom properties**: `--primary: #6366f1`, `--bg: #131317`, `--glass-bg: rgba(63,65,86,0.4)`, `--text: #e4e1e7`, etc.
- **Animations**: `fadeIn`, `fadeInUp`, `slideDown`, `pulse`, `typingDot`, `shimmer`, `toastIn`, `toastOut`, `shake`
- **Skeleton loading**: `.skeleton--text/title/avatar/card` with shimmer animation
- **Key sections**:
  - Base reset + typography + layout grid
  - Header/navbar + dropdown animation
  - Hero section (logged-out CTA)
  - Topic sidebar + activity panel (sticky, scrollable)
  - Room cards (glass, hover lift, participant stack)
  - Activity feed (gradient left border, ring avatars)
  - Empty states + forms + password controls
  - Auth (2-column split with glow orbs, glass cards, gradient borders)
  - Room chat (3-column flex layout, bubble system, typing, FAB)
  - Participants panel (scrollable, gradient rings, host star)
  - Profile (mobile-first, gradient avatar ring, stats grid, learning scroll)
  - Settings (glass card groups, inline editing)
  - Forgot/reset password (glass card, gradient top border)
  - Delete (warning icon, danger badge, shake)
  - Toast notifications (positioned top-right, slide in/out, color-coded)
  - Global scrollbar styling
  - **Responsive**: `≤1100px` (hide sidebars, auth collapses), `≤768px` (compact padding/hero/chat), `≤500px` (stack layout)

### CSS Gaps:
- No `prefers-reduced-motion` media query
- No `focus-visible` outline styles
- `scroll-behavior: smooth` missing from `html`
- No `@media (hover: hover)` optimization
- `font-display: swap` missing from Inter `@import`

## JavaScript (`static/js/script.js` - 270 lines)
### Behaviors implemented:
- User dropdown toggle with click-outside close
- Avatar upload preview (hidden file input → img preview)
- Toast notification auto-dismiss (4s) + close button
- Scroll-to-bottom button (appears when scrolled up 200px)
- Form submission loading states (disable btn, show spinner)
- Password show/hide toggle
- Password strength indicator (weak/medium/strong with labels)
- Mobile search toggle (clone + inline search bar)
- Character counter on textarea with `maxlength` (warn at 90%, error at 100%)
- Press-down effect on room cards/topic links
- IntersectionObserver for stagger animations
- Topic chip selection (click chip fills input)

### JS Gaps:
- No `prefers-reduced-motion` check to skip animations
- No WebSocket message delete handler (delete button in room.html sends HTTP GET to `/delete-message/<id>/` not WS)
- No smooth accordion for mobile menu items
- Toast `showToast()` function defined but not wired to form errors
- `password-wrapper` class referenced in password toggle JS but template uses `.input-icon-wrap` instead (toggle code path dead)

## WebSocket Architecture
- **Routing**: `ws/chat/<room_id>/` → `ChatConsumer`
- **Protocol**: JSON messages with `type` field
- **Events**: `message` (persist + broadcast), `typing` (broadcast start/stop)
- **Client**: room.html has inline JS that connects WebSocket, handles auto-reconnect (3s), fallback to HTTP POST if WS fails
- **Auth**: Rejects unauthenticated connections (close code 4000), invalid room ID (4004)
- **Test coverage**: 9 consumer tests (connect, disconnect, auth, message send/receive, typing, multi-client, avatar)

## Test Suite (`base/tests.py` - 43 tests)
| Test Group | Count | Covers |
|-----------|-------|--------|
| ModelTests | 7 | Topic/Room/Message creation, ordering, Profile auto-creation, bio update |
| ViewTests | 22 | All page GETs, POSTs, auth gates, 404s, search, profile stats/bio, forgot/reset password |
| WebSocketConsumerTests | 14 | Connect auth, room validation, message send/receive, typing, multi-client, disconnect, avatar |

## Security
- CSRF protection enabled
- Password hashing via PBKDF2
- Template auto-escaping prevents XSS
- Room/message ownership checks with `HttpResponseForbidden` (403)
- `get_object_or_404` on all single-object lookups
- Password reset token via Django's `default_token_generator`
- No email enumeration in forgot password (always shows same success message)

---

# COMPLETED: Full Design Redesign (Sessions 1-3)

## What Was Built
### Pages (all redesigned from Stitch AI designs):
1. **Home Page (Desktop)** — 3-column grid, glass navbar, hero for unauthenticated, glass room cards with stagger animations, glass activity feed with indigo borders, glass topic sidebar
2. **Room Chat (Desktop)** — 3-column layout, chat bubble system (own=indigo right, others=glass left), typing indicator, scroll-to-bottom FAB, avatar rings with status dots, WebSocket with auto-reconnect
3. **Login/Register** — 2-column split, brand features left (glass cards, social proof), form right (gradient border on register), password toggle, strength bar, Google button (UI only), collapse to single column ≤1100px
4. **User Profile (Mobile)** — mobile-first centered, gradient-ring avatar, stats grid, "Currently Learning" horizontal scroll with progress bars
5. **Settings (Mobile)** — glass card sections, inline editing, avatar upload, bio textarea, gradient save + error-color logout
6. **Forgot Password** — glass card with gradient top border, sends reset token email (if backend configured)
7. **Reset Password** — password form with match + length validation

### Backend Fixes:
- `get_object_or_404` on all single-object lookups (was raw `.get()`)
- `HttpResponseForbidden` (403) instead of plain `HttpResponse`
- Auth guard on room POST handler
- Full password reset flow with token generation and validation
- 4 new tests (43 total)
- No pending migrations

### CSS & JS:
- CSS grew from 1165 → 3574 lines (complete glassmorphism system)
- JS grew from basic dropdown to 270 lines (11 behaviors)
- Toast notification system replacing bare `<ul>` messages

---

# YET TO BE IMPLEMENTED

## 🔴 Critical (Must Fix)

### 1. Email Backend Configuration
**Problem**: `forgotPassword` view generates valid reset tokens but `send_mail()` is gated behind `if settings.EMAIL_HOST_USER:` which is never set.
**Fix**: Add to `settings.py`:
```python
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'noreply@studybud.app')
```
**Alternatively**: Set to console backend for dev so emails print to terminal instead of failing silently.

### 2. WebSocket Message Delete
**Problem**: Delete buttons on chat messages (room.html:79-82) send HTTP GET to `/delete-message/<id>/` (reloads page). Should use WebSocket to delete in real-time.
**Files affected**: `consumers.py`, `room.html` (inline JS), `views.py` (deleteMessage)
**Requires**: New WS event type `delete_message`, confirmation UX (undo snackbar?), server-side ownership check, broadcast delete event to group.

### 3. Cached `prefers-reduced-motion` Support (CSS)
**Missing from `style.css`**:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 4. `focus-visible` Outline Styles
**Missing from `style.css`**: Keyboard users get no visible focus indicators.
```css
:focus-visible {
  outline: 2px solid var(--primary-light);
  outline-offset: 2px;
}
```

### 5. `scroll-behavior: smooth` on `<html>`
**Missing from `style.css`**: Add to base reset.

### 6. `font-display: swap` on Google Fonts
**Missing from `style.css:1`**: Inter `@import` should include `&display=swap`.

## 🟡 Medium Priority

### 7. Password Toggle JS Dead Code
**Problem**: `script.js:125` targets `.password-wrapper` but templates use `.input-icon-wrap` with `.input-toggle`. The JS never finds targets and silently fails. Toggle works via the Material Symbols icon button in the template (which has its own inline toggle), but the script.js code path is dead.
**Fix**: Either update selector to `.input-icon-wrap .input-toggle` or remove dead code.

### 8. Form Validation Error Display
**Problem**: `login_register.html` and `room_form.html` lack inline error displays. Django form errors (`{{ form.errors }}`) are not rendered. Only `messages.error()` shows at top via toast.
**Fix**: Add `{% if field.errors %}...{% endif %}` blocks with `.error` class styling (CSS class `.error` and `.error-message` already exist at lines 1526-1537).

### 9. Remember Me Checkbox (Backend)
**Problem**: `login_register.html:128-131` has "Remember me" checkbox but `views.py:loginPage` never checks it. Login session expiry uses default (browser session).
**Fix**: Add `request.POST.get('remember')` check and set `request.session.set_expiry(2592000)` (30 days) if checked.

### 10. `forgotPassword` Doesn't Validate Email Format
**Problem**: No email field validation on server side (`views.py:206-226`). Could be extended to handle invalid email formats gracefully (currently just silently passes).

### 11. Password Strength Bar on Register Form
**Problem**: Template has strength bar markup (lines 177-184) and JS handles it (`script.js:139-175`), but the selector `#id_password1` may not match Django's auto-generated field IDs (could be `id_password1`, `id_new_password1`, etc.). Test with actual rendering.

## 🟢 Low Priority / Polish

### 12. My Learning Feature
Requires new model (e.g., `Enrollment` or repurpose `Topic` subscriptions), new view, new template. Fully deferred.

### 13. Stale Template Cleanup
Safe to delete: `home_old.html`, `room_old.html`, `login_register_old.html`, `room_form_old.html`, `profile_old.html`, `delete_old.html`, `activity.html`, `login.html`, `login.js`, `main.css`.

### 14. Active Nav Indicator
**Problem**: `navbar.html` has no visual indicator for current page. Should add `class="active"` to nav links based on `request.resolver_match.view_name`.

### 15. Avatar Upload Bug
**Problem**: Settings page (`update-user.html:37` and `profile_form.avatar`) uses hidden file input with label "Change" but the avatar is stored as `ImageField` — needs `enctype="multipart/form-data"` (already present) and proper file handling in view (already done). However, `MEDIA_ROOT` directory may not exist on fresh clone — `mkdir -p studybud/media/avatars/` needed.

### 16. Hero Section on Mobile
**Problem**: Hero (home.html:12-26) is hidden for authenticated users. For unauthenticated on mobile, the hero + Create Room button + feed header can be cramped. Verify responsive at 375px.

### 17. CSS Animation Performance
**Problem**: Some CSS uses `transition: all` instead of specific properties. Line 1130 uses `transition: all 0.3s cubic-bezier(...)`. Should be `transition: transform var(--normal) cubic-bezier(..), box-shadow var(--normal) cubic-bezier(...), border-color var(--normal)`.

### 18. Google Social Login (Backend)
**Problem**: Login/register has Google button (UI only). Would need `django-allauth` or `social-auth-app-django` for actual OAuth.

### 19. `re_path` in Routing
**Problem**: `routing.py:11` uses `re_path` without `^`/`$` anchors for WebSocket URL. Works because `URLRouter` matches prefix, but should use `^ws/chat/(?P<room_id>\d+)/$` for strict matching.

### 20. Topics Page Search Counter Bug
**Problem**: `topics.html:27` shows `{{topics.count}} topics` but this reflects the *filtered* count (after search `?q=`), not total topics. The "All Topics" link at line 29 also shows filtered count twice. Should separate total vs filtered count in the view.

## Verification for Future Sessions
Before marking any item complete:
1. Run `python manage.py test base` — must pass all 43 tests
2. Run `python manage.py makemigrations --check` — no pending migrations
3. Check that no stale templates are referenced by any active view
4. Verify the file wasn't modified in unexpected ways via `git diff --stat`

## Decision Records
- **Color palette**: `--bg: #131317`, `--primary: #6366f1`, `--tertiary: #7ed2ea`, `--text: #e4e1e7`
- **Font stack**: Inter (Google Fonts) for body, Material Symbols for icons
- **Animation approach**: CSS `@keyframes` + stagger classes rather than JS animation libraries
- **Navbar**: Fixed (not sticky), backdrop-filter glass effect
- **Auth collapse**: 1100px breakpoint hides brand column, shows single-column form
- **Password reset**: Custom implementation (not Django `PasswordResetView`) to match glass design, but uses Django's `default_token_generator` for token security
- **Stitch MCP**: Accessible at `stitch.googleapis.com/mcp` with API key. `stitch-and-ai.graphyte.ai` is defunct.
- **10 Stitch screen HTMLs** saved at `C:\Users\ADMIN\AppData\Local\Temp\opencode\stitch-*.html`

## File Change History
### Session 1 (CSS + Home/Room redesign):
- `style.css`: 1165 → 3574 lines
- `script.js`: Extended with 8 new behaviors
- `main.html`: Toast system, meta tags, fixed favicon
- `navbar.html`: Glass header, initials fallback, mobile search toggle
- `home.html`: Hero, empty state, gradient badges, stagger animations
- `room.html`: 3-column chat, WebSocket inline JS, bubble system, typing, FAB
- `feed_component.html`: Glass cards, participant stack, hover lift
- `activity_component.html`: Gradient border, ring avatars, truncation
- `topics_component.html`: SVG icons, active highlight, badges

### Session 2 (Auth + Profile + Settings + Forgot redesign):
- `login_register.html`: 2-column split, password features, social proof, responsive
- `profile.html`: Mobile-first, stats grid, learning scroll
- `update-user.html`: Glass card groups, inline editing, avatar upload
- `forgot_password.html`: New template, gradient border card
- `password_reset_email.html`: New template
- `reset_password.html`: New template
- `views.py`: Added `forgotPassword`, `resetPassword` views
- `urls.py`: Added `/forgot-password/`, `/reset/<uidb64>/<token>/` routes
- `tests.py`: +4 tests (43 total)

### Session 3 (Backend audit + hardening):
- `views.py`: `get_object_or_404` everywhere, `HttpResponseForbidden`, auth guard on room POST
- `AGENTS.md`: Complete rewrite with current state + remaining items
