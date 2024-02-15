from django.contrib import admin
from products.models import Category, SubCategory, Product


# Register your models here.

# admin.site.register(Category)


@admin.register(Category)
class Category_admin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ['name', ]}


@admin.register(SubCategory)
class Subcategory_admin(admin.ModelAdmin):
    list_display = ('name', 'category_id',)
    search_fields = ('name', 'category_id',)
    ordering = ('name', 'category_id',)
    prepopulated_fields = {'slug': ['name', ]}


@admin.register(Product)
class Product_admin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'subcategory', 'rating', 'review')
    prepopulated_fields = {'slug': ['name', ]}
