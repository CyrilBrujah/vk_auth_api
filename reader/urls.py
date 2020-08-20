from django.urls import path

from .views import GetCodeView, GetTokenView, ProfileView
from rest_framework import routers



app_name = "reader"

router = routers.DefaultRouter()
router.register(r'profiles', ProfileView, basename='profiles')


urlpatterns = [
    path('get_code/', GetCodeView.as_view()),
    path('token/', GetTokenView.as_view()),
]

urlpatterns += router.urls
