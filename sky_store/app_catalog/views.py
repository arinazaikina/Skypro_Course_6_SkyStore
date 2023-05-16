from django.contrib import messages
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView, ListView, DetailView

from .forms import FeedbackForm, ProductForm
from .models import Product, Category, CompanyContact
from .services import FeedbackServices


class HomePageView(TemplateView):
    template_name = 'app_catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.get_all_categories()
        context['products'] = Product.get_last_products(count=4)
        return context


class ProductListView(ListView):
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        if category_id:
            return Product.get_products_by_category(category_id=category_id)
        return Product.get_all_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        context['categories'] = Category.get_all_categories()
        if category_id:
            context['category'] = Category.get_category_by_id(category_id=category_id)
        else:
            context['category'] = 'Все'

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class CreateProduct(FormView):
    form_class = ProductForm
    template_name = 'app_catalog/create_product.html'

    def form_valid(self, form) -> HttpResponseRedirect:
        image = form.cleaned_data['image'] if form.cleaned_data['image'] else None
        product = Product.create_product(
            name=form.cleaned_data.get('name'),
            description=form.cleaned_data.get('description'),
            image=image,
            category=form.cleaned_data.get('category'),
            price=form.cleaned_data.get('price')
        )

        messages.success(self.request, 'Товар успешно добавлен')
        return HttpResponseRedirect(reverse('app_catalog:product_detail', args=[product.id]))


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = CompanyContact.get_company_contacts(count=1)
        context['contacts'] = contacts
        return context


class SuccessFeedbackView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse | HttpResponseRedirect:
        if request.session.get('form_submitted'):
            del request.session['form_submitted']
            return render(request=request, template_name='app_catalog/success_feedback.html')
        return redirect('app_catalog:contacts')
