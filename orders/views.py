import stripe
from django.http import HttpResponseRedirect
from http import HTTPStatus
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from basket.models import Basket, Favorites
from orders.forms import OrderForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from products.mixins import BaseMixin
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CancelView(TemplateView):
    template_name = 'orders/cancel.html'

class OrderCreateView(BaseMixin, CreateView):
    template_name = 'orders/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order')
    title = 'StuffStore - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1P3PUsP1duGM5UfbMr75VQOv',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}'.format(settings.DOMAIN_NAME),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order-canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response = super(OrderCreateView, self).form_valid(form)
        messages.success(self.request, "Заказ оплачен!")
        return response

    def form_invalid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, "Проверьте правильность ввода данных!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_products'] = Basket.objects.filter(user=self.request.user).all()
        return context
