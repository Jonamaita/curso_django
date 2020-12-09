from django.contrib import admin

from posts.models import Post

# Register your models here.


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    """
    Posts admin
    """

    list_display = ("user", "title", "photo")
    list_display_links = ("user",)

    list_editable = ("title", "photo")
