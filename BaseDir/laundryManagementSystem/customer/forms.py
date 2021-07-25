from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, UserProfile0
from django.contrib.auth import get_user_model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(label='')
    username = forms.CharField(max_length=50, label='')


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password do not match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        print(user_count)
        if user_count > 0:
            raise forms.ValidationError("This email has already been registered")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        name_count = User.objects.filter(username=username).count()
        print (name_count)
        if name_count > 0:
            raise forms.ValidationError("This username is already taken.")
        return username


# for testing
class ExtendUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile0
        fields = ['phone']
    #def clean_phone(self):
    #    phone = self.cleaned_data.get('phone')
    #    phone_count = User.objects.filter(phone=phone).count()
    #    print (phone_count)
    #    if phone_count > 0:
    #        raise forms.ValidationError('This phone number is already taken.')
    #    return phone
