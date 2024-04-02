from django.urls import path
from .views import *

app_name = 'basket'

urlpatterns = [
    path('add_product_to_basket/<int:product_id>/', add_product_to_basket, name='add_product_to_basket'),
    path('minus_product_to_basket/<int:product_id>/', minus_product_to_basket, name='minus_product_to_basket'),
    path('delete_product_from_basket/<int:basket_id>/', delete_product_from_basket, name='delete_product_from_basket'),
    path('add_product_to_favorites/<int:product_id>/', add_product_to_favorites, name='add_product_to_favorites'),
    path('selected_for_purchase/<int:basket_id>/', selected_for_purchase, name='selected_for_purchase'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('basket/', BasketView.as_view(), name='basket'),
    # path('basket/', basket_products, name='basket'),
    path('ajax/add_product_to_basket/<int:product_id>/', ajax_add_product_to_basket, name='ajax_add_product_to_basket'),
    path('ajax/minus_product_to_basket/<int:product_id>/', ajax_minus_product_to_basket, name='ajax_minus_product_to_basket'),
    path('ajax/delete_product_from_basket/<int:product_id>/', ajax_delete_product_from_basket, name='ajax_minus_product_to_basket'),
    path('ajax/ajax_add_product_to_favorites/<int:product_id>/', ajax_add_product_to_favorites, name='ajax_add_product_to_favorites'),
]
