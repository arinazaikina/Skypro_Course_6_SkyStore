from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from app_newsletter.forms import ClientCreateForm
from app_newsletter.models import Client


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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
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
