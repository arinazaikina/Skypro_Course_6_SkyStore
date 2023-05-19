from django.contrib import admin

from .models import Client, Newsletter, Message, NewsletterLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    list_display_links = ['email']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['pk', 'time', 'frequency', 'status', 'created_at']

    class Media:
        js = ('js/select_all.js',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject']


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'status']
