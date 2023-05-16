from django import forms

from app_newsletter.models import Client, Newsletter


class SelectMultipleWithAllOption(forms.SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value is None:
            option['attrs']['value'] = 'all'
            option['label'] = 'Выбрать все'
        return option


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'first_name', 'last_name', 'middle_name']
        labels = {
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество (необязательно)'
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите электронную почту'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите имя'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите фамилию'
                }
            ),
            'middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите отчество'
                }
            )
        }


class NewsletterCreateForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        label='Клиенты',
        widget=SelectMultipleWithAllOption(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    class Meta:
        model = Newsletter
        fields = ['time', 'frequency', 'status', 'clients', 'messages']
        labels = {
            'time': 'Время',
            'frequency': 'Периодичность',
            'status': 'Статус',
            'clients': 'Клиенты',
            'messages': 'Сообщения'
        }
        widgets = {
            'time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите время рассылки',
                    'type': 'time'
                }
            ),
            'frequency': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'messages': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                }
            )
        }
