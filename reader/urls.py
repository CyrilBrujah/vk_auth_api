from django.urls import path

from .views import ProfileView, get_code, token
from rest_framework import routers

app_name = "reader"


urlpatterns = [
    path('get_code/', get_code),
    path('token', token),
    #path('friends/', friends),
]

router = routers.DefaultRouter()
router.register(r'profiles', ProfileView, basename='profiles')

urlpatterns += router.urls
