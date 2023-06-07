from django.urls import path

from .apps import AppNewsletterConfig
from .views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView,
    NewsletterListView,
    NewsletterDetailView,
    NewsletterCreateView,
    NewsletterUpdateView,
    NewsletterDeleteView,
    NewsletterLogListView,
    NewsletterLogDetailView
)

app_name = AppNewsletterConfig.name

urlpatterns = [
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/update/<int:pk>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter/delete/<int:pk>/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletterlogs/', NewsletterLogListView.as_view(), name='newsletter_log_list'),
    path('newsletterlogs/<int:pk>/', NewsletterLogDetailView.as_view(), name='newsletter_log_detail'),
]
