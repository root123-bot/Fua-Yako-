from django.shortcuts import render, redirect
from .forms import LaundryForm, ChangeProfile
from django.http import HttpResponseRedirect
from .forms import LaundryForm, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from laundryManagementSystem.laundryman.models import LaundryProfile
from laundryManagementSystem.addtocart.models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = LaundryForm(request.POST)

        if form.is_valid():
            form.save()
            print('Form is saved ')
            return HttpResponseRedirect('/laundry/profile/')

    else:
        form = LaundryForm()
    context = {'form':form}
    return render(request, 'laundryman/index.html', context)

def laundrylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('viewprofile/')
        else:
            messages.error(request, 'Incorrent username/password')
    context = {}
    return render(request, 'laundryman/login.html', context) 


class LaundryProfileView(TemplateView):
    template_name = 'company/company_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = LaundryProfile.objects.get(user=self.request.user)

        wilaya = profile.district
        mkoa = profile.region
        kata = profile.ward
        mtaa = profile.street
        laundry_name = profile.user.username
        email = profile.user.email
        mobile = profile.tele
        pic = profile.photo.url
        anuani = profile.location
  
        context['name'] = laundry_name
        context['region'] = mkoa
        context['district'] = wilaya
        context['ward'] = kata
        context['street'] = mtaa
        context['mobile'] = mobile
        context['pic'] = pic
        context['anuani'] = anuani
        context['email'] = email

        return context
    
def changeProfileForm(request):
    if request.method == 'POST':
        form = ChangeProfile(request.POST, request.FILES)
        user = User.objects.get(username = request.user.username)
        print(user)
        profile = LaundryProfile.objects.get(user=request.user)
        pic = profile.photo.url
        if user and profile:
            if form.is_valid():  
                user.email = form.cleaned_data['email']
                print(user.email)
                user.save()
                profile.photo = form.cleaned_data['profile_picture']
                profile.tele = form.cleaned_data['contact']
                profile.location = form.cleaned_data['location']
                profile.region = form.cleaned_data['region']
                profile.district = form.cleaned_data['district']
                profile.ward = form.cleaned_data['ward']
                profile.street = form.cleaned_data['street']

                profile.save()
                messages.success(request, "Your information has successful updated")
                return HttpResponseRedirect('viewprofile/')
    else: 
        form = ChangeProfile()
        profile = LaundryProfile.objects.get(user=request.user)
        pic = profile.photo.url
    context = {'form':form, 'pic':pic}
    return render(request, 'laundryman/editProfile.html', context)



def profile(request):
    if request.method == 'POST':
        profile_form = Profile(request.POST, request.FILES)

        if profile_form.is_valid():
            user = User.objects.latest('date_joined')
            # this latest method is used to deal online with the date
            # attributes not interger like id and its only  return
            # single value, so it's never iterable, so when you query
            # id it will throw an error  like
            # User.objects.latest('id=2') since its only deals with
            # the dates objects. THANKS StackOverFlow

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            print('Profile form is saved')
            return HttpResponseRedirect('laundry/login')
    else:
        profile_form = Profile()

    context = {'profile_form': profile_form}
    return render(request, 'laundryman/profile.html', context)



def viewNotification(request):
    # When a user click link I want to drag all post information from the database and pass as contex variable to notification link
    # Fist all post records associated with this company
    username = request.user.username
    print(username)
    posts_qs = Post.objects.filter(receiver=username).order_by('-created_at')

    print(posts_qs)
    context = {'queryset': posts_qs}
    return render(request, 'laundryman/notification.html', context)
