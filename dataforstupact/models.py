from email.policy import default
from queue import Empty
from statistics import mode
from django.db import models

class mymodel(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    email=models.EmailField(max_length=30)
    faculty=models.CharField(max_length=10)
    batch=models.CharField(max_length=10)
    image=models.ImageField(upload_to="",default="user.png")

