
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.views.generic import ListView


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.order_by("-created_at")
        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm()
        return context


cclass PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tags_str = form.cleaned_data.get("tags", "")
        self._save_tags(tags_str, self.object)
        return response

    def _save_tags(self, tags_str, post):
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        tag_objs = []
        for name in tags:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["tags"] = ", ".join(self.object.tags.values_list("name", flat=True))
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tags_str = form.cleaned_data.get("tags", "")
        self._save_tags(tags_str, self.object)
        return response

    def _save_tags(self, tags_str, post):
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        tag_objs = []
        for name in tags:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    ...

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("post-detail", pk=post.id)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs["post_id"]})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()


class TagPostListView(ListView):
    model = Post
    template_name = "blog/tag_post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs["tag_name"]
        return Post.objects.filter(tags__name=tag_name).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_name"] = self.kwargs["tag_name"]
        return context
