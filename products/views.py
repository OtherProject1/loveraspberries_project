from django.shortcuts import render
from products.categories_list import first_categories, navbar_list


def home(request):
    context = {'categories': first_categories, 'navbar': navbar_list}
    return render(request, 'products/base.html', context)