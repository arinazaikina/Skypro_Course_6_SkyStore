from django.contrib import admin

from .models import Feedback, Category, Product


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'phone']
    list_display_links = ['pk', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'price', 'category']
    list_display_links = ['pk', 'name']
    search_fields = ['name', 'description']
    list_filter = ['category']
