from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import ClientCreateForm, NewsletterCreateForm
from .models import Client, Newsletter, NewsletterLog
from .services import NewsletterDeliveryService


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создать'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Клиент успешно создан')
        return response


class ClientListView(ListView):
    model = Client
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by('first_name')
        return queryset


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Редактировать'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Данные клиента успешно отредактированы')
        return response


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('app_newsletter:client_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.make_inactive()

        message = f'Статус пользователя "{self.object}" изменён на неактивный'
        messages.success(request, message)

        return HttpResponseRedirect(self.get_success_url())


class NewsletterListView(ListView):
    model = Newsletter
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by('-created_at')
        return queryset


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создать'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object.status = 'C'
        self.object.save()

        delivery_service = NewsletterDeliveryService(self.object)
        delivery_service.create_task()

        self.object.status = 'S'
        self.object.save()

        messages.success(self.request, 'Рассылка успешно создана')
        return response


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Редактировать'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        delivery_service = NewsletterDeliveryService(self.object)
        delivery_service.delete_task()
        delivery_service.create_task()

        messages.success(self.request, 'Данные рассылки успешно отредактированы')
        return response


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('app_newsletter:newsletter_list')

    def form_valid(self, form):
        self.object = self.get_object()

        delivery_service = NewsletterDeliveryService(self.object)
        delivery_service.delete_task()

        message = f'Рассылка "{self.object}" была удалена'
        self.object.delete()

        messages.success(self.request, message)

        return HttpResponseRedirect(self.get_success_url())


class NewsletterLogListView(ListView):
    model = NewsletterLog
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-date_time')
        return queryset


class NewsletterLogDetailView(DetailView):
    model = NewsletterLog
