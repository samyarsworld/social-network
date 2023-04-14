from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    name = models.CharField(default='None' ,max_length=200, blank=True, null=True)
    last = models.CharField(default='None' ,max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')
    pic = models.ImageField(max_length=1000, default="https://res.cloudinary.com/dizjm7yrb/image/upload/v1679930612/profile_img/u2hphaff7nxk1uyf09us.png")
    date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(default='None' ,max_length=200, blank=True, null=True)
    education = models.CharField(default='None' ,max_length=200, blank=True, null=True)
    phone = models.IntegerField(default=0 ,blank=True, null=True)
    about = models.CharField(default='None' ,max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name
