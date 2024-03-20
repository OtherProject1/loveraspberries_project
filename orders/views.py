from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.db.models import Sum, Count
from basket.models import Basket, Favorites
from orders.forms import OrderForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from users.models import User


# class OrderCreateView(CreateView):
#     template_name = 'orders/order.html'
#     form_class = OrderForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['basket'] = Basket.objects.filter(user=self.request.user, selected_for_purchase=1).select_related(
#             'product')
#         context['cost_selected_basket_products'] = Basket.objects.filter(user=self.request.user).filter(
#             selected_for_purchase=1).aggregate(
#             basket_cost=Sum('product__price'), basket_count_products=Sum('quantity'))
#         context['form'] = OrderForm(instance=self.request.user, data=self.request.POST)
#         return context


def orders(request):
    if request.method == 'POST':
        form = OrderForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заказ сформирован!")
            return HttpResponseRedirect(reverse('products:home'))
        else:
            messages.error(request, "Проверьте правильность ввода данных!")
            return HttpResponseRedirect(reverse('orders:order'))
    else:
        basket = Basket.objects.filter(user=request.user)
        context = {'title': 'Личные данные', 'form': OrderForm(instance=request.user),
                   'basket_products': basket}
        return render(request, 'orders/order.html', context)
