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
        self.slug = pytils.translit.slugify(f'{self.category_id.name}-{self.name}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'subcategory_slug': self.slug})
