from django import forms

from app_newsletter.models import Client


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
