from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .import views

urlpatterns = [
    path('', views.task_list, name='home'),
    path('geogebra', views.view_geo, name='geogebra'),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('video_list', views.video_list, name="video_list"),
    path('video/<int:pk>', views.video_detail.as_view(), name="video_detail"),
    path('create/video', views.create_video, name="create_video"),
    path('', include('django.contrib.auth.urls')),
    ##path('register/', views.Register.as_view(), name='register'),
    path('create', views.Create.as_view(), name='create_task'),
    path('detail/<pk>', views.DetailTask.as_view(), name='detail'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('signup', views.signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)