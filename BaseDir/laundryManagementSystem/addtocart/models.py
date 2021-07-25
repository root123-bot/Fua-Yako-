from django.db import models
from ..customer.models import UserProfile0
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
import random
#from django.contrib.postgres.fields.jsonb import JSONField
import string  
from jsonfield import JSONField
 
delta = timedelta(days=2)
finished_time = datetime.datetime.now() + delta

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(UserProfile0, on_delete=models.CASCADE)


    def __str__(self):
        return user.user

class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.PositiveIntegerField()
    quantity = models.IntegerField(default=1)
 
    def __str__(self):
        return self.title



         
# If I set null=True and blank=True here on the cart it means there
# is no login required to create a cart
class Cart(models.Model):
    # on naming use _ like ref_no not - like ref-no it will
    # throw syntax error
    #ref_no = models.CharField(max_length=200)

    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    arrived_at = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    finished_at = models.DateTimeField(default=finished_time, null=True, blank=True)
    options = (
        ("Pick at station", "Pick at station"),
        ("Door step pickup", "Door step pickup"),
    )
    mode = models.CharField(max_length=100, choices=options, blank=True, null=True, default="Pick at station")
  
 

class CartProduct(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    def __str__(self):
        return self.product.title

ORDER_STATUS = (
    ("Order received", "Order received"),
    ("On pending","On pending"),
    ("Order processed", "Order processed"),
    ("Completed", "Completed"),
    ("On delivery", "On delivery"),
    ("Order cancelled", "Order cancelled"),
)



location = (
    ('Ilala', 'Ilala'),
    ('Kinondoni', 'Kinondoni'),
    ('Temeke', 'Temeke'),
    ('Ubungo', 'Ubungo'),
    ('Kigamboni', 'Kigamboni')
)
class Order(models.Model):
    assignedTo = models.CharField(max_length=200, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.ForeignKey(User, related_name = 'ordered_set', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.PositiveIntegerField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    district = models.CharField(max_length=200, choices = location, null=True, blank=True)
    ward = models.CharField(max_length = 200, null=True, blank=True)
    street = models.CharField(max_length = 200, null=True, blank=True)
    zipcode = models.PositiveIntegerField(null=True, blank=True)
    orderID = models.CharField(max_length=25, null=True, blank=True)
    def __str__(self):
        return "Order: "+str(self.id)



class Post(models.Model):
    head = models.CharField(max_length=50)
    body = models.CharField(max_length=200)
    sender = models.CharField(max_length=30, default="admin", null=True, blank=True)
    receiver = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    contact = models.IntegerField(null=True, blank = True)
    code = models.IntegerField(null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    physical_address = models.CharField(max_length=200, null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    finishDate = models.DateTimeField(null=True, blank=True)
    items = JSONField(null=True, blank=True)
    quantity = models.CharField(max_length=100, null=True, blank=True)
    mode = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        when = self.created_at.strftime("%Y-%m-%d %H:%M")
        return "Its created at: "+ when
