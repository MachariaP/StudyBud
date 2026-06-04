# Feature #2: Avatar Upload + Rich Profiles

## Goal
Replace all hardcoded `randomuser.me` avatar URLs with real uploaded avatars + auto-generated initials fallback. Add bio field to user profiles. Display real stats (rooms hosted, messages sent, join date).

## Architecture
- **Profile model** (OneToOneField → User): `avatar` (ImageField), `bio` (TextField)
- **Signal**: Auto-create Profile on User creation (`post_save`)
- **Media**: `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`, `avatars/` upload dir
- **Form**: `UserForm` (username, email) + `ProfileForm` (avatar, bio) in same template
- **Avatar fallback**: Template inline — check `user.profile.avatar`, else render initials via CSS

## Files Changed
| File | Change |
|------|--------|
| `base/models.py` | Add `Profile` model |
| `base/forms.py` | Add `ProfileForm` |
| `base/views.py` | Update `updateUser` to handle ProfileForm + `request.FILES`; add `get_or_create` profile in `userProfile` |
| `base/urls.py` | No change needed |
| `studybud/settings.py` | Add `MEDIA_URL`, `MEDIA_ROOT` |
| `studybud/urls.py` | Add `+ static(settings.MEDIA_URL...)` for dev |
| `base/admin.py` | Register `Profile` |
| `base/templates/base/profile.html` | Use `user.profile.avatar.url` or initials; show bio |
| `base/templates/base/update-user.html` | Add avatar preview, bio textarea, file input |
| `templates/navbar.html` | Avatar fallback from `request.user.profile` |
| `base/templates/base/feed_component.html` | Avatar fallback from `room.host.profile` |
| `base/templates/base/activity_component.html` | Avatar fallback from `message.user.profile` |
| `base/templates/base/room.html` | Avatar fallbacks for host, messages, participants |
| `static/js/script.js` | Avatar preview on file select in update-user |
| `base/tests.py` | Test Profile model creation via signal, ProfileForm, avatar in views |

## Edge Cases
- **Existing users without Profile**: Auto-create on first access via `get_or_create` in `userProfile` view
- **No avatar uploaded**: Show initials (first letter of username, uppercase) with random-ish bg color
- **File too large**: Django `ImageField` validates; form handles validation errors
- **Invalid image upload**: Django `ImageField` rejects non-image files
- **Bio too long**: `TextField` has no limit by default, but form can add `maxlength` attribute
- **Anonymous users**: Profile is never accessed (already gated by `@login_required`)
- **Registration**: Signal auto-creates Profile when User is created via `UserCreationForm` + `login`

## Testing Strategy
1. **Profile model test**: Profile created via signal on User creation, fields default to blank
2. **Profile signal test**: Creating a User creates an associated Profile
3. **Profile view test**: `updateUser` saves avatar and bio correctly
4. **Profile page test**: Profile page shows bio and avatar
5. **Registration test**: New user gets auto-created Profile
6. **Existing users test**: Profile page still works for users without Profile (get_or_create)
