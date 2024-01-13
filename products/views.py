from django.shortcuts import render
from products.categories_list import first_categories, navbar_list

context = {'categories': first_categories, 'navbar': navbar_list}
def home(request):
    return render(request, 'products/base.html', context)
