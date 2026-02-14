## Authentication System

- **Register**: `/register/` — create a new account (username, email, password).
- **Login**: `/login/` — authenticate existing users.
- **Logout**: `/logout/` — end session.
- **Profile**: `/profile/` — view and update email.

### Testing
1. Go to `/register/` and create a new user.
2. Log in at `/login/`.
3. Visit `/profile/` to view and update your email.
4. Logout at `/logout/`.

## Blog Post Management

- **List posts**: `/posts/`
- **View post**: `/posts/<id>/`
- **Create post**: `/posts/new/` (authenticated users only)
- **Edit post**: `/posts/<id>/edit/` (author only)
- **Delete post**: `/posts/<id>/delete/` (author only)

Permissions:
- Anyone can view posts.
- Only logged-in users can create posts.
- Only the author can edit or delete their own posts.


## Comment System

- Users can view comments on each post on the post detail page.
- Authenticated users can:
  - Add comments at `/posts/<post_id>/comments/new/`
  - Edit their own comments at `/comments/<id>/edit/`
  - Delete their own comments at `/comments/<id>/delete/`

Permissions:
- Only the comment author can edit or delete their comment.
- All visitors can read comments.
