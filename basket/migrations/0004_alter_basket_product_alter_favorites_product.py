# Generated by Django 5.0.1 on 2024-03-17 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0003_favorites'),
        ('products', '0010_remove_product_rating_remove_product_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to='products.product'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='products.product'),
        ),
    ]