from email.policy import default
from pyexpat import model
from datetime import datetime
from queue import Empty
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
import uuid
class mymodel(models.Model):
    first_name=models.CharField(max_length=30,blank=True)
    last_name=models.CharField(max_length=30,blank=True)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    email=models.EmailField(max_length=30)
    faculty=models.CharField(max_length=10,blank=True)
    batch=models.CharField(max_length=10,blank=True)
    image=models.ImageField(upload_to="",default="user.svg")
    phonenumber=models.CharField(max_length=15,blank=True)
    reward=models.IntegerField(default=0,blank=True)
    verified=models.BooleanField(default=False,blank=True)

class stumartmodel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    title=models.CharField(max_length=30,blank=True)
    username=models.CharField(max_length=30)
    image=models.ImageField(upload_to="stumart/products/",blank=True)
    price=models.IntegerField(default=0)
    details=models.TextField(blank=True)
    category=models.CharField(max_length=30,default="other")
    time=models.DateTimeField(auto_now_add=True,blank=True)
    verify=models.BooleanField(default=False,blank=True)

class order_list(models.Model):
    buyer=models.CharField(max_length=30)
    seller=models.CharField(max_length=30,blank=True)
    region=models.CharField(max_length=40)
    product=models.CharField(max_length=40,blank=True)
    first_name=models.CharField(max_length=30,blank=True)
    last_name=models.CharField(max_length=30,blank=True)
    phonenumber=models.CharField(max_length=15,blank=True)
    price=models.IntegerField(default=0,blank=True)
    delivery_charge=models.IntegerField(default=0,blank=True)
    status=models.CharField(max_length=20,blank=True)
    title=models.CharField(max_length=30,blank=True)

class notifications(models.Model):
    username=models.CharField(max_length=30)
    notify=models.TextField()
    status=models.CharField(max_length=8,default="unseen")
    # time=models.CharField(max_length=20,default=datetime.now().strftime("%Y%m%d%H%M%S"))
    time=models.DateTimeField(auto_now_add=True)

class verifyrequest(models.Model):
    username=models.CharField(max_length=30)
    filevalue=models.FileField(upload_to="verify/")

