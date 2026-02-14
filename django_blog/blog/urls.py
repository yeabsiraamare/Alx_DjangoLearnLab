from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    add_comment, CommentUpdateView, CommentDeleteView,
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    path("posts/<int:post_id>/comments/new/", add_comment, name="comment-add"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]
