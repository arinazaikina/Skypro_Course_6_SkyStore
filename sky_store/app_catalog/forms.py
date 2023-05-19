from django import forms
from django.core.validators import RegexValidator, MinValueValidator

from .models import Category


class FeedbackForm(forms.Form):
    phone_validator = RegexValidator(
        regex=r'^\+7\(\d{3}\)\d{3}-\d{4}$',
        message='Некорректный номер телефона. Формат номера: +7(XXX)XXX-XXXX'
    )

    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'required': True,
        }),
    )
    phone = forms.CharField(
        max_length=20,
        validators=[phone_validator],
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Контактный телефон',
            'required': True,
        }),
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше сообщение',
            'required': True,
        }),
    )


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Название',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название товара',
        }),
    )

    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите описание товара',
        }),
    )

    image = forms.ImageField(
        label='Изображение (превью)',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        })
    )

    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.get_all_categories(),
        widget=forms.Select(attrs={
            'class': 'form-control',

        })
    )

    price = forms.DecimalField(
        label='Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1, message='Цена должна быть больше 0')],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
