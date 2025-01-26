from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    api_key = models.CharField(max_length=50) 
    pass
    
