from django.contrib import admin
from products.models import Category, SubCategory


# Register your models here.

# admin.site.register(Category)


@admin.register(Category)
class Category_admin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SubCategory)
class Subcategory_admin(admin.ModelAdmin):
    list_display = ('name', 'category_id',)
    search_fields = ('name', 'category_id',)
    ordering = ('name', 'category_id',)
