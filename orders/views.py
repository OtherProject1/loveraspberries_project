import stripe
from django.http import HttpResponseRedirect
from http import HTTPStatus
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from basket.models import Basket, Favorites
from orders.models import Order
from orders.forms import OrderForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from products.mixins import BaseMixin
from django.conf import settings
from main import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET_KEY

# Секретный ключ stripe для подключения оплаты
stripe.api_key = STRIPE_SECRET_KEY



class CancelView(TemplateView):
    template_name = 'orders/cancel.html'


class OrderCreateView(BaseMixin, CreateView):
    template_name = 'orders/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order')
    title = 'StuffStore - Оформление заказа'

    # Логика отправки данных с корзины на оплату
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}'.format(settings.DOMAIN_NAME),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order-canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response = super(OrderCreateView, self).form_valid(form)
        self.message_success(self)
        return response

    @staticmethod
    def message_success(self):
        message = messages.success(self.request, 'Заказ оплачен!')
        return message

    def form_invalid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, "Проверьте правильность ввода данных!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_products'] = Basket.objects.filter(user=self.request.user).all()
        return context


# Обработчик события оплаты
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session, request)

    # Passed signature verification
    return HttpResponse(status=200)


# Логика если оплата прошла успешно
def fulfill_order(session, request):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
