# Generated by Django 4.2 on 2023-05-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app_newsletter', '0010_alter_newsletterlog_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время завершения рассылки'),
        ),
    ]
