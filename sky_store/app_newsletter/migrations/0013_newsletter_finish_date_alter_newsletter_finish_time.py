# Generated by Django 4.2 on 2023-05-18 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_newsletter', '0012_alter_newsletter_finish_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='finish_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата завершения рассылки'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='finish_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время завершения рассылки'),
        ),
    ]