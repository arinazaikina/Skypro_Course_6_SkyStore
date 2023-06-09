from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from app_catalog.forms import ProductModeratorForm, ProductCreatorForm


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


class AdminAccessMixin:
    """
    Миксин, который обеспечивает доступ к представлению только для администратора.

    Проверка осуществляется по атрибуту is_superuser текущего пользователя.
    Если пользователь не является администратором,
    происходит перенаправление на главную страницу
    с соответствующим информационным сообщением.
    """

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
        Переопределение метода dispatch для проверки прав доступа.
        Если пользователь не является администратором,
        он будет перенаправлен на главную страницу.
        :param request: HttpRequest объект.
        """

        if not request.user.is_superuser:
            messages.info(request=request, message='У вас нет соответствующих прав доступа!')
            return redirect(reverse('app_catalog:home'))

        return super().dispatch(request, *args, **kwargs)


class ModeratorAccessMixin:
    """
    Миксин, который обеспечивает доступ к представлению только для модераторов.

    Если пользователь не является модератором,
    происходит перенаправление на главную страницу
    с соответствующим информационным сообщением.
    """

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
        Переопределение метода dispatch для проверки прав доступа.
        Если пользователь не является модератором,
        он будет перенаправлен на главную страницу.
        :param request: HttpRequest объект.
        """

        if not request.user.groups.filter(name='Модераторы'):
            messages.info(request=request, message='У вас нет соответствующих прав доступа!')
            return redirect(reverse('app_catalog:home'))

        return super().dispatch(request, *args, **kwargs)


class ModeratorOrCreatorMixin(UserPassesTestMixin):
    """
    Миксин, который проверяет, является ли пользователь модератором или создателем объекта.
    """

    def get_form_class(self):
        """
        Возвращает форму в зависимости от роли пользователя.
        """
        if self.request.user.groups.filter(name='Модераторы').exists():
            return ProductModeratorForm
        else:
            return ProductCreatorForm

    def check_creator_access(self, obj) -> bool:
        """
        Проверяет, является ли текущий пользователь создателем объекта.
        :param obj: Объект, который нужно проверить.
        """
        return obj.created_by == self.request.user

    def test_func(self) -> bool:
        """
        Определяет, входит ли пользователь в группу 'Модераторы' или является создателем товара.
        """
        return self.request.user.groups.filter(
            name='Модераторы').exists() or self.check_creator_access(self.get_object())

    def handle_no_permission(self) -> HttpResponseRedirect:
        """
        Метод, который вызывается в случае, если пользователь
        не проходит проверку на соответствие условию в `test_func`.

        В этом случае выводится сообщение, информирующее пользователя о том,
        что у него нет прав на редактирование,
        происходит перенаправление на главную страницу.
        """
        messages.info(self.request, "У вас нет прав для редактирования этого объекта.")
        return redirect('app_catalog:home')


class CombinedAccessMixin:
    """
    Миксин, обеспечивающий доступ к представлению только для создателя и контент-менеджера.

    Если пользователь не является создателем или контент-менеджером,
    происходит перенаправление на главную страницу
    с соответствующим информационным сообщением.
    """

    def check_access(self, obj) -> bool:
        """
        Проверяет, имеет ли текущий пользователь доступ
        к редактированию или удалению объекта.
        :param obj: Объект, который нужно проверить.
        """
        return obj.created_by == self.request.user or self.request.user.groups.filter(name='Контент менеджеры')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
        Переопределение метода dispatch для проверки прав доступа.
        Если пользователь не является создателем или контент менеджером,
        он будет перенаправлен на главную страницу.
        :param request: HttpRequest объект.
        """

        obj = self.get_object()

        if not self.check_access(obj=obj):
            messages.info(request=request, message='У вас нет соответствующих прав доступа!')
            return redirect(reverse('app_catalog:home'))

        return super().dispatch(request, *args, **kwargs)
