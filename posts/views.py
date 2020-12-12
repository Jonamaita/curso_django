"""
Posts Views
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

# Forms
from posts.forms import PostForm
# Models
from posts.models import Post

# Create your views here.


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts."""

    # Enviamos em template
    template_name = "posts/feed.html"
    # El modelo que listaremos
    model = Post
    # El orden
    ordering = ("-created",)
    # Paginamos
    paginate_by = 30
    # Enviamos el objeto al html como posts
    context_object_name = "posts"


class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""

    template_name = "posts/detail.html"
    queryset = Post.objects.all()
    context_object_name = "post"


@login_required
def create_post(request):
    """Create new post view."""

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.profile = request.user.profile
            form.save()
            return redirect("posts:feed")

    else:
        form = PostForm()

    return render(
        request=request,
        template_name="posts/new.html",
        context={
            "form": form,
            "user": request.user,
            "profile": request.user.profile,
        },
    )
