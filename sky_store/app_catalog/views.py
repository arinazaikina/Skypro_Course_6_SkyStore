from typing import Dict, Any

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from permissions.authenticate import AuthenticatedAccessMixin
from permissions.user_permission import CreatorAccessMixin, ModeratorOrCreatorMixin, ModeratorAccessMixin
from .forms import FeedbackForm, ProductForm, ProductVersionFormSet
from .models import Product, Category, CompanyContact
from .services import FeedbackServices, get_all_categories


class HomePageView(TemplateView):
    template_name = 'app_catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_all_categories()
        context['products'] = Product.get_last_products(count=4)
        return context


class ProductListView(ListView):
    """
    Представление для списка товаров.
    Настроена пагинация.
    На одной странице отображается 4 товара.
    """
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Product]:
        """
        Получает и возвращает queryset опубликованных товаров в зависимости
        от выбранной категории или всех опубликованных товаров.
        """
        category_id = self.request.GET.get('category', None)

        if category_id:
            queryset = Product.get_published_products_by_category(category_id=category_id)
        else:
            queryset = Product.get_all_published_products()

        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Возвращает контекст данных для шаблона списка товаров,
        включая категории и текущую выбранную категорию.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        context['categories'] = get_all_categories()
        if category_id:
            context['category'] = Category.get_category_by_id(category_id=category_id)
        else:
            context['category'] = 'Все'

        return context


class ProductDetailView(DetailView):
    """
    Представление для отображения деталей товара.
    """
    model = Product
    context_object_name = 'product'


class ProductCreateView(AuthenticatedAccessMixin, CreateView):
    """
    Представление для создания нового товара.
    """
    model = Product
    form_class = ProductForm

    def form_valid(self, form: ProductForm) -> HttpResponseRedirect:
        """
        Обрабатывает форму, если она валидна,
        сохраняет товар и перенаправляет на страницу деталей товара.
        """
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.save()

        messages.success(self.request, 'Товар успешно добавлен')
        return HttpResponseRedirect(reverse('app_catalog:product_detail', args=[product.id]))

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Получает и возвращает контекст данных для шаблона создания товара,
        включая информацию о действии.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создать'
        return context


class ProductUpdateView(ModeratorOrCreatorMixin, UpdateView):
    """
    Представление для редактирования существующего товара.
    """
    model = Product

    def form_valid(self, form: ProductForm) -> HttpResponseRedirect:
        """
        Обрабатывает форму, если она валидна, сохраняет товар и версии товара и
        перенаправляет на страницу редактирования товара.
        """
        product = form.save()
        context = self.get_context_data()
        versions = context.get('versions')

        if versions:
            if versions.is_valid():
                versions.instance = product
                versions.save()
            else:
                error_message = versions.non_form_errors()
                messages.error(self.request, error_message)
                return self.form_invalid(form)

        messages.success(self.request, 'Товар обновлён')
        return HttpResponseRedirect(reverse('app_catalog:update_product', args=[product.id]))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Возвращает контекст данных для шаблона редактирования товара,
        включая формсет версий и информацию о действии.
        """
        context = super().get_context_data(**kwargs)
        context['versions'] = self.get_versions_formset()
        context['action'] = 'Редактировать'
        return context

    def get_versions_formset(self) -> ProductVersionFormSet:
        """
        Возвращает экземпляр формсета версий товара.
        """
        if self.request.user.groups.filter(name='Модераторы').exists():
            return None
        elif self.request.POST:
            return ProductVersionFormSet(self.request.POST, instance=self.object)
        else:
            return ProductVersionFormSet(instance=self.object)


class ProductDeleteView(CreatorAccessMixin, DeleteView):
    """
    Представление для удаления существующего товара.
    """
    model = Product
    success_url = reverse_lazy('app_catalog:product_list')

    def delete(self, request, *args, **kwargs):
        """
        Удаляет товар и перенаправляет на страницу списка товаров.
        """
        self.object = self.get_object()

        message = f'Товар "{self.object.title}" удалён'
        messages.success(request, message)

        return HttpResponseRedirect(self.get_success_url())


class UserProductListView(AuthenticatedAccessMixin, ListView):
    """
    Представление для списка товаров, созданных аутентифицированным пользователем.
    Настроена пагинация.
    На одной странице отображается 4 товара.
    """
    template_name = 'app_catalog/products.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Product]:
        """
        Получает и возвращает queryset товаров, созданных текущим пользователем.
        """
        return Product.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Получает и возвращает контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['header'] = 'Созданные мной товары'
        return context


class UnpublishedProductListView(ModeratorAccessMixin, ListView):
    """
    Представление для списка неопубликованных товаров.
    Настроена пагинация.
    На одной странице отображается 4 товара.
    """
    template_name = 'app_catalog/products.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Product]:
        """
        Получает и возвращает queryset неопубликованных товаров.
        """
        return Product.get_unpublished_products()

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Получает и возвращает контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['header'] = 'Неопубликованные товары'
        return context


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
