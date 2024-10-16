from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import User


# from django.contrib.auth.models import AbstractBaseUser, AbstractUser
# Create your models here.

# class User(models.Model):
#     user_name = models.CharField(max_length=100, unique=True)
#     user_mail = models.EmailField()
#     user_image = models.ImageField(null=True)
#     user_phone = models.CharField(max_length=100)



#     def __str__(self):
#         return f"{self.user_name}, {self.user_mail}"



class CustomUser(models.Model):
       user = models.OneToOneField(User, on_delete=models.CASCADE)
       phone = models.CharField(max_length=15)

       def __str__(self):
              return self.user.username