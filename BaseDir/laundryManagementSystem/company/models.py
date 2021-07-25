from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here

class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SignUp(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=30)
    password = models.CharField(max_length =40)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }


class companyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length = 20)
    mobile = models.CharField(max_length=10)
    photo = models.ImageField(blank=True, null=True, upload_to='images/')
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=30, default="Company")



    def __str__(self):
        return self.user.username
