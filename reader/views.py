from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import api_view, action, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import django.db

from .models import Profile
from .serializers import ProfileSerializer


import requests


version = '5.122'
client_id = 7572251


@api_view(['GET'])
def get_code(request, format=None):
    """
    Запрос на получение страницы авторизации vk
    """
    response = requests.get("https://oauth.vk.com/authorize/",
                            params={'client_id': client_id, 'redirect_uri': 'http://127.0.0.1:8000/api/token', 'display': 'page',   'response_type': 'code', 'v': version})
    return HttpResponseRedirect(response.url)


@api_view(["GET"])
def token(request, format=None):
    """
    Запрос на получение token для доступа к методам api vk. В случае успешного получения токена создается новый запрос на получение информации о профиле пользователя vk. Профиль пользователя заносится в БД сервера или обновляет токен существующего пользователя
    """
    code = request.query_params['code']
    response = requests.get("https://oauth.vk.com/access_token",
                            params={'client_id': client_id, 'client_secret': '5IwMHn55CcxuhnDt8dZj',
                                    'redirect_uri': 'http://127.0.0.1:8000/api/token', 'code': code})
    access_token = response.json()['access_token']
    user_id = response.json()['user_id']
    response = requests.get("https://api.vk.com/method/users.get",
                            params={'user_id': user_id, 'access_token': access_token, 'v': version})
    result = response.json()['response']
    result = result[0]
    vk_id = result['id']
    first_name = result['first_name']
    last_name = result['last_name']
    try:
        Profile.objects.create(vk_id=vk_id, first_name=first_name,
                               last_name=last_name, access_token=access_token)
    except django.db.IntegrityError:
        profile = Profile.objects.get(pk=vk_id)
        profile.access_token = access_token
        profile.save()
    return HttpResponseRedirect(reverse('reader:profiles-detail', args=[vk_id]))


class ProfilesViewSet(viewsets.ViewSet):
    """
    ViewSet для получения информации о профилях, хранящихся в БД
    """

    def list(self, request):
        """
        Метод получения списка пользователей в формате JSON
        """
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Метод получения отдельного пользователя по его vk id. Результат выводится в формате JSON
        """
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def delete_profile(self, request, pk):
        """
        Метод удаления профиля из БД
        """
        profile = Profile.objects.get(pk=pk)
        profile.delete()
        return HttpResponseRedirect(reverse('reader:profiles-list'))

    @action(detail=True, methods=['GET'], renderer_classes=([TemplateHTMLRenderer]))
    def friends(self, request, pk):
        """
        Проверочный метод для получения списка идентификаторов друзей пользователя.
        Результат выводится с помощью html-шаблона.
        """
        profile = Profile.objects.get(pk=pk)
        response = requests.get("https://api.vk.com/method/friends.get", params={
            'user_id': profile.vk_id, 'access_token': profile.access_token, 'v': version
        })
        friends = response.json()['response']
        template_name = 'reader/friends.html'
        context = {'profile': profile, 'friends': friends}
        return Response(context, template_name=template_name)
