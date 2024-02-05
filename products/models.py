from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)


class SubCategory(models.Model):
    name = models.CharField(max_length=128)
    category_id = models.ForeignKey(to=Category, on_delete=models.PROTECT)


