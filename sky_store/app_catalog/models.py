from typing import Union, Optional

from django.core.validators import MinValueValidator
from django.db import models

from app_user.models import CustomUser

NULLABLE = {'blank': True, 'null': True}


class Feedback(models.Model):
    """
    Модель, описывающая обратную связь
    """
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'Отзыв №{self.pk} от {self.name}'


class Category(models.Model):
    """
    Модель, описывающая категорию товара
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_all_categories(cls) -> models.QuerySet:
        """
        Возвращает все категории товаров

        :return: QuerySet c категориями товаров
        """
        return cls.objects.all()

    @classmethod
    def get_category_by_id(cls, category_id: int) -> 'Category':
        """
        Возвращает категорию по её идентификатору.

        :param category_id: Идентификатор категории, которую нужно получить.
        :return: Объект категории с указанным идентификатором.
        """
        return cls.objects.get(id=category_id)


class Product(models.Model):
    """
    Модель, описывающая товар
    """
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='products/', verbose_name='Изображение (превью)', default='products/default.png'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0, message='Цена не может быть меньше 0')]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Кем создан', default=1)
    is_published = models.BooleanField(verbose_name='Опубликован', default=False)

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.category} - {self.price}"

    @classmethod
    def get_last_products(cls, count: int) -> models.QuerySet:
        """
        Возвращает последние товары в количестве 'count'.

        :param count: Количество товаров, которые нужно получить
        :return: QuerySet c последними товарами
        """
        return cls.objects.order_by('-created_at')[:count]

    @classmethod
    def get_products_by_category(cls, category_id: int) -> models.QuerySet:
        """
        Возвращает товары определённой категории.
        :param category_id: Идентификатор категории товаров
        :return: QuerySet c товарами выбранной категории
        """
        return cls.objects.filter(category_id=category_id)

    @classmethod
    def get_all_products(cls) -> models.QuerySet:
        """
        Возвращает все товары

        :return: QuerySet c товарами
        """
        return cls.objects.all()

    @classmethod
    def create_product(cls, name: str, description: str, category: Category, price: float,
                       image: Union[str, models.ImageField] = None) -> 'Product':
        """
        Создает и сохраняет новый объект товара с заданными параметрами.

        :param name: Название товара.
        :param description: Описание товара.
        :param category: Категория товара.
        :param price: Цена товара.
        :param image: Изображение товара (путь к файлу) или объект ImageField. Если изображение не указано,
        будет использовано изображение по умолчанию.
        :return: Созданный объект товара.
        """
        if not image:
            image = 'products/default.png'

        product = cls(
            name=name,
            description=description,
            image=image,
            category=category,
            price=price
        )
        product.save()
        return product

    def get_active_version(self) -> Optional['Version']:
        """
        Возвращает активную версию товара, если она существует.
        Если активная версия не найдена, возвращает None
        """
        return self.version.filter(is_current_version=True).first()

    @classmethod
    def get_published_products_by_category(cls, category_id: int) -> models.QuerySet:
        """
        Возвращает опубликованные товары определенной категории.
        :param category_id: Идентификатор категории товаров
        :return: QuerySet с опубликованными товарами выбранной категории
        """
        return cls.objects.filter(category_id=category_id, is_published=True)

    @classmethod
    def get_all_published_products(cls) -> models.QuerySet:
        """
        Возвращает все опубликованные товары.

        :return: QuerySet с опубликованными товарами
        """
        return cls.objects.filter(is_published=True)

    @classmethod
    def get_products_by_user(cls, user_id: int) -> models.QuerySet:
        """
        Возвращает товары, созданные указанным пользователем.
        :param user_id: Идентификатор пользователя
        :return: QuerySet c товарами выбранного пользователя
        """
        return cls.objects.filter(created_by_id=user_id)

    @classmethod
    def get_unpublished_products(cls) -> models.QuerySet:
        """
        Возвращает все неопубликованные товары.

        :return: QuerySet с неопубликованными товарами
        """
        return cls.objects.filter(is_published=False)


class Version(models.Model):
    """
    Модель, описывающая версию товара.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='version', verbose_name='Продукт')
    version_number = models.CharField(max_length=100, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current_version = models.BooleanField(default=False, verbose_name='Текущая версия')

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        db_table = 'versions'

    def __str__(self):
        return f"{self.version_number}: {self.version_name}"


class CompanyContact(models.Model):
    """
    Модель, описывающая контакты компании
    """
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    postcode = models.CharField(max_length=20, verbose_name='Индекс', **NULLABLE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    email = models.EmailField(max_length=255, verbose_name='Электронная почта', **NULLABLE)
    tin = models.CharField(max_length=100, verbose_name='ИНН', **NULLABLE)

    class Meta:
        db_table = 'company_contact'
        verbose_name = 'Контакт компании'
        verbose_name_plural = 'Контакты компании'

    def __str__(self):
        return f"{self.country}, {self.city}, {self.address}"

    @classmethod
    def get_company_contacts(cls, count: int) -> models.QuerySet:
        """
        Возвращает все адреса компании

        :param count: Количество контактов, которые нужно получить
        :return: QuerySet c адресами компании
        """
        return cls.objects.all()[:count]
