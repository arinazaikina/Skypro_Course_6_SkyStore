from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class CreatorAccessMixin:
    """
    Миксин, обеспечивающий доступ к редактированию объектов
    только тому пользователю сервиса, который их создал.
    """

    def check_creator_access(self, obj) -> bool:
        """
        Проверяет, имеет ли текущий пользователь доступ
        к редактированию или удалению объекта.
        :param obj: Объект, который нужно проверить.
        """
        return obj.created_by == self.request.user

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
        Переопределение метода dispatch для проверки доступа пользователя
        перед редактированием или удалением объекта.
        Если пользователь не является создателем объекта,
        он будет перенаправлен на главную страницу.
        :param request: HttpRequest объект.
        """
        obj = self.get_object()

        if not self.check_creator_access(obj=obj):
            message = 'У вас нет разрешения на редактирование и удаление этого объекта'
            messages.info(request=self.request, message=message)
            return redirect(reverse('app_catalog:home'))

        return super().dispatch(request, *args, **kwargs)
