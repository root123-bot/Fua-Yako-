from django.shortcuts import render, get_object_or_404
from .models import companyProfile
from django.db.models import Q 
from ..laundryman.models import LaundryProfile
from django.shortcuts import redirect
from .forms import CompanyForm, CProfile
from django.http import HttpResponseRedirect
#from .forms import LaundryForm, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..laundryman.models import LaundryProfile
from django.views.generic import TemplateView
from .forms import ChangeProfile, ChangePassword
from laundryManagementSystem.addtocart.models import Post
from django import forms
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.core.paginator import Paginator 


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():


            form.save()
            print('Form is saved ')
            return HttpResponseRedirect('company/profile/')

    else:
        form = CompanyForm()
    context = {'form':form}
    return render(request, 'company/index.html', context)

#@login_required(login_url='laundry/login/')
def profile(request):
        if request.method == 'POST':
            profile_form = CProfile(request.POST, request.FILES)

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
                return HttpResponseRedirect('company/login/')
        else:
            profile_form = CProfile()

        context = {'profile_form': profile_form}
        return render(request, 'company/profile.html', context)



def companylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('viewcompanyprofile/')
        else:
            messages.error(request, 'Incorrent username/password')
    context = {}
    return render(request, 'laundryman/login.html', context)

# this will post a user profiles to our home for user to view
@login_required(login_url= 'laundry/login/')
def companiesView(request):
    company_profiles = companyProfile.objects.all().only('id', 'user', 'reg_no', 'photo', 'address', 'category')
    paginator = Paginator(company_profiles, 6)
    page_number = request.GET.get('page')
    company_profiles = paginator.get_page(page_number)
    context = {'company_profiles': company_profiles}
    print(company_profiles)
    return render(request, 'companiesView.html', context)
   

@login_required(login_url= 'laundry/login/')
def laundriesView(request):
    laundry_profiles = LaundryProfile.objects.all().only('id', 'user', 'photo', 'region', 'district', 'ward', 'street', 'location', 'category')
    paginator = Paginator(laundry_profiles, 6)
    page_number = request.GET.get('page')
    print(page_number) # it will GET this page parameter in our url
    laundry_profiles = paginator.get_page(page_number)
    #context = {'product_list':product_list}
    context = {'laundry_profiles': laundry_profiles}
    print(laundry_profiles)
    return render(request, 'laundriesView.html', context)

def search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        print(search_query)
        # the use of __icontains does not work with interger, its only works with 'string',
        # by default the companyProfile and LaundryProfile models have field of 'user' which 
        # references the user model, the user field of these models has reference username  
        # throught the User primary key which here for me is default one which is 'id' id is 
        # integer, so icontains can't do that in 'id', so we shall concatenate our 'user'
        # with 'username' with  this means that in that reference we need our 'user' field which is
        # by default reference all User model fields like id, username, email, password and so on.
        # So here to __icontains the username field which is string unlike id which is interger 
        # we use (user__username__icontains) this username is refered from the User model 'Usename'
        company = companyProfile.objects.filter(Q(user__username__icontains=search_query) | Q(address__icontains=search_query))
        laundry = LaundryProfile.objects.filter(Q(user__username__icontains=search_query) | Q(region__icontains=search_query) | Q(district__icontains=search_query) | Q(ward__icontains=search_query) | Q(street__icontains=search_query) | Q(location__icontains=search_query))
        print(laundry)
        print(company)
    else:
        company = companyProfile.objects.all()
        laundry = LaundryProfile.objects.all()
    context = {'company':company, 'laundry':laundry}
    return render(request, 'results.html', context)



class CompanyProfileView(TemplateView):
    template_name = 'company/company_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = companyProfile.objects.get(user=self.request.user)
        brela_no = profile.reg_no
        comp_name = profile.user.username
        email = profile.user.email
        mobile = profile.mobile
        pic = profile.photo.url
        anuani = profile.address

        context['brela'] = brela_no
        context['name'] = comp_name
        context['mobile'] = mobile
        context['pic'] = pic
        context['anuani'] = anuani
        context['pepe'] = email

        return context 
    
class EditProfile(TemplateView):
    template_name = 'company/editProfile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = companyProfile.objects.get(user=self.request.user)


def changeProfileForm(request):
    if request.method == 'POST':
        form = ChangeProfile(request.POST, request.FILES)
        user = User.objects.get(username = request.user.username)
        print(user)
        profile = companyProfile.objects.get(user=request.user)
        pic = profile.photo.url
        if user and profile:
            if form.is_valid():
                user.email = form.cleaned_data['email']
                print(user.email)
                user.save()
                profile.photo = form.cleaned_data['profile_picture']
                profile.mobile = form.cleaned_data['contact']
                profile.address = form.cleaned_data['location']
                profile.save()
                messages.success(request, "Your information has successful updated")
                return HttpResponseRedirect('viewcompanyprofile/')
    else: 
        form = ChangeProfile()
        profile = companyProfile.objects.get(user=request.user)
        pic = profile.photo.url
    context = {'form':form, 'pic':pic}
    return render(request, 'company/editProfile.html', context)


def viewNotification(request):
    # When a user click link I want to drag all post information from the database and pass as contex variable to notification link
    # Fist all post records associated with this company
    username = request.user.username
    print(username)
    posts_qs = Post.objects.filter(receiver=username).order_by('-created_at')

    print(posts_qs)
    context = {'queryset': posts_qs}
    return render(request, 'company/notification.html', context)


def realseenotification(request, notification_id):
    exactly_element = Post.objects.get(id=notification_id)
    print(exactly_element)

    head = exactly_element.head
    body = exactly_element.body
    sender= exactly_element.sender
    phone = exactly_element.contact
    zipcode = exactly_element.code
    district = exactly_element.district
    ward = exactly_element.ward
    street = exactly_element.street
    location = exactly_element.physical_address
    itemsAndQuantity = exactly_element.items
    context = {'head':head, 'body':body, 'sender':sender, 'phone':phone, 'zipcode':zipcode, 'district':district, 'ward':ward, 'street':street, 'location':location, 'items':itemsAndQuantity}
    return render(request, 'company/viewNotification.html', context)




class PasswordChangeView(PasswordChangeView):
    form_class = ChangePassword
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'company/successChangePassword.html', {})