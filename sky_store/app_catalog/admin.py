from django.contrib import admin

from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'phone']
    list_display_links = ['pk', 'name']
