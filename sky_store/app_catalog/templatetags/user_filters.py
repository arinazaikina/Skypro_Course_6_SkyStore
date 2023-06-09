from django import template
from django.contrib.auth.models import Group

from app_user.models import CustomUser

register = template.Library()


@register.filter(name='has_group')
def has_group(user: CustomUser, group_name: str) -> bool:
    """
    Проверяет, принадлежит ли пользователь к определенной группе.

    :param user: Пользователь, которого нужно проверить.
    :param group_name: Название группы, к которой выполняется проверка.
    """
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()
