from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class SignUp(models.Model):
    name = models.CharField(max_length=25)
    email= models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = '__all__'
        labels = {
            # Hii ina-overwrite label zote majina ya form input
            #'password2': 'Re-enter your password' hii itafanya ionekane 'Re-enter your password instead of 'password'
            # Now I want to make all labels to be none
            'name':'',
            'email':'',
            'password':'Enter your passwrd',
            'password2':'Re-enter your password'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Enter email'}),
            'password': forms.PasswordInput(),
            #'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your password'}),
            'password2': forms.PasswordInput(),
            #'password2': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Re-enter your password'})
        }

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password2 != password:
            raise forms.ValidationError('Unmatched passwords')
        return password2

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    photo = models.ImageField(blank=True, null=True, upload_to='images/')
    location = models.CharField(max_length = 100, null=True, blank=True)
    address = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return self.user.username


# for testing saving data to db

class UserProfile0(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    photo = models.ImageField(blank=True, null=True)
    location = models.CharField(max_length = 100, null=True, blank=True)
    address = models.CharField(max_length=70, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.username



class EmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=User.objects.get(email=username)
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id').first()
        except User.DoesNotExist:
            return None
        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
