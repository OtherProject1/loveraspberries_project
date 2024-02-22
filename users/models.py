from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# Для карты пока что временный класс
class Card(models.Model):
    card_number = models.CharField(max_length=16)
    hidden_number = models.CharField(max_length=4)
    month = models.IntegerField()
    year = models.IntegerField()


class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    gender = models.BooleanField(default=False)
    card = models.OneToOneField(to=Card, on_delete=models.PROTECT, null=True)
