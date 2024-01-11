from django.shortcuts import render
from products.categories_list import first_categories


def home(request):
    context = {'categories': first_categories}
    return render(request, 'products/base.html', context)


def favorities_products(request):
    context = {}
    return render(request, 'products/favorites_products.html', context=context)
