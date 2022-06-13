from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render

from .models import Article, Comment

admin.site.register(Article)
admin.site.register(Comment)

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    pass