from django.urls import path

from .apps import AppConfig
from .views import (
    HomePageView,
    ProductListView,
    ProductDetailView,
    CreateProduct,
    ContactsView,
    SuccessFeedbackView
)

app_name = AppConfig.__name__

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', CreateProduct.as_view(), name='create_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/success-feedback', SuccessFeedbackView.as_view(), name='success_feedback')
]
