# Generated by Django 4.2 on 2023-05-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_newsletter', '0014_alter_newsletter_finish_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(blank=True, choices=[('F', 'Завершена'), ('C', 'Создана'), ('S', 'Запущена')], max_length=1, verbose_name='Статус рассылки'),
        ),
    ]