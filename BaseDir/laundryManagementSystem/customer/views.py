from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponseRedirect
from .forms import CustomUserForm, UserProfileForm, ExtendUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #insert into DB
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'customer/signup.html', {'form':form})


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and userProfileForm.is_valid():
            user = form.save()
            profile = userProfileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('laundry/login/')

    else:
        form = CustomUserForm()
        userProfileForm = UserProfileForm()

    context = {'form':form, 'profile':UserProfileForm}
    return render(request, 'customer/index.html', context)


def customerlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('index2/')
        else:
            messages.error(request, 'Incorrent username/password')
    context = {}
    return render(request, 'laundryman/login.html', context) 


# Demo for testing
def registerDemo(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        profile_form = ExtendUserForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile=profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('laundry/login')

    else:
        form = CustomUserForm()
        profile_form = ExtendUserForm() 

    return render(request, 'customer/index2.html', {'form':form, 'profile_form':profile_form}) 
