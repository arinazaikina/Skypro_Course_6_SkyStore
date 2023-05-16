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
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly')
    ]

    STATUS_CHOICES = [
        ('F', 'Finished'),
        ('C', 'Created'),
        ('S', 'Started')
    ]

    time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', related_name='newsletters')
    messages = models.ManyToManyField('Message', verbose_name='Сообщения', related_name='newsletters')

    class Meta:
        db_table = 'newsletters'
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Newsletter #{self.id} for {self.client.email}"


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
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='newsletter_log'
    )

    class Meta:
        db_table = 'newsletter_logs'
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'

    def __str__(self):
        return f'{self.status}: {self.date_time}'
