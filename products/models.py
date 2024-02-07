from django.db import models
from django.utils.text import slugify
from .scripts import translit_to_eng


# class SlugMixin:
    # def save(self, *args, **kwargs):
        # self.slug = translit_to_eng(f'{self.name}-{self.pk}')
#         return super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = translit_to_eng(self.name)
        return super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=128)
    category_id = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = translit_to_eng(f'{self.category_id.name} {self.name}')
        return super(SubCategory, self).save(*args, **kwargs)