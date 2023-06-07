from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'preview']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'preview': 'Изображение (превью)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст статьи'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
