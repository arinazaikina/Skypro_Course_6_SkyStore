from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import AppConfig
from .views import (
    HomePageView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ContactsView,
    SuccessFeedbackView,
    UserProductListView,
    UnpublishedProductListView
)

app_name = AppConfig.__name__

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('user/products/', UserProductListView.as_view(), name='user_products'),
    path('products/unpublished/', UnpublishedProductListView.as_view(), name='unpublished_products'),
    path('product/<int:pk>/', cache_page(60 * 2)(ProductDetailView.as_view()), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/success-feedback', SuccessFeedbackView.as_view(), name='success_feedback')
]
