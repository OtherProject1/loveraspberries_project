from django.contrib.auth.models import AnonymousUser

from products.categories_list import first_categories, navbar_list, footer_list, cards, payment_list, favourite_cards, \
    shopping_cards, user_reviews
from .models import Category, SubCategory
from basket.models import Basket


class BaseMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        context.update({'title': self.title, 
                        'categories': Category.objects.all(),
                        'subcategories': SubCategory.objects.all(),
                        'navbar': navbar_list, 'footer': footer_list,
                        'logo': payment_list, 'bought_cards': cards, 'shopping': shopping_cards,
                        'payment_list': favourite_cards,
                        })
        if not isinstance(self.request.user, AnonymousUser):
            context['basket_counter'] = Basket.objects.filter(user=self.request.user).count()
        return context
