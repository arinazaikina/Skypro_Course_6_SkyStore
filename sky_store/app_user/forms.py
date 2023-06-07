import re
from typing import Optional

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import CustomUser


class BaseUserForm(forms.ModelForm):
    """
    Базовая форма для создания и редактирования пользователя,
    содержащая методы валидации.
    """

    def clean(self):
        """
        Проверка дополнительных условий при валидации формы.
        Переопределяет метод clean() и добавляет проверки
        для полей first_name и last_name.
        Если имя/фамилия отсутствуют или состоят только из пробелов,
        будет показана ошибка под соответствующим полем.
        """
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name is None or first_name.strip() == "":
            self.add_error('first_name', "Имя обязательно для заполнения")

        if last_name is None or last_name.strip() == "":
            self.add_error('last_name', "Фамилия обязательна для заполнения")

    def clean_phone(self) -> Optional[str]:
        """
        Валидация поля "Телефон".
        Проверяет, что номер содержит от 10 до 15 символов и состоит только из цифр,
        пробелов, знака плюс и дефисов. Если введенный номер не соответствует указанному
        формату, возбуждает ошибку валидации формы.
        """
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[\+\-\s\d]{10,15}$', phone):
            raise forms.ValidationError("Неверный формат телефонного номера")
        return phone


class UserRegistrationForm(UserCreationForm, BaseUserForm):
    """
    Форма для регистрации пользователя.
    Наследуется от BasUserForm и UserCreationForm Django.
    Предоставляет поля для ввода электронной почты, имени,
    фамилии, телефона, страны, пароля, повтора пароля и
    загрузки аватарки.
    """

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'country', 'avatar']

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и добавляет CSS-классы и плейсхолдеры для полей формы.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'})
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'})
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'})
        self.fields['phone'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ваш телефон'})
        self.fields['country'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите вашу страну'})
        self.fields['avatar'].widget = forms.FileInput(
            attrs={'class': 'form-control-file'})

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите ваш пароль'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Повторите ваш пароль'})


class UserLoginForm(AuthenticationForm):
    """
    Форма для входа пользователя в систему.
    Наследуется от AuthenticationForm Django.
    Предоставляет поля для ввода электронной почты и пароля.
    """
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и добавляет CSS-классы и плейсхолдеры для полей формы.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        })


class UserUpdateForm(BaseUserForm, forms.ModelForm):
    """
    Форма для редактирования пользователя.
    Наследуется от BaseUserForm ModelForm Django.
    Предоставляет поля для ввода имени, фамилии, телефона, страны и
    поле для загрузки аватарки.
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'country', 'avatar']

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и добавляет CSS-классы и плейсхолдеры для полей формы.
        """
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'})
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'})
        self.fields['phone'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ваш телефон'})
        self.fields['country'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите вашу страну'})
        self.fields['avatar'].widget = forms.FileInput(
            attrs={'class': 'form-control-file'})


class CustomPasswordResetForm(PasswordResetForm):
    """
    Форма для сброса пароля.
    Наследуется от Django PasswordResetForm.
    Предоставляет поле для ввода электронной почты, на которую
    будет отправлена ссылка для восстановления пароля.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и добавляет CSS-классы и плейсхолдеры для полей формы.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите вашу электронную почту'})


class CustomSetPasswordForm(SetPasswordForm):
    """
    Форма для установки нового пароля.
    Наследуется от Django SetPasswordForm.
    Предоставляет поле для ввода нового пароля и поле
    для его подтверждения.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и добавляет CSS-классы и плейсхолдеры для полей формы.
        """
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'})
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'})
