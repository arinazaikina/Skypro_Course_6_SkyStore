from django.db import models
from django.urls import reverse

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель, описывающая клиента
    """
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        db_table = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('app_newsletter:client_detail', args=[str(self.id)])

    def make_inactive(self):
        """
        Делает клиента неактивным.
        """
        self.is_active = False
        self.save()


class Newsletter(models.Model):
    """
    Модель, описывающая рассылку
    """
    FREQUENCY_CHOICES = [
        ('D', 'Раз в день'),
        ('W', 'Раз в неделю'),
        ('M', 'Раз в месяц')
    ]

    STATUS_CHOICES = [
        ('F', 'Завершена'),
        ('C', 'Создана'),
        ('S', 'Запущена')
    ]

    time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус рассылки', blank=True)
    clients = models.ManyToManyField('Client', verbose_name='Клиенты', related_name='newsletters')
    messages = models.ManyToManyField('Message', verbose_name='Сообщения', related_name='newsletters')
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finish_date = models.DateField(verbose_name='Дата завершения рассылки')
    finish_time = models.TimeField(verbose_name='Время завершения рассылки')

    class Meta:
        db_table = 'newsletters'
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка #{self.pk}"

    def get_absolute_url(self):
        return reverse('app_newsletter:newsletter_detail', args=[str(self.pk)])

    def make_inactive(self):
        """
        Делает рассылку неактивной.
        """
        self.is_active = False
        self.save()


class Message(models.Model):
    """
    Модель, описывающая сообщение
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class NewsletterLog(models.Model):
    """
    Модель, описывающая лог рассылки
    """
    STATUS_CHOICES = [
        ('S', 'Success'),
        ('F', 'Failure')
    ]

    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ почтового сервера')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение', **NULLABLE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, verbose_name='Рассылка', **NULLABLE)

    class Meta:
        db_table = 'newsletter_logs'
        verbose_name = 'Лог отправки письма'
        verbose_name_plural = 'Логи отправок писем'

    def __str__(self):
        return f'Лог #{self.pk}'
