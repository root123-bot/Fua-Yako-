from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LaundryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tele = models.CharField(max_length=10)
    photo = models.ImageField(blank=True, null=True, upload_to='images/')
    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    ward = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    location = models.TextField(max_length=200)
    category = models.CharField(max_length=30, default="Laundryman")
    def __str__(self):  
        return self.user.username
