from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import companyProfile
from django.core.validators import RegexValidator



class CompanyForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Company name')

    # this initialize function make parent form to have these properties by default
    # Hii initialize function inabd ikae juu kabisa, Thanks StackOverFlow
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Company name','required': 'required'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Email','required': 'required'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password','required': 'required'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}


    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']

    # Ko hapa the way unavyohit function ya save unafanya hivi vitu
    # vilivyopo humu ndani ambapo username itakua lastname.firstname
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data['first_name']


        if commit:
            user.save()
        return user

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




class CProfile(forms.ModelForm):
    class Meta:
        model = companyProfile
        fields = ['reg_no', 'mobile', 'photo', 'address']

        labels = {
            # Hii ina-overwrite label zote majina ya form input
            #'password2': 'Re-enter your password' hii itafanya ionekane 'Re-enter your password instead of 'password'
            # Now I want to make all labels to be none
            'reg_no':'Brela number',
            'mobile':'Mobile phone',
            'photo':'Company Profile',
            'address':'Location address'
        }



class ChangeProfile(forms.Form):
    profile_picture = forms.ImageField() # the upload_to option is only found in models.ImageField not forms.ImageField
    contact = forms.IntegerField()
    email = forms.EmailField()
    location = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        value = self.cleaned_data['email']

        # let's check if the object with that email is found
        #check = User.objects.exists(email=value)
        if User.objects.filter(email=value).exists():
            raise forms.ValidationError("Email you entered is found, pick another email")
        
        return value

class ChangePassword(PasswordChangeForm):
    """ChangePassword definition."""

    # TODO: Define form fields 
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=50, label="New password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'New password'}))
    new_password2 = forms.CharField(max_length=50, label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'placeholder': 'Confirm password'}))    

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')



