from django.db import models
from users.models import User
from products.models import Product


class BasketQueryset(models.QuerySet):
    def total_sum(self):
        # В self хранится Basket.objects.filter(user=self.request.user)
        return sum(basket.sum() for basket in self if basket.selected_for_purchase)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket')
    quantity = models.IntegerField(default=0)
    selected_for_purchase = models.BooleanField(default=True)
    # Подключение собственного Queryset
    objects = BasketQueryset.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username}| Продукт {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorite')
