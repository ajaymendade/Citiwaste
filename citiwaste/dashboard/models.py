from django.db import models
from django.contrib.auth.models import AbstractUser
from dashboard.manager import UserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    user_type_datas = ((1,'Administrator'),(2,'Driver'),(3,'Citizen'))
    user_type = models.IntegerField(choices=user_type_datas, default=3)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator')
    mobile_no = models.BigIntegerField(default='')
    
    def __str__(self):
        return self.user.email


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    mobile_no = models.BigIntegerField(default='')

    def __str__(self):
        return self.user.email

class Citizen(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen')
    mobile_no = models.BigIntegerField(default='')
    
    def __str__(self):
        return self.user.email

class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaint')
    photo = models.ImageField(upload_to='dashboard')
    latitude = models.DecimalField(max_digits=30, decimal_places=16)
    longitude = models.DecimalField(max_digits=30, decimal_places=16)
    description = models.TextField(default="")
    status_types = ((1,'Pending'),(2,'Completed'))
    datetime = models.DateTimeField(default="2012-12-12 00:00:00")
    status = models.IntegerField(choices=status_types, default=1)
    
    def __str__(self):
        return self.user.email