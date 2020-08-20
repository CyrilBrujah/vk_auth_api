from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('vk_id', 'first_name', 'last_name', 'access_token')
