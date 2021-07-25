from rest_framework import serializers
from laundryManagementSystem.addtocart.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from laundryManagementSystem.Payment.models import Payment
class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    price = serializers.IntegerField()

class AllFieldsProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class ReturnAllPaymentRecordsFieldsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
# Here we try to customize the authenticate user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # I think this is used to limit only write only(to write the password) in django rest framework
    
    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user) # this is used to ensure token are created when user is created in UserCreate view
        return user