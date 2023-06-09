import logging
from typing import Dict, Any

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from permissions.authenticate import AuthenticatedAccessMixin
from permissions.user_permission import AdminAccessMixin
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import CustomUser
from .services import EmailConfirmationService, email_token_generator

logger = logging.getLogger(__name__)


class UserRegisterView(CreateView):
    """
    Представление для регистрации пользователя.
    Наследуется от CreateView для создания нового экземпляра пользователя.
    После успешной валидации формы, отправляет письмо с подтверждением на email пользователя.
    """
    model = CustomUser
    form_class = UserRegistrationForm
    success_url = reverse_lazy('app_catalog:home')

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        """
        Метод вызывается, если форма валидна.
        Создает и сохраняет пользователя, отправляет письмо с подтверждением.
        :param form: Валидная форма.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.username = user.email
        user.save()

        EmailConfirmationService.send_confirmation_email(user=user, request=self.request)

        messages.success(self.request, 'Спасибо за регистрацию! Вам на почту выслано письмо с подтверждением.')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Возвращает контекстные данные для шаблона
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['header'] = 'Регистрация'
        context['action'] = 'Зарегистрироваться'
        return context


class EmailConfirmationView(View):
    """
    Представление для подтверждения email пользователя.
    При GET запросе проверяет токен и активирует аккаунт пользователя.
    """

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponseRedirect:
        """
        При получении GET запроса декодирует id пользователя, проверяет токен и активирует аккаунт пользователя.
        Если токен невалидный или пользователь не найден, возвращает ошибку.
        :param request: HttpRequest объект.
        :param uidb64: Закодированный id пользователя.
        :param token: Токен для проверки.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.get_user_by_id(user_id=uid)

            logger.debug('Старт процедуры подтверждения email')
            logger.debug(f"Получено из URL user.id = {user.pk}, {user}")
            logger.debug(f"Получено из URL token: {token}")

            if email_token_generator.check_token(user=user, token=token):
                logger.debug('Получен корректный токен')
                user.email_verified = True
                user.is_active = True
                user.save()
                login(request=request, user=user)
                messages.success(request=self.request, message='Регистрация на сайте успешно завершена!')
                return redirect(user.get_absolute_url())

            else:
                logger.debug('Получен некорректный токен')
                messages.error(
                    request=self.request,
                    message='Ваш email не подтверждён! '
                            'Пожалуйста, проверьте вашу почту и следуйте инструкциям '
                            'для подтверждения электронной почты.'
                )
                return HttpResponseRedirect(user.get_absolute_url())
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            messages.error(
                request=self.request,
                message='Ваш email не подтверждён! '
                        'Пожалуйста, проверьте вашу почту и следуйте инструкциям '
                        'для подтверждения электронной почты.'
            )
            return redirect(to='app_catalog:home')


class UserLoginView(LoginView):
    """
    Представление для входа пользователя в систему.
    Наследуется от стандартного Django LoginView.
    Использует UserLoginForm как форму входа и
    отображает эту форму на странице 'app_user/login.html'.
    """
    form_class = UserLoginForm
    template_name = 'app_user/login.html'

    def form_invalid(self, form: UserLoginForm) -> HttpResponse:
        """
        Метод вызывается, если форма недействительна.
        В этом методе происходит проверка подтверждён ли адрес электронной почты,
        заблокирован ли пользователь, существует ли такой адрес электронной почты в системе,
        корректный ли пароль.
        В зависимости от ошибки выводятся соответствующие сообщения об ошибках.
        :param form: Форма, которая не прошла валидацию.
        """
        email = form.data.get('username')

        try:
            user = CustomUser.get_user_by_email(user_email=email)

            if not user.email_verified:
                logger.debug('Попытка логина с неподтверждённой почтой')
                message = 'Ваш email не подтвержден. ' \
                          'Пожалуйста, перейдите по ссылке, отправленной на вашу электронную почту!'
                messages.error(self.request, message=message)
                return redirect(to='app_catalog:home')

        except CustomUser.DoesNotExist:
            logger.debug(f'Пользователь с почтой {form.data.get("username")} не найден')
            message = 'Пользователь с таким адресом электронной почты не найден! ' \
                      'Введите корректный адрес электронной почты или ' \
                      'пройдите регистрацию на нашем сайте, если вы здесь впервые.'
            messages.error(self.request, message=message)
            return redirect(to='app_user:login')

        if form.errors.get('__all__'):
            message = 'Вы ввели неверный пароль!'
            messages.error(self.request, message=message)
            return super().form_invalid(form)

        return super().form_invalid(form)

    def get_success_url(self) -> str:
        """
        Метод возвращает URL-адрес, на который будет перенаправлен
        клиент после успешного входа.
        """
        return self.request.user.get_absolute_url()


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление для выхода пользователя из системы и
    перенаправление на страницу входа.
    """
    logout(request)
    return redirect(to='app_user:login')


class UserUpdateView(AuthenticatedAccessMixin, UpdateView):
    """
    Представление для редактирования профиля пользователя
    """
    model = CustomUser
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        """
        Метод для получения объекта пользователя, который будет редактироваться.
        В данном случае, используется текущий пользователь.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Метод, вызываемый при валидной форме.
        В данном случае, сохраняет изменения и выполняет редирект.
        """
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """
        Возвращает контекстные данные для шаблона
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль | {self.request.user}'
        context['header'] = self.request.user
        context['action'] = 'Сохранить'
        return context


