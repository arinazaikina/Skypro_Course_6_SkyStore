from django import forms
from django.core.validators import RegexValidator


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
