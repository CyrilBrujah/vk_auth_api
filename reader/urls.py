from django.urls import path

from .views import ProfilesViewSet, get_code, token
from rest_framework import routers

app_name = "reader"


urlpatterns = [
    path('get_code/', get_code, name='get_code'),
    path('token', token, name='token'),
]

router = routers.DefaultRouter()
router.register(r'profiles', ProfilesViewSet, basename='profiles')

urlpatterns += router.urls
