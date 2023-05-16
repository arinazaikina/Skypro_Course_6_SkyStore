# Generated by Django 4.2 on 2023-05-16 12:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app_newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AlterModelOptions(
            name='newsletterlog',
            options={'verbose_name': 'Лог рассылки', 'verbose_name_plural': 'Логи рассылок'},
        ),
        migrations.AlterModelTable(
            name='message',
            table='messages',
        ),
        migrations.AlterModelTable(
            name='newsletterlog',
            table='newsletter_logs',
        ),
    ]