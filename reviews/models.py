from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='reviews', verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время отзыва')
    description = models.TextField()

    class Meta:
        ordering = ['-date', ]


class ReviewImages(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews_images')