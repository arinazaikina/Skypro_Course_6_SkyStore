from django import forms
from django.core.validators import RegexValidator

from .models import Product


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


class ProductForm(forms.ModelForm):
    """
    Форма для создания товара
    """
    FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализирует форму и добавляет CSS-классы и
        плейсхолдеры для полей формы.
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['name'].widget.attrs['placeholder'] = 'Введите название товара'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание товара'

    def clean_name(self) -> str:
        """
        Валидация названия продукта.
        Проверяет наличие запрещенных слов в названии.

        :return: Очищенное название продукта.
        :raises: forms.ValidationError, если название содержит запрещенное слово.
        """
        name = self.cleaned_data['name']
        for word in self.FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Название содержит запрещенное слово: {word}")
        return name

    def clean_description(self) -> str:
        """
        Валидация описания продукта.
        Проверяет наличие запрещенных слов в описании.

        :return: Очищенное описание продукта.
        :raises: forms.ValidationError, если описание содержит запрещенное слово.
        """
        description = self.cleaned_data['description']
        for word in self.FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"Описание содержит запрещенное слово: {word}")
        return description

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
