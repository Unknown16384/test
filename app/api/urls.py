from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import UserList, UserDetail, UserDesk, AdminList, AdminDetail

app_name = 'api'
schema_view = get_schema_view(openapi.Info(title='workspace API', default_version='v1'), public=True)

urlpatterns = [
    path('', UserList.as_view()),
    path('<int:id>/', UserDetail.as_view()),
    path('<int:userid>/desk', UserDesk.as_view()),
    path('admin/', AdminList.as_view()),
    path('admin/<int:id>', AdminDetail.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))
]
