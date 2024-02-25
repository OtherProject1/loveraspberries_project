from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.categories_list import first_categories, navbar_list, footer_list, cards, payment_list, favourite_cards, \
    shopping_cards, user_reviews
from .models import Category, SubCategory
from django.views.generic import ListView, DetailView
from .mixins import BaseMixin
from products.models import Product

from users.forms import UserLoginForm, UserRegistrationForm

context = {'title': 'LoveRaspberry', 'categories': Category.objects.all(), 'subcategories': SubCategory.objects.all(),
           'navbar': navbar_list, 'footer': footer_list,
           'logo': payment_list, 'bought_cards': cards, 'shopping': shopping_cards, 'payment_list': favourite_cards,
           }

class MainView(BaseMixin, ListView):
    model = Product
    template_name = 'products/main.html'

    # Для отображения категории товара
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data()
        context['title'] = 'LoveRaspberry'
        context['form'] = UserLoginForm()
        context['registration_form'] = UserRegistrationForm()
        return context


def product_page(request, subcategory_slug, product_id):
    product = Product.objects.get(id=product_id)
    slug = SubCategory.objects.get(slug=subcategory_slug)
    context['product'] = product
    context['subcategory'] = slug
    return render(request, 'products/product.html', context)


class ProductDetail(BaseMixin, DetailView):
    model = Product
    template_name = 'products/product.html'
    slug_url_kwarg = ''


class CatalogListView(BaseMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'

    # Для отображения категории товара
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogListView, self).get_context_data()
        subcategory_slug = get_object_or_404(SubCategory, slug=self.kwargs.get('subcategory_slug'))
        context['title'] = subcategory_slug.name
        context['subcategory'] = subcategory_slug
        context['category'] = subcategory_slug.category
        return context

    # Для отображения самого товара
    def get_queryset(self):
        queryset = super(CatalogListView, self).get_queryset()
        subcategory_slug = self.kwargs.get('subcategory_slug')
        # Получаем id категории
        subcategory = SubCategory.objects.get(slug=subcategory_slug)
        subcategory_id = subcategory.id
        return queryset.filter(subcategory_id=subcategory_id) if subcategory_slug else queryset


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
    context['is_not_payment'] = True
    context['title'] = 'Доставки'
    return render(request, 'products/delivery.html', context)


def history(request):
    context['title'] = 'Покупки'
    context['is_auth'] = True
    return render(request, 'products/history.html', context)


def details(request):
    context['title'] = 'Личные данные'
    return render(request, 'products/details.html', context)


def payment_methods(request):
    context['title'] = 'Способы оплаты'
    return render(request, 'products/payment_methods.html', context)


def item_return(request):
    context['title'] = 'Возврат товара'
    return render(request, 'products/item_return.html', context)


def sale_rules(request):
    context['title'] = 'Правила продажи товара'
    return render(request, 'products/sale_rules.html.', context)


def delivery_rules(request):
    context['title'] = 'Правила доставки'
    return render(request, 'products/delivery_rules.html', context)


def terms_rules(request):
    context['title'] = 'Правила пользования торговой площадкой'
    return render(request, 'products/terms.html', context)


def money_return(request):
    context['title'] = 'Возврат денежных средств'
    return render(request, 'products/money_return.html', context)


def policy(request):
    context['title'] = 'Политика обработки персональных данных'
    return render(request, 'products/policy.html', context)


def sale_on_market(request):
    return redirect("https://seller-auth.wildberries.ru/ru/?redirect_url=https://seller.wildberries.ru/")


def point_promo(request):
    return redirect("https://point-promo.wb.ru/")


def guru(request):
    return redirect("https://guru.wildberries.ru/?utm_source=main_footer")


def all_work(request):
    return redirect("https://vsemrabota.ru/appwb")


def digital(request):
    return redirect("https://digital.wildberries.ru/")


def contacts(request):
    context['title'] = 'Контакты'
    return render(request, 'products/contacts.html', context)


def vacancies(request):
    context['title'] = 'Вакансии'
    return render(request, 'products/vacancies.html', context)


def about_us(request):
    context['title'] = 'О нас'
    return render(request, 'products/about_us.html', context)


def franchisee(request):
    return render(request, 'products/franchisee.html', context)


def reviews(request):
    context['is_auth'] = True
    context['reviews'] = user_reviews
    return render(request, 'products/reviews.html', context)
