import pytils
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# class SlugMixin:
# def save(self, *args, **kwargs):
# self.slug = translit_to_eng(f'{self.name}-{self.pk}')
#         return super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = pytils.translit.slugify(self.name)
            return super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = pytils.translit.slugify(f'{self.category.name}-{self.name}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'subcategory_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    subcategory = models.ForeignKey(to=SubCategory, on_delete=models.PROTECT)
    rating = models.DecimalField(max_digits=2, decimal_places=1, )
    review = models.PositiveIntegerField(default=0)

    # details = models.PositiveIntegerField(default=0) для отображения количества полей характеристики
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'subcategory_slug': self.subcategory.slug, 'product_id': self.pk})


class ProductImages(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, related_name='images')
    image = models.ImageField(upload_to='products_images')
