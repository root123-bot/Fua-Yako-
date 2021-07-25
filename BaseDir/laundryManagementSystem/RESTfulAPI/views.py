from django.shortcuts import render
from django.http import HttpResponse
from laundryManagementSystem.addtocart.models  import CartProduct, Product
import json
from django.core import serializers
from .serializers import ProductSerializer, AllFieldsProductSerializers, UserSerializer, ReturnAllPaymentRecordsFieldsSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from laundryManagementSystem.Payment.models import Payment

# REMEMBER THE REST SERVICE END POINT (is the url loaded to browser)
# ( To implement security the rest api use key, also its you to 
# decide either to give the api sensitive action like Update(UPT) 
# and delete(DELETE)
#) This delete and update are sensitive operation so if you dont have
# secrete key to implement security and exposing points(url)- open to the public 
#may provide insecurity

# Create your views here.
def rest_cart(request):
    product_list = CartProduct.objects.all()
    product_names = [{"name": pro.product.title} for pro in product_list]
    return HttpResponse(json.dumps(product_names), content_type = 'application/json')

def rest_cartproduct(request, product_id = None):
    product_list = CartProduct.objects.all()
    if product_id:
        product_list = product_list.filter(id=product_id)
    if 'type' in request.GET and request.GET['xml'] == 'xml':
        serialized_product = serializers.serialize('xml', product_list)
        return HttpResponse(serialized_product, content_type='application/xml')
    else:
        serialized_product = serializers.serialize('json', product_list)
        return HttpResponse(serialized_product, content_type='application/json')

@api_view(['GET', 'POST', 'DELETE'])
def rest2(request):
    if request.method  == 'GET':
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


@api_view(['GET', 'POST', 'DELETE'])
def rest3(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializers = AllFieldsProductSerializers(products, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

# In django restful framework there is the class based view
# which simplifies the work of using the @api_view decorators
# in method above, the one of class based view is APIView class

class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass


# lets try to reduce the couple of the lines, since coding
# especially in python follow DRY principle, this can 
# be achieved by using class based view mixins, here we 
# use ListCreateAPIView is the REST view to generate a list
# based on the queryset(this is required), also this view 
# need the required serializer_class option that point to the 
# serializer class or others


# This generic class view below using mixins is pretty powerful for just
# three lines, but its just tone class to display a list of Product
# records
class UsingMixinProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = AllFieldsProductSerializers


 ################# View Sets and Routers ####################
# This generic class view above using mixins is pretty powerful for just
# three lines, but its just tone class to display a list of Product
# records. Let's assume u now need to create a REST service to display
# a specific Product record, another ret service to update a Product
# record, and ye t another rest service to delete store records. In
# this scenario, you would need to create a three more generic class
# views and three more URL mappings to roll out this basic CRUD
# functionality. But instead of creating separate view classes for 
# each case, you can instead rely on a Django rest framework 'view set'
# as name implies 'django view sets' is the group of views. To create
# django rest  framework view sets all you need to do is create class
# that inherits its behaviour from one of the django rest framework's
# classes intended for this purpose.  Code below illustrates a view set
# created with the ModelViewSet class
# Yaani hapa hii class ya view set itakua na view karibu zote kwa
# kupitia class hii like ku-delete, create, read and etc

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AllFieldsProductSerializers

# This above class is the View set. But this view set is incomplete
# we should give it the urls to access views contained on it, Using
# this class alone, a rest service is automaticallly hooked up to 
# display a store record list, as well as to create, read, update or
#  delete individual store records .
# Because a view set generates multiple views, you are still left
# with the issue of configuring each view to a url, in which case
# the easiest path is to use a Django REST framework router. A 
# router is to view set what a url statement is to class-based-view
# (Yaani hii router ni sawa to url statement katika class based view)
# a way to hook up an end point( Jinsi ya kuifikia destinatioin)
# Code on url.py describe setup with django rest framework router.





class UserCreate(generics.CreateAPIView):
    # this create api view is used to create json data and populate in model
    # so its does not need queryset, to create it use the method POSTS
    # so this is the api for posting data to the model or database

    #authentication_classes = () # Hii inatumika kuiondolea hii authentication so you can access this class with no need of authentication
    #permission_classes = () # Hii Pia inaiondolea hata kama hauna permission yoyote unaweza ukaaccess hii 
    # these serializer classes is only used for the queryset, used to convert queryset into json data types
    # for normal dictionary or data use json.dumps() method to do so, TAKE THAT OTHERWISE YOU WILL GET AN ERROR.
    serializer_class = UserSerializer

class LoginView(APIView):
    permissioni_classes = ()

    def post(self, request,):
        usename = request.data.get("username")
        password = request.data.get("password")   
        user = authenticate(usename=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong credentials"}, status =status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'DELETE'])
def payment(request):
    if request.method == 'GET':
        pays = Payment.objects.all()
        serializers = ReturnAllPaymentRecordsFieldsSerializers(pays, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
