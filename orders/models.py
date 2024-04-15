from django.db import models
from users.models import User
from basket.models import Basket


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    RECEIVED = 4
    STATUS = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
        (RECEIVED, 'Получено'),
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

    # Метод для работы с корзиной после оплаты товара
    def update_after_payment(self):
        basket_product = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased': [basket.de_basket_history_json() for basket in basket_product],
            'total_sum': float(basket_product.total_sum()),
        }
        basket_product.delete()
        self.save()
