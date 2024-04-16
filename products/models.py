import pytils, stripe
from django.db import models
from django.urls import reverse
from django.db.models import Avg
from main import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


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
        return reverse('products:catalog', kwargs={'subcategory_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    subcategory = models.ForeignKey(to=SubCategory, on_delete=models.PROTECT)
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True)

    # details = models.PositiveIntegerField(default=0) для отображения количества полей характеристики
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_page',
                       kwargs={'subcategory_slug': self.subcategory.slug, 'product_id': self.pk})

    def get_avg_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating

    # Для передачи информации о продукте на оплату
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='byn',
        )
        return stripe_product_price

    # Метод будет заполнять информацию для stripe_product_price_id при добавлении товара в бд
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stipe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stipe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class ProductImages(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, related_name='images')
    image = models.ImageField(upload_to='products_images')


class CategoryDetails(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Details(models.Model):
    '''Info about all details, which users choose for yourseld product'''
    name = models.CharField(max_length=128)
    category = models.ForeignKey(to=CategoryDetails, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ProductDetail(models.Model):
    detail = models.ForeignKey(to=Details, on_delete=models.SET_NULL, null=True, related_name='product_details')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='details')
    description = models.CharField(max_length=255)
