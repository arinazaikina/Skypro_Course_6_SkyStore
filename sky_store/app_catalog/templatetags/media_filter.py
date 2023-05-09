from django import template
from django.conf import settings

register = template.Library()


@register.filter
def mediapath(value):
    """
    Шаблонный фильтр, который преобразует переданный путь в полный путь для доступа к медиа файлу.
    :param value: относительный путь к медиа файлу
    :return: полный путь к медиа файлу
    """
    return f"{settings.MEDIA_URL}{value}"
