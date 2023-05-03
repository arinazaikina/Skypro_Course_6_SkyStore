import random

from django.core.management import BaseCommand

from app_catalog.models import Category, Product


class Command(BaseCommand):
    """
    Команда для наполнения базы данных тестовыми данными категорий и товаров.

    Удаляет все существующие объекты категорий и товаров, создает список категорий,
    а затем генерирует случайные объекты товаров с разными характеристиками, привязанными
    к этим категориям.
    """
    help = 'Populating the database with test data'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_list = [
            'Рассылки', 'Телеграм бот', 'Полезные утилиты',
            'Веб-приложения', 'Микросервисы'
        ]
        category_objects = []
        for category in category_list:
            category_objects.append(
                Category(name=category)
            )
        Category.objects.bulk_create(objs=category_objects)

        products_data = {
            'names': [
                'Удобный сервис рассылок', 'Мощный телеграм-бот', 'Полезный генератор паролей',
                'Простой конструктор веб-приложений', 'Микросервис для оптимизации изображений'
            ],
            'prices': [140, 250, 75, 120, 190],
            'features': [
                'Неограниченная лицензия', 'Поддержка', 'Установка на сервер',
                'Получение обновлений', 'Совместимость с мобильными устройствами'
            ]
        }
        product_objects = []
        for _ in range(10):
            category = random.choice(Category.objects.all())
            features = random.sample(products_data['features'], k=random.randint(1, len(products_data['features'])))
            description = "- " + "\n- ".join(features)
            product = Product(
                name=f"{random.choice(products_data.get('names'))}-{random.randint(1, 10)}",
                description=description,
                category=category,
                price=random.choice(products_data.get('prices'))
            )
            product_objects.append(product)
        Product.objects.bulk_create(objs=product_objects)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data'))
