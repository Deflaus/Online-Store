from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ] # Поля, отображаемые на странице списка объектов
    prepopulated_fields = {
        'slug': ('name',)
    } # Определение slug, основываясь на названии категории


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated',
    ] # Поля, отображаемые на странице списка объектов
    list_filter = [
        'available',
        'created',
        'updated',
    ] # Фильтр данных
    list_editable = [
        'price',
        'available',
    ] # Поля, которые можно будет редактировать на странице списка объектов
    prepopulated_fields = {
        'slug': ('name',)
    } # Определение slug, основываясь на названии товара
