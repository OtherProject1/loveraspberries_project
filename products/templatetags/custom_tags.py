from django import template
from django.urls import reverse

from reviews.models import Review
from basket.models import Basket, Favorites


register = template.Library()

@register.simple_tag
def custom_range(count):
    return range(int(count))

@register.simple_tag
def multiply(x, y):
    return str(x*y)

@register.simple_tag
def width_line_rating(product_id, value, all_count):
    count = Review.objects.filter(product=product_id, rating=int(value)).count()
    return [count, int(count)/int(all_count)*100] #the first its common count, the second for rating_line


@register.simple_tag
def find_product_in_basket(product, basket):
    try:
        return basket.get(product=product)
    except:
        return False

@register.inclusion_tag('products/templatetags/card_of_product.html')
def cards_of_products(data, user=None):
    context = {'products': data, 'user': user}
    # if not isinstance(self.request.user, AnonymousUser):
    if user:
        context['basket_products'] = Basket.objects.filter(user=user)
        context['favorites_products'] = list(*list(zip(*Favorites.objects.filter(user=user).values_list('product'))))
    return context

@register.inclusion_tag('products/templatetags/profile_menu.html')
def profile_menu(current_page):
    menu = [
        {'name': 'Профиль', 'href': reverse('users:profile')},
        {'name': 'Доставки и покупки', 'href': reverse('products:delivery')},
        {'name': 'Избранное', 'href': reverse('basket:favorites')},
        {'name': 'Отзывы', 'href': reverse('reviews:reviews')},
        {'name': 'Личные данные', 'href': reverse('users:details')},
    ]
    return {'menu': menu, 'current_page': current_page}