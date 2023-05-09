from django.urls import path

from .apps import AppConfig
from .views import (
    HomePageView,
    ProductListView,
    ContactsView,
    SuccessFeedbackView
)

app_name = AppConfig.__name__

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/success-feedback', SuccessFeedbackView.as_view(), name='success_feedback')
]
