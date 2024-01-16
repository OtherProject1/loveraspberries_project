from django.shortcuts import render
from products.categories_list import first_categories, navbar_list, footer_list, cards, payment_list

context = {'categories': first_categories, 'navbar': navbar_list, 'footer': footer_list, 'logo': payment_list}


def home(request):
    context['cards'] = cards
    return render(request, 'products/main.html', context)


def favorities_products(request):
    return render(request, 'products/favourites_products.html', context)


def profile(request):
    context['is_auth'] = True
    return render(request, 'products/profile.html', context)


def shopping_cart(request):
    return render(request, 'products/shopping_cart.html', context)


def delivery(request):
    context['is_auth'] = True
    return render(request, 'products/delivery.html', context)


def favourites_products(request):
    return render(request, 'products/favourites_products.html', context)


def payment_methods(request):
    return render(request, 'products/payment_methods.html', context)
