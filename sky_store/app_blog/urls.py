from django.urls import path

from app_blog.apps import AppBlogConfig
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

app_name = AppBlogConfig.name

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
