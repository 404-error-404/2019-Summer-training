from django.db import models

# Create your models here.

class user(models.Model):
    user_name = models.CharField(max_length=50)
    avatar_address = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=20)