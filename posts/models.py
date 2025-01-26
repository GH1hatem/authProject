from django.db import models
# Create your models here.
class Post(models.Model) : 
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200) 
    author = models.ForeignKey('users.User' , on_delete=models.CASCADE)