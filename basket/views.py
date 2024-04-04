from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from products.mixins import BaseMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from users.forms import UserLoginForm
from .models import Basket, Favorites
from products.models import Product
from django.db.models.aggregates import Sum
from django.db.models.expressions import F

'''
Твой вариант
'''


# @login_required()
# def add_product_to_basket(request, product_id):
#     '''пока делаю, что в корзину могут добавлять только авторизованные юзеры и при этом страница перезагружается'''
#     product = Product.objects.get(pk=product_id)
#     product_in_basket = Basket.objects.get_or_create(user=request.user, product=product)
#     if not product_in_basket[
#         1]:  # get_or_create возвращает кортеж, где второй параметр говорит, создан ли элемент (True) или найден (False)
#         product_in_basket[0].quantity += 1
#         product_in_basket[0].save()
#     return redirect('products:home')

# @login_required()
# def minus_product_to_basket(request, product_id):
#     '''пока делаю, что в корзину могут добавлять только авторизованные юзеры и при этом страница перезагружается'''
#     product = Product.objects.get(pk=product_id)
#     product_in_basket = Basket.objects.get_or_create(user=request.user, product=product)
#     if not product_in_basket[
#         1]:  # get_or_create возвращает кортеж, где второй параметр говорит, создан ли элемент (True) или найден (False)
#         product_in_basket[0].quantity -= 1
#         product_in_basket[0].save()
#         if product_in_basket[0].quantity == 0:
#             product_in_basket[0].delete()
#     return redirect('products:home')

# @login_required
# def add_product_to_favorites(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     product_in_favorites = Favorites.objects.get_or_create(user=request.user, product=product)
#     if not product_in_favorites[
#         1]:
#         product_in_favorites[0].delete()
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


class BasketView(BaseMixin, ListView):
    model = Basket
    template_name = 'basket/basket.html'
    context_object_name = 'basket_products'

    def get_queryset(self) -> QuerySet[Any]:
        return Basket.objects.filter(user=self.request.user).select_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'StuffStore - Корзина'
        context['basket_products_new'] = Basket.objects.filter(user=self.request.user)
        context['favorites_products'] = list(
            *list(zip(*Favorites.objects.filter(user=self.request.user).values_list('product'))))
        context['cost_selected_basket_products'] = context['basket_products'].filter(selected_for_purchase=1).aggregate(
            basket_cost=Sum(F('product__price') * F('quantity')), basket_count_products=Sum('quantity'))
        return context


'''
Попробую написать функцию добавления товара немного по другому
'''


@login_required
def ajax_add_product_to_basket(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.filter(user=request.user, product=product)
    response = {'success': True,
                'product_id': product_id, }
    # Если QuerySet пуст
    if not product_in_basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        response['basket_product_quantity'] = 1
    else:
        basket = product_in_basket.first()
        basket.quantity += 1
        basket.save()
        response['basket_product_quantity'] = basket.quantity
    basket = Basket.objects.filter(user=request.user)
    response['basket_counter'] = basket.count()
    response['add_product_to_basket'] = reverse('basket:ajax_add_product_to_basket', args=[product_id, ])
    response['minus_product_to_basket'] = reverse('basket:ajax_minus_product_to_basket', args=[product_id, ])
    response['total_basket_quantity_and_cost'] = basket.filter(selected_for_purchase=1).aggregate(
        basket_cost=Sum(F('product__price') * F('quantity')), basket_quantity=Sum('quantity'))
    response['product_sum'] = product_in_basket[0].sum()
    return JsonResponse(response)


@login_required
def ajax_minus_product_to_basket(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.filter(user=request.user, product=product)
    response = {'success': True,
                'product_id': product_id, }
    if product_in_basket.exists():
        basket = product_in_basket.last()
        basket.quantity -= 1
        basket.save()
        response['basket_product_quantity'] = basket.quantity
        response['product_sum'] = product_in_basket[0].sum()
        if product_in_basket[0].quantity == 0:
            basket.delete()
    basket = Basket.objects.filter(user=request.user)
    response['basket_counter'] = Basket.objects.filter(user=request.user).count()
    response['add_product_to_basket'] = reverse('basket:ajax_add_product_to_basket', args=[product_id, ])
    response['minus_product_to_basket'] = reverse('basket:ajax_minus_product_to_basket', args=[product_id, ])
    response['total_basket_quantity_and_cost'] = basket.filter(selected_for_purchase=1).aggregate(
        basket_cost=Sum(F('product__price') * F('quantity')), basket_quantity=Sum('quantity'))
    return JsonResponse(response)


@login_required()
def ajax_delete_product_from_basket(request, product_id):
    response = {'success': True,
                'product_id': product_id, }
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.filter(user=request.user, product=product)
    Basket.objects.get(pk=product_in_basket[0].pk).delete()
    basket = Basket.objects.filter(user=request.user)
    response['basket_counter'] = Basket.objects.filter(user=request.user).count()
    response['total_basket_quantity_and_cost'] = basket.filter(selected_for_purchase=1).aggregate(
        basket_cost=Sum(F('product__price') * F('quantity')), basket_quantity=Sum('quantity'))
    return JsonResponse(response)


@login_required
def ajax_add_product_to_favorites(request, product_id):
    response = {'success': True,
                'product_id': product_id, }
    product = Product.objects.get(pk=product_id)
    product_in_favorites = Favorites.objects.filter(user=request.user, product=product)
    if product_in_favorites.exists():
        product_in_favorites.last().delete()
        response['add_product'] = False
    else:
        Favorites.objects.create(user=request.user, product=product)
        response['add_product'] = True
    return JsonResponse(response)


@login_required
def add_product_to_basket(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.filter(user=request.user, product=product)
    # Если QuerySet пуст
    if not product_in_basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = product_in_basket.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def minus_product_to_basket(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.filter(user=request.user, product=product)
    if product_in_basket.exists():
        basket = product_in_basket.last()
        basket.quantity -= 1
        basket.save()
        if product_in_basket[0].quantity == 0:
            basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def delete_product_from_basket(request, basket_id):
    Basket.objects.get(pk=basket_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def selected_for_purchase(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.selected_for_purchase = not basket.selected_for_purchase
    basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_product_to_favorites(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_in_favorites = Favorites.objects.filter(user=request.user, product=product)
    if product_in_favorites.exists():
        product_in_favorites.last().delete()
    else:
        Favorites.objects.create(user=request.user, product=product)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_products(request):
    basket = Basket.objects.filter(user=request.user)
    context = {'title': 'StuffStore - Корзина', 'basket_products': basket,
               'favorites_products': list(
                   *list(zip(*Favorites.objects.filter(user=request.user).values_list('product'))))}
    return render(request, 'basket/basket.html', context=context)


class FavoritesView(BaseMixin, ListView):
    model = Favorites
    template_name = 'basket/favorites.html'
    context_object_name = 'favorites_products'
    title = 'StuffStore - Избранное'

    def get_queryset(self) -> QuerySet[Any]:
        # return Favorites.objects.filter(user=self.request.user).select_related('product')
        return Product.objects.filter(favorite__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_products'] = Basket.objects.filter(user=self.request.user)
        return context
