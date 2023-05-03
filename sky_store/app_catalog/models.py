from django.db import models

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
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

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
