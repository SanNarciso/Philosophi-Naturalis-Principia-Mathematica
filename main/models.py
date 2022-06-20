from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):
    pass


class Video(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    file = models.FileField(
        default='',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    image = models.ImageField(default='')

    create_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    question = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Вопрос', blank=True, null=True, related_name='comments_video')
    text = models.TextField(verbose_name='')
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

