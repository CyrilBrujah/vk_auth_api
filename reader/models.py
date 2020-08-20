from django.db import models

class Profile(models.Model):
    vk_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    access_token = models.TextField(null=True)
