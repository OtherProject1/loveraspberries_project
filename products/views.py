from django.shortcuts import render
from products.categories_list import first_categories, navbar_list, footer_list

context = {'categories': first_categories, 'navbar': navbar_list, 'footer': footer_list}
def home(request):
    return render(request, 'products/base.html', context)

def favorities_products(request):
    context = {}
    return render(request, 'products/favorites_products.html', context=context)

def profile(request):
    context = {'is_auth': True}
    return render(request, 'products/profile.html', context)

def shopping_cart(request):
    context = {}
    return render(request, 'products/shopping_cart.html', context)

def delivery(request):
    context = {}
    return render(request, 'products/delivery.html', context)
def favourites_products(request):
    return render(request, 'products/favourites_products.html', context)
