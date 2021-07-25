"""laundryManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
""" 

from django.conf.urls import include, url
from django.contrib import admin
from laundryManagementSystem.company import views as company_views
from laundryManagementSystem.customer import views as customer_views
from django.views.generic import TemplateView
from laundryManagementSystem.laundryman import views as laundry_views
from laundryManagementSystem.demo import views as demo_views
from django.conf import settings
from django.conf.urls.static import static
from laundryManagementSystem.addtocart.views import PricingView, DemoView, AddedToCart, MyCartView, ManageCartView, EmptyCartView, CheckoutView
from laundryManagementSystem.addtocart import views as addtocart_views
from laundryManagementSystem.demo.views import HomeView, CustomDetailView, TestingRESTAPI
from laundryManagementSystem.addtocart.views import AddedOrderItems
from django.urls import path
from laundryManagementSystem.RESTfulAPI import views as RESTfulAPI_views
from rest_framework import routers
from rest_framework.authtoken import views
from laundryManagementSystem.company.views import CompanyProfileView  
from django.contrib.auth import views as auth_views
from laundryManagementSystem.Payment import views as payment_views
from django.views.static import serve

router = routers.DefaultRouter()
router.register(r'rest6', RESTfulAPI_views.ProductViewSet)
# Here above we register our router which accept two argument first one is 
# the REST url preffix('inamaanisha url inayoanzia rest6' ni rest6 sio rest5 or rest)
# second is  our view set


# The combination of viewset and router automatically create a sensitive
# REST end points (e.g. delete and update) which by default are accessible
# to anyone

