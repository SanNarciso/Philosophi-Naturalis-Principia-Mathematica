from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Article, Comment
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, PasswordInput, EmailInput


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'anons', 'full_text', 'pub_date']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'название статьи'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'анонс статьи'
            }),
            "pub_date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'дата публикации'
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'текст статьи'
            })
        }


User = get_user_model()


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            "Логин": TextInput(attrs={
                'class': 'form-control',
            }),
            "Пароль": PasswordInput(attrs={
                'class': 'form-control',
            }),
            "Повтор пароля": PasswordInput(attrs={
                'class': 'form-control',
            }),
            "full_text": EmailInput(attrs={
                'class': 'form-control',
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите комментарий',
                'rows': 2,
            }),
        }