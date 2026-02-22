## Follow System
- `POST /api/accounts/follow/<user_id>/` → Follow a user
- `POST /api/accounts/unfollow/<user_id>/` → Unfollow a user

## Feed
- `GET /api/feed/` → Get posts from followed users (ordered by newest first)

## Likes
- `POST /api/posts/<id>/like/` → Like a post
- `POST /api/posts/<id>/unlike/` → Unlike a post

## Notifications
- `GET /api/notifications/` → View notifications (latest first)