# REMEMBER THE REST SERVICE END POINT (is the url loaded to browser)
urlpatterns = [
    path('confirmed/', TemplateView.as_view(template_name="payment/confirm.html"), name="confirmedPosted"),
    path('changeNamba/', TemplateView.as_view(template_name='payment/changeno.html'), name="doUWantToChangeIt"),
    path('finishHim', addtocart_views.succeedPayment, name="finishHim"),
    path('handlingPaymentNumber/', payment_views.handlingPaymentNumber, name = "pay"),
    path('clickPay/', payment_views.get_jsonResponse, name="payButton"),
    path('paymentAPI/', RESTfulAPI_views.payment, name="paymentAPI"),
    path('changePassword/', company_views.PasswordChangeView.as_view(template_name='company/changePassword.html'), name="forgotPassword"),
    path('password_success/', company_views.password_success, name = "password_success"),
    path('viewCompNotification<int:notification_id>/', company_views.realseenotification, name = "viewCompNotification"),
    path('lauNotification/', laundry_views.viewNotification, name = "lauNotification"),
    path('compNotification/', company_views.viewNotification, name="compNotification"),
    path('editingLauProfile/', laundry_views.changeProfileForm, name="editLauProfile"),
    path('editingCompProfile/', company_views.changeProfileForm, name="editCompProfile"),
    path('comwallet/', TemplateView.as_view(template_name="company/walet.html"), name="comWallet"),
    path('comreceivedOrder/', TemplateView.as_view(template_name="company/r_order.html"), name="com_received_order"),
    path('lauwallet/', TemplateView.as_view(template_name='laundryman/i_walet.html'), name="lauWallet"),
    path('laureceivedOrder/', TemplateView.as_view(template_name='laundryman/r_i_order.html'), name="received_order"),
    path('viewCompanies/', company_views.companiesView, name = "listOfCompanies"),
    path('viewLaundries/', company_views.laundriesView, name = "listOfLaundries"),
    path('option/', TemplateView.as_view(template_name = 'login_as.html'), name="chagua"),
    path('logREST/', views.obtain_auth_token, name = "login"),
    path('loginREST/', RESTfulAPI_views.LoginView.as_view(), name = "login"),
    path('users/', RESTfulAPI_views.UserCreate.as_view(), name="user_create"),
    url(r'^rest-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest6/', include(router.urls)),
    path('rest5/', RESTfulAPI_views.UsingMixinProductList.as_view(), name='usingMixinsAsBoilerPointToReduceCode'),
    path('rest4/', RESTfulAPI_views.ProductList.as_view(), name= 'classBasedAPIView'),
    path('rest3/', RESTfulAPI_views.rest3, name= 'usingRestFramework2'),
    path('rest2/', RESTfulAPI_views.rest2, name= 'usingRestFramework'),
    path('rest/<int:product_id>/', RESTfulAPI_views.rest_cartproduct, name='detail'),
    path('demo2/', TestingRESTAPI.as_view(), name="api_test"),
    url(r'^rest/$', RESTfulAPI_views.rest_cart, name ='api'),
    url(r'^scheduled/$', addtocart_views.scheduled, name="scheduled"),
    path('placedTo/', addtocart_views.placedTo, name = 'whoassigned'),
    path('checkout/', addtocart_views.checkout, name="checkout"),
    path('empty-cart/', EmptyCartView.as_view(), name="emptycart"),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name="managecart"),
    path('mycart/', MyCartView.as_view(), name="mycart"),
    path("realaddedtocart-<int:pro>/", AddedToCart.as_view(), name="realaddtocartbtn"),
    path('awesome/', TemplateView.as_view(template_name = 'product/added2.html'), name='keepmoving'),
    path('addedornot/<title>/', addtocart_views.add_to_cart, name="itemisaddedornot"),
    path('addToCart/<int:pk>/', DemoView.as_view(), name="add_to_cart"),
    path('itemlist/', AddedOrderItems.as_view(), name="itemlist"),
    # hii pattern hapa inakataa ko ni bora utumie path ku-render these additional info in urls
    #    url('r^details/(?P<pk>\d+)/$', CustomDetailView.as_view(), name="details"),
    # this is how we add additional argument in url using the path library
    path('details/<int:pk>', CustomDetailView.as_view(), name="details"),
    # any templateView customized class should contains as_view() method
    path('pricing/<int:migo>/', PricingView.as_view(), name="pricing"),
    url(r'^demo/$', HomeView.as_view(), name="demo"),  
    url(r'^index2/results/$', company_views.search),
    url(r'^results/$', company_views.search, name="searched_list"),
    url(r'^test2/$', TemplateView.as_view(template_name='signup.html'), name="secondEncounteredInterface"), #2
    url(r'index2/$', TemplateView.as_view(template_name = 'option.html'), name="viewLaundersAfterLogin"),   #wafuaji
    url(r'company/profile/$', company_views.profile, name="nolimit"), 
    url(r'company/register/$', company_views.register, name="jisajili"), 
    #url(r'tests/$', company_views.pricing, name="pricing"),
    url(r'viewcompanyprofile/$', CompanyProfileView.as_view(template_name='company/company_profile.html'), name="company_profile"), # hapa inakuja kukaa profile aliyokupa thabiti 
    url(r'viewprofile/$', laundry_views.LaundryProfileView.as_view(template_name='laundryman/individual_profile.html'), name="profile222"),  # Hapa inakuja kukaa profile aliyokupa thabiti
    url(r'test/$', TemplateView.as_view(template_name='laundryman/realprofile.html')),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='localhost'),   # 1
    url(r'customer/login/$', customer_views.customerlogin, name="customer_login"),
    url(r'company/login/$', company_views.companylogin, name="company_login"),
    url(r'laundry/login/$', laundry_views.laundrylogin, name="laundry_login"),
    url(r'laundry/profile/$', laundry_views.profile,  name="profile"),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'laundry/register/$', laundry_views.register),
    url(r'accounts/', include('allauth.urls')), 
    url(r'^customer/demo/$', customer_views.registerDemo),  
    url(r'^customer/signup/$', customer_views.register),
    #url(r'^company/signup/$', company_views.signUp),
    url(r'^company/$', include('laundryManagementSystem.company.urls')),
    url(r'^admin/', admin.site.urls, name="/"),
    url(r'^test0/$', TemplateView.as_view(template_name="font&booteffects.html")),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'), name="password_reset_complete"),

    # this is for hosting on heroku
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
