from .models import Product, Order
from django import forms


class ProductQuantityForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['district', 'mobile', 'address', 'ward', 'street','zipcode']