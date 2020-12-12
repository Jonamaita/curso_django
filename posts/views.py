"""
Posts Views
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# Models
from posts.models import Post

# Forms
from posts.forms import PostForm

# Create your views here.


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts."""

    # Enviamos em template
    template_name = 'posts/feed.html'
    # El modelo que listaremos
    model = Post
    # El orden
    ordering = ('-created',)
    # Paginamos
    paginate_by = 2
    # Enviamos el objeto al html como posts
    context_object_name = 'posts'


@login_required
def create_post(request):
    """Create new post view."""

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.profile = request.user.profile
            form.save()
            return redirect('posts:feed')

    else:
        form = PostForm()

    return render(
        request=request,
        template_name='posts/new.html',
        context={
            'form': form,
            'user': request.user,
            'profile': request.user.profile
        }
    )
