from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from slugify import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostCreateForm
from .models import Post


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.increment_view_count()
        return obj


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.save()
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
        post.slug = slugify(post.title)
        post.save()
        messages.success(request=self.request, message='Статья успешно отредактирована')
        return redirect(reverse('app_blog:post_detail', kwargs={'slug': post.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Редактировать'
        return context


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('app_blog:post_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.make_unpublished()

        message = f'Статус статьи "{self.object.title}" изменён на не опубликована'
        messages.success(request, message)

        return HttpResponseRedirect(self.get_success_url())
