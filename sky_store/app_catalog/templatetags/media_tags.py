from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def mediapath(image):
    """
    Функция-шаблонный тег, преобразующий путь к медиа файлу в полный URL для доступа к этому файлу.
    """
    return f"{settings.MEDIA_URL}{image}"
