from django.contrib import admin

from app_blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'published', 'views_count']
    list_display_links = ['title']
