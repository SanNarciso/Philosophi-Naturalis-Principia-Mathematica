from django.contrib import admin
from django.urls import path, include
from . import views
from .views import Register, NewsDetailView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name='home'),
    path('<int:pk>', NewsDetailView.as_view(), name='news-detail'),
    path('connect', views.connect, name='connect'),
    path('create', views.create, name='create'),
    path('register', Register.as_view(), name='register'),
    path('profile', views.view_profile, name='profile')
]