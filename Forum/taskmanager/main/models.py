import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField('название статьи', max_length=100)
    anons = models.CharField('анонс', max_length=250, blank=True)
    full_text = models.TextField('текст статьи')
    pub_date = models.DateTimeField('дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class User(AbstractUser):

    email = models.EmailField('адрес email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', blank=True, null=True, related_name='comment_article')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"