class UserDetailView(AuthenticatedAccessMixin, DetailView):
    """
    Представление для отображения детальной информации о пользователе
    """
    model = CustomUser


class CustomPasswordResetView(PasswordResetView):
    """
    Представление для сброса пароля.
    Наследуется от Django PasswordResetView.
    """
    email_template_name = 'app_user/password_reset_email.html'
    template_name = 'app_user/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('app_user:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Представление для отображения страницы успешной отправки
    ссылки на сброс пароля.
    Наследуется от Django PasswordResetDoneView.
    """
    template_name = 'app_user/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Представление для отображения страницы подтверждения сброса пароля.
    Наследуется от Django PasswordResetConfirmView.
    """
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("app_user:password_reset_complete")
    template_name = "app_user/password_reset_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Представление для отображения страницы успешного сброса пароля.
    Наследуется от Django PasswordResetCompleteView.
    """
    template_name = 'app_user/password_reset_complete.html'


class UserListView(AdminAccessMixin, ListView):
    """
    Представление для отображения списка пользователей сервиса.
    Наследуется от AdminAccessMixin и Django-класса ListView.
    Класс AdminAccessMixin обеспечивает доступ к представлению
    только для администраторов.
    """
    model = CustomUser
    paginate_by = 5

    def get_queryset(self) -> QuerySet[CustomUser]:
        """
        Возвращает queryset со всеми пользователями
        кроме администратора.
        """
        queryset = super().get_queryset()
        return queryset.exclude(is_superuser=True)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Возвращает контекст для шаблона.
        Добавляет список идентификаторов модераторов и контент менеджеров.
        """
        context = super().get_context_data(**kwargs)
        moderator_group = Group.objects.get(name='Модераторы')
        content_manager_group = Group.objects.get(name='Контент менеджеры')
        context['moderator_ids'] = list(moderator_group.user_set.values_list('id', flat=True))
        context['content_manager_ids'] = list(content_manager_group.user_set.values_list('id', flat=True))
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
        Обрабатывает POST-запрос при обновлении групп пользователей.

        Метод получает список идентификаторов пользователей, выбранных
        в форме для каждой группы (модераторы, контент менеджеры).
        Затем он очищает текущих пользователей в группах "Модераторы" и "Контент менеджеры".
        После этого он добавляет выбранных пользователей в соответствующие группы.
        """

        moderator_user_ids = request.POST.getlist('box_moderator')
        moderator_user_ids = [int(id) for id in moderator_user_ids]

        content_manager_user_ids = request.POST.getlist('box_content_manager')
        content_manager_user_ids = [int(id) for id in content_manager_user_ids]

        moderator_group = Group.objects.get(name='Модераторы')
        content_manager_group = Group.objects.get(name='Контент менеджеры')

        moderator_group.user_set.clear()
        content_manager_group.user_set.clear()

        moderator_group.user_set.add(*CustomUser.objects.filter(id__in=moderator_user_ids))
        content_manager_group.user_set.add(*CustomUser.objects.filter(id__in=content_manager_user_ids))

        return HttpResponseRedirect(self.request.path_info)
