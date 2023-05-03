from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import FeedbackForm
from .models import Product, Category
from .services import FeedbackServices


class HomePageView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        categories = Category.get_all_categories()
        products = Product.get_last_products(count=4)
        context = {
            'categories': categories,
            'products': products
        }
        return render(request=request, template_name='app_catalog/home.html', context=context)


class ContactsView(FormView):
    form_class = FeedbackForm
    template_name = 'app_catalog/contacts.html'
    success_url = reverse_lazy('app_catalog:success_feedback')

    def form_valid(self, form) -> HttpResponseRedirect:
        name = form.cleaned_data.get('name')
        phone = form.cleaned_data.get('phone')
        message = form.cleaned_data.get('message')

        FeedbackServices.save_feedback(name=name, phone=phone, message=message)
        self.request.session['form_submitted'] = True
        return super().form_valid(form)


class SuccessFeedbackView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse | HttpResponseRedirect:
        if request.session.get('form_submitted'):
            del request.session['form_submitted']
            return render(request=request, template_name='app_catalog/success_feedback.html')
        return redirect('app_catalog:contacts')
