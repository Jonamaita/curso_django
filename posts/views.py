"""
Posts Views
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Models
from posts.models import Post

# Forms
from posts.forms import PostForm


# Create your views here.

@login_required
def list_posts(request):  # pylint: disable = unused-argument
    """
    View to lists posts
    """
    posts = Post.objects.all().order_by('-created')

    return render(request, 'posts/feed.html', {'posts': posts})


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
