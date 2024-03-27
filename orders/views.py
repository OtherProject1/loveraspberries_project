from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.db.models import Sum, Count
from basket.models import Basket, Favorites
from orders.forms import OrderForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from users.models import User
from django.contrib import messages
from products.mixins import BaseMixin


class OrderCreateView(BaseMixin, CreateView):
    template_name = 'orders/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order')
    title = 'StuffStore - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response = super(OrderCreateView, self).form_valid(form)
        messages.success(self.request, "Заказ сформирован!")
        return response

    def form_invalid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, "Проверьте правильность ввода данных!")
        return response

# def orders(request):
#     if request.method == 'POST':
#         form = OrderForm(instance=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Заказ сформирован!")
#             return HttpResponseRedirect(reverse('products:home'))
#         else:
#             messages.error(request, "Проверьте правильность ввода данных!")
#             return HttpResponseRedirect(reverse('orders:order'))
#     else:
#         basket = Basket.objects.filter(user=request.user)
#         context = {'title': 'StuffStore - Оформление заказа', 'form': OrderForm(instance=request.user),
#                    'basket_products': basket}
#         return render(request, 'orders/order.html', context)
