from django.db import models

"""
class User(models.Model):
    vk_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    access_token = models.TextField(null=True)

    def __str__(self):
        return '%s:\t%s %s' % (self.vk_id, self.first_name, self.last_name)"""

class Profile(models.Model):
    vk_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    access_token = models.TextField(null=True)
