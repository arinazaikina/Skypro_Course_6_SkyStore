import logging

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser

logger = logging.getLogger(__name__)


class EmailConfirmTokenGenerator(PasswordResetTokenGenerator):
    """
    Класс, описывающий генератор токенов для подтверждения электронной почты.
    Наследует от PasswordResetTokenGenerator и переопределяет метод для создания хеш-значения.
    """

    def _make_hash_value(self, user: CustomUser, timestamp: int) -> str:
        """
        Создает хеш-значение, которое используется для создания токена.
        :param user: Экземпляр класса CustomUser, для которого создаётся токен.
        :param timestamp: Временная метка, которая используется при создании токена.
        :return: Хеш-значение, состоящее из идентификатора пользователя, временной метки,
        активности пользователя и статуса подтверждения электронной почты.
        """
        return str(user.pk) + str(timestamp) + str(user.is_active) + str(user.email_verified)


email_token_generator = EmailConfirmTokenGenerator()


class EmailConfirmationService:
    @staticmethod
    def send_confirmation_email(user: CustomUser, request: HttpRequest) -> None:
        """
        Отправляет электронное письмо, содержащее ссылку для подтверждения регистрации.
        :param user: Пользователь, которому отправляется письмо.
        :param request: Объект HttpRequest для доступа к текущему сайту.
        """
        current_site = get_current_site(request=request)
        mail_subject = 'Подтверждение регистрации'
        message = render_to_string(
            template_name='app_user/confirmation_email.html',
            context={
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_token_generator.make_token(user=user)
            }
        )

        logger.debug(
            f"user.ID = {user.pk}, "
            f"user.email_verified = {user.email_verified}, "
            f"user.is_active = {user.is_active}"
        )
        logger.debug(f"token = {email_token_generator.make_token(user=user)}")

        email = EmailMessage(
            subject=mail_subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[user.email]
        )
        try:
            email.send()
            logger.debug('Письмо для подтверждения email отправлено')
        except Exception as error:
            logger.error(f'Ошибка отправки письма: {error}')
