from django.urls import path

from .views import GetCodeView, GetTokenView, ProfileView
from rest_framework import routers



#app_name = "api"

router = routers.DefaultRouter()
router.register(r'profiles', ProfileView, basename='profiles')
#router.register(r'get_code', GetCodeView, basename='get_code')


urlpatterns = [
    #path('profiles/', ProfileView.as_view({'get': 'list'})),
    #path('profiles/<int:pk>', ProfileView.as_view({'get': 'retrieve'})),
    path('get_code/', GetCodeView.as_view()),
    path('token/', GetTokenView.as_view()),
]

urlpatterns += router.urls
