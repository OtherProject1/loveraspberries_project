from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from products.mixins import BaseMixin
from django.contrib.auth.models import AnonymousUser

from .models import Basket, Favorites
from products.models import Product

# Create your views here.

@login_required
def add_product_to_favorites(request, product_id):
    '''пока делаю, что в избранное могут добавлять только авторихованные юзеры и при этом страница перезагружается'''
    product = Product.objects.get(pk=product_id)
    product_in_favorites = Favorites.objects.get_or_create(user=request.user, product=product)
    if not product_in_favorites[1]: #get_or_create возвращает кортеж, где второй параметр говорит, создан ли элемент (True) или найден (False)
        product_in_favorites[0].delete()
    return redirect('products:home')

@login_required()
def add_product_to_basket(request, product_id):
    '''пока делаю, что в корзину могут добавлять только авторизованные юзеры и при этом страница перезагружается'''
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.get_or_create(user=request.user, product=product)
    if not product_in_basket[1]: #get_or_create возвращает кортеж, где второй параметр говорит, создан ли элемент (True) или найден (False)
        product_in_basket[0].quantity += 1
        product_in_basket[0].save()
    return redirect('products:home')

@login_required()
def minus_product_to_basket(request, product_id):
    '''пока делаю, что в корзину могут добавлять только авторизованные юзеры и при этом страница перезагружается'''
    product = Product.objects.get(pk=product_id)
    product_in_basket = Basket.objects.get_or_create(user=request.user, product=product)
    if not product_in_basket[1]: #get_or_create возвращает кортеж, где второй параметр говорит, создан ли элемент (True) или найден (False)
        product_in_basket[0].quantity -= 1
        product_in_basket[0].save()
        if product_in_basket[0].quantity == 0:
            product_in_basket[0].delete()
    return redirect('products:home')


class BasketView(BaseMixin, ListView):
    model = Basket
    template_name = 'basket/basket.html'
    context_object_name = 'basket_products'

    def get_queryset(self) -> QuerySet[Any]:
        return Basket.objects.filter(user=self.request.user).select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FavoritesView(BaseMixin, ListView):
    model = Favorites
    template_name = 'basket/favorites.html'
    context_object_name = 'favorites_products'

    def get_queryset(self) -> QuerySet[Any]:
        # return Favorites.objects.filter(user=self.request.user).select_related('product')
        return Product.objects.filter(favorite__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_products'] = Basket.objects.filter(user=self.request.user)
        return context