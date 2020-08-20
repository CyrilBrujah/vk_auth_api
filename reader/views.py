from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404


from .models import Profile
from .serializers import ProfileSerializer


import requests


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class UserView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SingleUserView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class GetCodeView(APIView):
    def get(self, request):
        response = requests.get("https://oauth.vk.com/authorize/",
                                #headers={'Content-Type': 'application/json'},
                                params={'client_id': 7572251, 'redirect_uri': 'http://127.0.0.1:8000/api/token', 'display': 'page', 'response_type': 'code', 'v': '5.122', 'scope': 'friends'})
        # return HttpResponse(response.url)
        return HttpResponseRedirect(response.url)
        # return render(request, 'reader/auth.html', {'response': response})


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
        # return HttpResponse('%s\n%s\n%s\n%s' % (vk_id, first_name, last_name, access_token))
        return Response(response.json())
        # return Response({'message': 'Got some data', 'code': request.query_params['code']})

    def post(self, request):
        return Response({'message': 'Post some data', 'data': request.data})


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
