# Generated by Django 4.2 on 2023-05-31 12:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0003_companycontact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0, message='Цена не может быть меньше 0')], verbose_name='Цена'),
        ),
    ]
