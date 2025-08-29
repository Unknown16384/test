from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('', views.index, name=''),
    path('all/', views.user_list, name='all'),
    path('<int:id>/', views.user_detail, name='detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)