from django.contrib import admin
from products.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ['name', ]}


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id',)
    search_fields = ('name', 'category_id',)
    ordering = ('name', 'category_id',)
    prepopulated_fields = {'slug': ['name', ]}


class ProductImagesInline(admin.TabularInline):
    model = ProductImages

class ProductDetailsInline(admin.TabularInline):
    model = ProductDetail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'subcategory', )
    prepopulated_fields = {'slug': ['name', ]}
    inlines = [
        ProductImagesInline,
        ProductDetailsInline,
    ]


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )


@admin.register(CategoryDetails)
class CategoryDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    fields = ('product', 'image',)
