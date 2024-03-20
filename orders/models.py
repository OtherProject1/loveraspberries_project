# import stripe
from django.db import models
from users.models import User
from django.conf import settings
from basket.models import Basket

# stripe.api_key = settings.STRIPE_SECRET_KEY

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUS = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ #{self.id}. Для {self.first_name} {self.last_name}'

    # def update_after_payment(self):
    #     baskets = Basket.objects.filter(user=self.initiator)
    #     self.status = self.PAID
    #     self.basket_history = {
    #         'purchased_items': [basket.de_json() for basket in baskets],
    #         'total_sum': float(baskets.total_sum()),
    #     }
    #     baskets.delete()
    #     self.save()