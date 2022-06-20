from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea, TextInput, PasswordInput, EmailInput

from main.models import Comment

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст комментария',
                'rows': 2,
            }),
        }


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
