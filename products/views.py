from django.shortcuts import render

def home(request):
    return render(request, 'products/base.html')

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