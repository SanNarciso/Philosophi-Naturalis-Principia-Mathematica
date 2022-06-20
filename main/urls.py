from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('geogebra', views.view_geo, name='geogebra'),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('video_list', views.video_list, name="video_list"),
    path('video/<int:pk>', views.video_detail.as_view(), name="video_detail"),
    path('create/video', views.create_video, name="create_video"),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)