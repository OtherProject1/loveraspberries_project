from django.shortcuts import render

def home(request):
    return render(request, 'products/base.html')

def favorities_products(request):
    context = {}
    return render(request, 'products/favorites_products.html', context=context)