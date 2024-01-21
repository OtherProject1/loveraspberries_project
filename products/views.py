from django.shortcuts import render, redirect
from products.categories_list import first_categories, navbar_list, footer_list, cards, payment_list, favourite_cards, shopping_cards

context = {'title': 'LoveRaspberry', 'categories': first_categories, 'navbar': navbar_list, 'footer': footer_list,
           'logo': payment_list}


def home(request):
    context['cards'] = cards
    context['title'] = 'LoveRaspberry'
    return render(request, 'products/main.html', context)


def favourites_products(request):
    context['favorites_products'] = favourite_cards
    context['title'] = 'Избранное'
    return render(request, 'products/favourites_products.html', context)


def profile(request):
    context['is_auth'] = True
    context['title'] = 'Профиль'
    return render(request, 'products/profile.html', context)


def shopping_cart(request):
    context['title'] = 'Корзина'
    context['is_auth'] = True
    context['shopping_cards'] = shopping_cards
    return render(request, 'products/shopping_cart.html', context)


def delivery(request):
    context['is_auth'] = True
    context['title'] = 'Доставки'
    return render(request, 'products/delivery.html', context)


def payment_methods(request):
    return render(request, 'products/payment_methods.html', context)


def item_return(request):
    return render(request, 'products/item_return.html', context)


def sale_rules(request):
    return render(request, 'products/sale_rules.html.', context)


def delivery_rules(request):
    return render(request, 'products/delivery_rules.html', context)


def terms_rules(request):
    return render(request, 'products/terms.html', context)


def money_return(request):
    return render(request, 'products/money_return.html', context)


def policy(request):
    return render(request, 'products/policy.html', context)

def sale_on_market(request):
    return redirect("https://seller-auth.wildberries.ru/ru/?redirect_url=https://seller.wildberries.ru/")