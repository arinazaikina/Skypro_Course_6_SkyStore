from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from .managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    """
    Модель, описывающая пользователя сервиса рассылок.
    Наследуется от AbstractUser.
    """
    objects = CustomUserManager()

    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', default='users/default.png')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    country = models.CharField(max_length=100, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_user_by_id(cls, user_id: int) -> 'CustomUser':
        """
        Возвращает пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Объект пользователя с указанным идентификатором.
        """
        return cls.objects.get(id=user_id)

    @classmethod
    def get_user_by_email(cls, user_email: str) -> 'CustomUser':
        """
        Возвращает пользователя по его электронной почте.

        :param user_email: Электронная почта пользователя.
        :return: Объект пользователя с указанной электронной почтой.
        """
        return cls.objects.get(email=user_email)

    def get_absolute_url(self) -> str:
        """
        Возвращает абсолютный URL профиля пользователя.

        Используется в Django представлениях (например, в UpdateView)
        для автоматического определения URL-адреса перенаправления
        после успешного обновления экземпляра модели.
        """
        return reverse('app_user:profile', args=[str(self.id)])
