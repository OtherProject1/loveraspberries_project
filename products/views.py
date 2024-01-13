from django.shortcuts import render
from products.categories_list import first_categories, navbar_list, footer_list

context = {'categories': first_categories, 'navbar': navbar_list, 'footer': footer_list}
def home(request):
    return render(request, 'products/base.html', context)

def favourites_products(request):
    return render(request, 'products/favourites_products.html', context)