from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404


from .models import Profile
from .serializers import ProfileSerializer


import requests


@api_view(['GET'])
def get_code(request, format=None):
    response = requests.get("https://oauth.vk.com/authorize/",
                            #headers={'Content-Type': 'application/json'},
                            params={'client_id': 7572251, 'redirect_uri': 'http://127.0.0.1:8000/api/token', 'display': 'page', 'response_type': 'code', 'v': '5.122'})
    return HttpResponseRedirect(response.url)


@api_view(["GET"])
def token(request, format=None):
    code = request.query_params['code']
    response = requests.get("https://oauth.vk.com/access_token",
                            params={'client_id': 7572251, 'client_secret': '5IwMHn55CcxuhnDt8dZj', 'redirect_uri': 'http://127.0.0.1:8000/api/token', 'code': code})
    access_token = response.json()['access_token']
    user_id = response.json()['user_id']
    response = requests.get("https://api.vk.com/method/users.get",
                            params={'user_id': user_id, 'access_token': access_token, 'v': '5.122'})
    result = response.json()['response']
    result = result[0]
    vk_id = result['id']
    first_name = result['first_name']
    last_name = result['last_name']
    Profile.objects.create(vk_id=vk_id, first_name=first_name,
                           last_name=last_name, access_token=access_token)
    return Response(response.json())


class GetCodeView(APIView):
    def get(self, request):
        response = requests.get("https://oauth.vk.com/authorize/",
                                params={'client_id': 7572251, 'redirect_uri': 'http://127.0.0.1:8000/api/token', 'display': 'page', 'response_type': 'code', 'v': '5.122'})
        return HttpResponseRedirect(response.url)


class GetTokenView(APIView):
    def get(self, request):
        code = request.query_params['code']
        response = requests.get("https://oauth.vk.com/access_token",
                                params={'client_id': 7572251, 'client_secret': '5IwMHn55CcxuhnDt8dZj', 'redirect_uri': 'http://127.0.0.1:8000/api/token', 'code': code})
        access_token = response.json()['access_token']
        user_id = response.json()['user_id']
        response = requests.get("https://api.vk.com/method/users.get",
                                params={'user_id': user_id, 'access_token': access_token, 'v': '5.122'})
        result = response.json()['response']
        result = result[0]
        vk_id = result['id']
        first_name = result['first_name']
        last_name = result['last_name']
        Profile.objects.create(vk_id=vk_id, first_name=first_name,
                               last_name=last_name, access_token=access_token)
        return Response(response.json())


class ProfileView(viewsets.ViewSet):

    def list(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
