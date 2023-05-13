from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from app_blog.forms import PostCreateForm
from app_blog.models import Post


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        post = form.save()
        messages.success(request=self.request, message='Статья успешно создана')
        return redirect(reverse('app_blog:post_detail', kwargs={'slug': post.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создать'
        return context


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        post = form.save()
        messages.success(request=self.request, message='Статья успешно отредактирована')
        return redirect(reverse('app_blog:post_detail', kwargs={'slug': post.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Редактировать'
        return context

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('app_blog:post_list')