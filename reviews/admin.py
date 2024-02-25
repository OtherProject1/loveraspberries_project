from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'date']
    list_display_links = ['product', 'user', 'rating', 'date']