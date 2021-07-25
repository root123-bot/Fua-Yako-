from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView, View, CreateView 
from .models import Product, Customer, Order, Cart, Post, CartProduct
from django.contrib.auth.models import User
from .forms import ProductQuantityForm, CheckoutForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime, random, string
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json, requests
from django.core import serializers
from django.core.mail import send_mail
from laundryManagementSystem.Payment.models import Payment
# Create your views here.
 
class AddedToCart(TemplateView):
    template_name = 'pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Now let's get the product id from requested url, remember we passed  <int:pro> to help to capture the individual product url from the template through the {% url '-----' product.id }, so these pro keyword in 
        # <int:pro> is the keyword argument or the context variable which is defaulted as dictionary so process the below code to get the id of the individual element/product

        product_id = self.kwargs['pro'] # this pro is the key passed to the url which is rendered in the template as the id of the product 
        print(product_id, '***********************') # this worked as you see in the console there is 7 as id of our product we clicked in template

        
        # then get the product object with that id
        product_obj = Product.objects.get(id=product_id)

        cart_id = self.request.session.get('cart_id', None)
        # Check if cart  exists
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            # this is for items existing in the cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal  += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.customer = self.request.user
                cart_obj.save()
            # new item is added in the cart 
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product= product_obj,
                    quantity = 1, subtotal = product_obj.price
                )
                # After that increase the cart value
                cart_obj.total += product_obj.price
                cart_obj.customer = self.request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total = 0) # Here the total defaulted to 0 since no any cart existing
            self.request.session['cart_id'] = cart_obj.id # Here we create a session for the cart
            # then we need to create the new cart object
            cartproduct = CartProduct.objects.create(
                cart = cart_obj, product = product_obj, 
                quantity = 1, subtotal = product_obj.price
            )
            cart_obj.total += product_obj.price
            cart_obj.customer = self.request.user
            cart_obj.save()
        messages.info(self.request, 'Product has been added to the cart successful')
        print(self.request.user)
        context['product_list'] = Product.objects.all()
        return context

class PricingView(TemplateView):
    template_name = "pricing.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assigned_id = self.kwargs['migo']
        # this above line is used to get the parameter passed to the url <int:migo> its value, this 'migo should be contained to the url processed with this classbasedView that's all '
        print(assigned_id)
        whoisResponsible = User.objects.get(id=assigned_id)
        name = whoisResponsible.username
        print(name)
        # lets create a session to hold this value of the name of the laundry/company assigned the job
        # if request is not contained as parameter in get_context_data() method we should call it by using self as self.request otherwise it will throw an error
        self.request.session['addedTo'] = name
        # order = Order.object.get(id=1)
        # order.assignedTo = name
        # order.save()
        context['product_list'] = Product.objects.all()
        return context 

class AddedOrderItems(ListView):
    model = CartProduct
    template_name = 'product/listsOfAddedItems.html'


# this returns only the individual element given from the list view, so the list view results should be there
class DemoView(DetailView):
    model = CartProduct
    template_name = 'product/add.html'


@login_required(login_url = "laundry/login")
def add_to_cart(request, title):
    item = get_object_or_404(Product, id=id)
    order_item = CartProduct.objects.create(item=item)
    # this is_ordered is False is make sure we only getting the 
    # order/Cart that its not completed
    order_qs = Cart.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the cart
        if order.items.filter(item__slug=item.id).exists():
            order_item.quantity += 1
            order_item.save()
    else:
        order = Order.objects.create(user=request.user)
        order.item.add(order_item)
    return redirect("keepmoving", kwargs={})


def capturingQuantity(request):
    if request.method == 'POST':
        quantity_form = ProductQuantityForm(request.POST)

        if quantity_form.is_valid():
            quantity_form.save()
            quantity = quantity_form.cleaned_data['quantity']
            print(quantity)
        
    else:
        quantity_form = ProductQuantityForm()

    context = {'quantity_form': quantity_form}
    return render(request, 'pricing.html', context) 

class MyCartView(TemplateView):
    template_name = "addtocart/mycart.html"

    def get_context_data(self, **kwargs):
        # this method use the call the  inherited parent method which is get_context_data to take in **kwargs keyword arguments which in this case is the context dictionary data
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        name = self.request.session['addedTo'] # this is the session key containing the name of the compan/laundry assigned the job, so take it in your head the session is created in PricingView above
        # Hizi session mbili hapa juu zina syntax tofauti kumbuka kuwa session ya juu imetumia get() this means yenyewe inatumika ku-capture session zenye GET method, hii ya chini inatumika ku-capture session zotezote, so inabd uzieleweeeee pasco I'm with you
        print(name, '*****************')
        if cart_id:
            # if cart exist then get that cart by using  its id
            cart = Cart.objects.get(id=cart_id)
            # if cart exist then it contains many cartproducts throught their relation view models.py
            # to grab all cartproducts from cart use: cart.cartproduct_set.all query
            starte = cart.arrived_at
            started = starte.strftime("%Y-%m-%d %H:%M") #hapa nilikua najiuliza django nitafanyeje ili nipate format ambayo inahitajika kwenye project yangu ambayo ni Y%M%s H:m ko django yenyewe inatumia hadi am, pm, noon keyword ko inakua ngumu na inakataa nikitaka ni-save kwenye project yangu, ko hapa imenibidi niichukue ile default format ambayo imetumika kwenye tarehe then ni-pass kwenye strftime ili niibadl kwenye string kwa kutumia format inayoitaka
            format = '%Y-%m-%d %H:%M'
            time1 = datetime.datetime.strptime(started, format)
            print(time1, '&&&&&&&&&&&&&&&&&&&')
            ended = cart.finished_at.strftime("%Y-%m-%d %H:%M") # we use strftime  to convert our django dumb date format to our using in our system, this strftime is used to convert django datetime object into the string type object which here we pass our desired datetime format using in our project
            time2 = datetime.datetime.strptime(ended, format) # Here we use the strptime object to convert our string datetime which is output of passing our default assigned django time into the string using the  strftime format I use this kwa kuzan pia hapa itahitajika tu-pass datetime object but imekubali kupass string object so haina shida thanks bro
            print(started, ended, '#######################')
        else:
            cart=None
        context['cart'] = cart
        context['name'] = name
        context['start'] = started
        context['end'] = ended
        return context

class ManageCartView(View):
    # this  below get() function is only used for GET method not POST
    def get(self, request, *args, **kwargs):
        print("This is the managecart section")
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        print(cp_id, action)
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_price = cp_obj.product.price
            cp_obj.subtotal += cp_price
            cp_obj.save()
            cart_obj.total += cp_price
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_price = cp_obj.product.price
            cp_obj.subtotal -= cp_price
            cp_obj.save()
            cart_obj.total -= cp_price
            cart_obj.save()
            if cp_obj.quantity < 1:
                print('empty product so I deleted it')
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('mycart')

class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None) # here we dont put self.request.session.get since the request is already parameter of our get() but if does not exist then there is a need to use self.request
        if cart_id: 
            cart = Cart.objects.get(id=cart_id)
            # then get all cart product associated with cart id above
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('mycart')



def scheduled(request):
    # for any case even if its any form kama gerrard alivyosema inabidi utumie post kwenye form yako once user anavyo-click button ya submit basi ila field uliyoipa name tuna-idaka kwa kutumia post method. reques.POST.get('') shukrani kwa gerrard you are good bro
    if request.method == "POST":
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        radio = request.POST.get('flexRadioDefault', '')
        # create session to send this end date data to the checkout
        request.session['started_at'] = start
        request.session['ending_at'] = end
        
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            print(cart_id)
            cart = Cart.objects.get(id=cart_id)
            datetimeFormat = '%Y-%m-%d %H:%M' # this strptime() method used to convert date in the string and its takes two argument one is datetime objects and another is the format
            delta = datetime.datetime.strptime(end, datetimeFormat) - datetime.datetime.strptime(start, datetimeFormat)
            print(delta, 'This is the delta')
            days = delta.days
            print(days)
            # so to do this all manipulation in django you should first convert the datetime object in string

            if days < 2 or days > 15:
                messages.error(request, 'Duration is either less than 2 or larger than 15, please enter arriving and ending date again')
            else:
                cart.arrived_at = start
                cart.save()
                cart.finished_at = end
                cart.save()
                cart.mode = radio
                cart.save()
                messages.success(request, 'Your information was successful submitted, click the button below to proceed to checkout')
    
        else:
            return None
        print(start)
        print(end)
        print(radio)
    return redirect('mycart')


class CheckoutView(CreateView):
    template_name = 'addtocart/checkout.html' 
    form_class = CheckoutForm
    success_url = reverse_lazy("{% url 'home' %}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        name = self.request.session['addedTo'] # this is the session key containing the name of the compan/laundry assigned the job, so take it in your head the session is created in PricingView above
        # Hizi session mbili hapa juu zina syntax tofauti kumbuka kuwa session ya juu imetumia get() this means yenyewe inatumika ku-capture session zenye GET method, hii ya chini inatumika ku-capture session zotezote, so inabd uzieleweeeee pasco I'm with you

        #started = self.request.session['started_at']
        #ended = self.request.session['ending_at']
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
                
        else:
            cart_obj = None

        context['cart'] = cart_obj # Hii ndo tume-print kwenye our template as total
        context['name'] = name
        context['started'] = started
        # Hizi value mbili tumezi-access kwenye database hapo juu hatujatumia session hapa ko ni vizuri uka-access kwenye db kuliko kutumia session
        context['ended'] = ended
        context['mode'] = mode
        return context




"""
def checkout(request):
    if request.method == 'POST':
        cart_id = request.session.get("cart_id", None)
        name = request.session['addedTo']
        anuani = request.POST.get('address', None)
        namba = request.POST.get('phone', None)
        wilaya = request.POST.get('district', None)
        kito = request.POST.get('ward', None)
        mtaa = request.POST.get('street', None)
        kod = request.POST.get('code', None)
        malipo = request.POST.get('flexRadioDefault', '')
        idNO = "".join(random.choices(string.ascii_uppercase + string.digits, k=25))
        # the 'request.user' is the user object which in most case return username when its called but its a object not username, to get only the usename I will use
        user = User.objects.get(username=request.user.username)
        pepe = user
        mteja = user.username
        #jina = user.ordered_set.get() # this is for returning all order objects with username as BigBoss
        print(pepe)
        if cart_id:
            print(cart_id)
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
            orderObj = Order.objects.create(assignedTo=name, cart=cart_obj, ordered_by=request.user, address=anuani, mobile=namba, email=pepe, order_status="Order received", district=wilaya, ward=kito, street=mtaa, zipcode=kod, orderID=idNO)
            order_id = orderObj.id
            print(str(order_id) + 'This is your order id')
            orderObj.district = wilaya
            print(str(wilaya))
            cart_obj.is_ordered = True
            print(str(cart_obj.is_ordered))
            print("Everything is good *************, then we should delete all sessions")

            ngapi = cart_obj.cartproduct_set.all().count()
            print("There is " + str(ngapi) + "cart products")
            keys = []
            for c in range(ngapi):
                keys.append(c)
            print(str(keys))

            qs = cart_obj.cartproduct_set.all()
            
            hash = dict(zip(keys,qs))
            #json_obj = json.dumps(hash, sort_keys=Trues)
            seliarized_json = serializers.serialize('json', qs)
            print(str(hash))
            
            # create the object of the post so as to post to the required laundryman/company
            postObj = Post.objects.create(
                physical_address = anuani,
                district = wilaya,
                ward = kito,
                contact = namba,
                street = mtaa,
                code =  kod,
                head = "New Job",
                body = "Hey dude you have got a new job here",
                receiver = name,
                mode = cart_obj.mode,
                startDate = started,
                finishDate = ended,
                total = cart_obj.total,
                items = seliarized_json
            )
        

            name_list = []
            quantity_list = []
            json_data = postObj.items
            json_list = eval(json_data)   #this only used to convert json found in string(complex json inside the string) like "[a:{},b:{a:{}}" to list
            noOfElements = len(json_list)
            print(str(noOfElements))
            for no in range(noOfElements):
                prod_id = json_list[no]['fields']['product']
                productObj = Product.objects.get(id=prod_id)
                cartProduct = productObj.cartproduct_set.all()
                for cproduct in cartProduct:
                    name_list.append(cproduct.product.title)
                    quantity_list.append(cproduct.quantity)
            dictOfnameandquantity = dict(zip(name_list, quantity_list))
            print(str(dictOfnameandquantity))

            serialize = json.dumps(dictOfnameandquantity)
            postObj.items = serialize
            postObj.save()
            print(str(postObj.items))

            # then after that let's send the mail to the selected/assigned laundryman/company

            # the name of the  assigned laundryman/company is stored in variable 'name'
            assignedObj = User.objects.get(username=name)
            assignedEmail = assignedObj.email
            print(assignedEmail)
            send_mail(
                'New Job',
                'We would like to inform you have been booked for laundry job, for more information login to your account and navigate to notification bar',
                'mweuc654@gmail.com',
                [assignedEmail],
            )

            del request.session['cart_id']
            del request.session['addedTo']
            return HttpResponseRedirect('index2/')
       
    else:   
        # This means  in case method is not POST, may its request
        cart_id = request.session.get("cart_id", None)
        name = request.session['addedTo']
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
    context = {'cart':cart_obj, 'name':name, 'started':started, 'ended':ended, 'mode':mode}

    return render(request, 'addtocart/checkout.html', context)


"""

def checkout(request):
    if request.method == 'POST':
        cart_id = request.session.get("cart_id", None)
        name = request.session['addedTo']
        anuani = request.POST.get('address', None)
        request.session['anuani'] = anuani
        namba = request.POST.get('phone', None)
        request.session['namba'] = namba
        wilaya = request.POST.get('district', None)
        request.session['wilaya'] = wilaya
        kito = request.POST.get('ward', None)
        request.session['kito'] = kito
        mtaa = request.POST.get('street', None)
        request.session['mtaa'] = mtaa
        kod = request.POST.get('code', None)
        request.session['kod'] = kod
        malipo = request.POST.get('flexRadioDefault', '')
        idNO = "".join(random.choices(string.ascii_uppercase + string.digits, k=25))
        request.session['idNO'] = idNO
        # the 'request.user' is the user object which in most case return username when its called but its a object not username, to get only the usename I will use
        accNo = request.POST.get('pay', None)
        request.session['accNo'] = accNo
        user = User.objects.get(username=request.user.username)
        #seliarized_user = serializers.serialize('json', user)
        request.session['pepe'] = user.email     # this pepe object is not serialized it's from user model
        print(str(user))
        #jina = user.ordered_set.get() # this is for returning all order objects with username as BigBoss
        #print(pepe)
        if cart_id:
            print(cart_id)
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
            
            print("Everything is good *************, then we should delete all sessions")

            # then redirect to the fist thabiti payment page which will contains first forms to change number and last to finish/pay with this number
            return HttpResponseRedirect('/handlingPaymentNumber/')
       
    else:   
        # This means  in case method is not POST, may its request
        cart_id = request.session.get("cart_id", None)
        name = request.session['addedTo']
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
    context = {'cart':cart_obj, 'name':name, 'started':started, 'ended':ended, 'mode':mode}

    return render(request, 'addtocart/checkout.html', context)


"""
def checkout(request):
    if request.method == 'POST':
        cart_id = request.session.get("cart_id", None)
        name = request.session['addedTo']
        anuani = request.POST.get('address', None)
        namba = request.POST.get('phone', None)
        wilaya = request.POST.get('district', None)
        kito = request.POST.get('ward', None)
        mtaa = request.POST.get('street', None)
        kod = request.POST.get('code', None)
        malipo = request.POST.get('flexRadioDefault', '')
        idNO = "".join(random.choices(string.ascii_uppercase + string.digits, k=25))
        accNo = request.POST.get('pay', None)
        # the 'request.user' is the user object which in most case return username when its called but its a object not username, to get only the usename I will use
        user = User.objects.get(username=request.user.username)
        pepe = user
        mteja = user.username
        #jina = user.ordered_set.get() # this is for returning all order objects with username as BigBoss
        print(pepe)
        if cart_id and accNo:
            print(cart_id)
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
            orderObj = Order.objects.create(assignedTo=name, cart=cart_obj, ordered_by=request.user, address=anuani, mobile=namba, email=pepe, order_status="Order received", district=wilaya, ward=kito, street=mtaa, zipcode=kod, orderID=idNO)
            order_id = orderObj.id
            print(str(order_id) + 'This is your order id')
            orderObj.district = wilaya
            print(str(wilaya))
            cart_obj.is_ordered = True
            print(str(cart_obj.is_ordered))
            print("Everything is good *************, then we should delete all sessions")

            ngapi = cart_obj.cartproduct_set.all().count()
            print("There is " + str(ngapi) + "cart products")
            keys = []
            for c in range(ngapi):
                keys.append(c)
            print(str(keys))

            qs = cart_obj.cartproduct_set.all()
            
            hash = dict(zip(keys,qs))
            #json_obj = json.dumps(hash, sort_keys=Trues)
            seliarized_json = serializers.serialize('json', qs)
            print(str(hash))
            # Don't create post object till payment is done
            response = requests.get('http://127.0.0.1:8000/paymentAPI/')
            listOfAccount = []
            indexOfDict = []
            listObj = response.json()
            print(listObj[0]['balance'])
            noOfElements = len(listObj)
            print('no of elements in list objects is '+ str(noOfElements))
            for no in range(noOfElements):
                indexOfDict.append(no)
                accountNo = listObj[no]['account_number']
                listOfAccount.append(accountNo)
            print("This is the index of every dictionary found in this json_list" +str(indexOfDict))
            print("This is the list of all accounts "+str(listOfAccount))
            print("This is the account number you entered " +str(accNo))
            # let's me zip the account and account index list
            accountsXindexDict = dict(zip(indexOfDict, listOfAccount))
            print(str(accountsXindexDict))
            if accNo in listOfAccount:
                # why don't we get account_number associated with it
                print('good its found')

                # this is how to get the key associated with value in dictionary python
                index = 2
                dict_items = accountsXindexDict.items()
                # then value we want to track from our dict is
                val = str(accNo)
                for key,value in dict_items:
                    if value==val:
                        index = key
                print("This is the key associated with a given number where we can use it to access the balance associated with the number " + str(index))

                associatedBalance = listObj[index]['balance']

                print(associatedBalance)
                if associatedBalance < cart_obj.total:
                    print("You are running out of balance, refill your account")
                else:
                    # first minimize the record balance to that required to make order
                    paymentObj = Payment.objects.get(balance=associatedBalance)
                    paymentObj.balance -= associatedBalance
                    paymentObj.save()
                    # then after that it means money has been already submitted, then you should create a post objects 
                            
                    # create the object of the post so as to post to the required laundryman/company
                    postObj = Post.objects.create(
                        physical_address = anuani,
                        district = wilaya,
                        ward = kito,
                        contact = namba,
                        street = mtaa,
                        code =  kod,
                        head = "New Job",
                        body = "Hey dude you have got a new job here",
                        receiver = name,
                        mode = cart_obj.mode,
                        startDate = started,
                        finishDate = ended,
                        total = cart_obj.total,
                        items = seliarized_json
                    )
                

                    name_list = []
                    quantity_list = []
                    json_data = postObj.items
                    json_list = eval(json_data)   #this only used to convert json found in string(complex json inside the string) like "[a:{},b:{a:{}}" to list
                    noOfElements = len(json_list)
                    print(str(noOfElements))
                    for no in range(noOfElements):
                        prod_id = json_list[no]['fields']['product']
                        productObj = Product.objects.get(id=prod_id)
                        cartProduct = productObj.cartproduct_set.all()
                        for cproduct in cartProduct:
                            name_list.append(cproduct.product.title)
                            quantity_list.append(cproduct.quantity)
                    dictOfnameandquantity = dict(zip(name_list, quantity_list))
                    print(str(dictOfnameandquantity))

                    serialize = json.dumps(dictOfnameandquantity)
                    postObj.items = serialize
                    postObj.save()
                    print(str(postObj.items))

                    # then after that let's send the mail to the selected/assigned laundryman/company

                    # the name of the  assigned laundryman/company is stored in variable 'name'
                    assignedObj = User.objects.get(username=name)
                    assignedEmail = assignedObj.email
                    print(assignedEmail)
                    send_mail(
                        'New Job',
                        'We would like to inform you have been booked for laundry job, for more information login to your account and navigate to notification bar',
                        'mweuc654@gmail.com',
                        [assignedEmail],
                    )

                    del request.session['cart_id']
                    del request.session['addedTo']
                    print("You have been successful paid for service, we will")
                    return HttpResponseRedirect('index2/')
            
    else:   
        # This means  in case method is not POST, may its request
        cart_id = request.session.get("cart_id", None)
        name = request.session['addedTo']
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            started = cart_obj.arrived_at
            ended = cart_obj.finished_at
            mode = cart_obj.mode
    context = {'cart':cart_obj, 'name':name, 'started':started, 'ended':ended, 'mode':mode}

    return render(request, 'addtocart/checkout.html', context)

"""


def placedTo(request):
    pass



def succeedPayment(request):
    accNo = request.session['accNo']
    cart_id = request.session.get("cart_id", None)
    if cart_id and accNo:
        cart_obj = Cart.objects.get(id=cart_id)
        ngapi = cart_obj.cartproduct_set.all().count()
        print("There is " + str(ngapi) + "cart products")
        keys =[]
        for c in range(ngapi):
            keys.append(c)
        print(str(keys))
        qs = cart_obj.cartproduct_set.all()
        
        hash = dict(zip(keys,qs))
        #json_obj = json.dumps(hash, sort_keys=Trues)
        seliarized_json = serializers.serialize('json', qs)
        print(str(hash))
        # Don't create post object till payment is done
        response = requests.get('http://127.0.0.1:8000/paymentAPI/')
        listOfAccount = []
        indexOfDict = []
        listObj = response.json()
        print(listObj[0]['balance'])
        noOfElements = len(listObj)
        print('no of elements in list objects is '+ str(noOfElements))
        for no in range(noOfElements):
            indexOfDict.append(no)
            accountNo = listObj[no]['account_number']
            listOfAccount.append(accountNo)
        print("This is the index of every dictionary found in this json_list" +str(indexOfDict))
        print("This is the list of all accounts "+str(listOfAccount))
        print("This is the account number you entered " +str(accNo))
        # let's me zip the account and account index list
        accountsXindexDict = dict(zip(indexOfDict, listOfAccount))
        print(str(accountsXindexDict))
        if str(accNo) in listOfAccount:
            # why don't we get account_number associated with it
            print('good its found')
            # this is how to get the key associated with value in dictionary python
            index = 2
            dict_items = accountsXindexDict.items()
            # then value we want to track from our dict is
            val = str(accNo)
            for key,value in dict_items:
                if value==val:
                    index = key
            print("This is the key associated with a given number where we can use it to access the balance associated with the number " + str(index))
            associatedBalance = listObj[index]['balance']
            print(associatedBalance)
            if associatedBalance < cart_obj.total:
                print("You are running out of balance, refill your account")
            else:
                # first minimize the record balance to that required to make order
                paymentObj = Payment.objects.get(balance=associatedBalance)
                paymentObj.balance -= cart_obj.total
                paymentObj.save()
                # then after that it means money has been already submitted, then you should create a post objects 
                # If everything is good first create order object
                
                # here is where the errors found, **** this is where we get errors I will solve this shit
                #unapendwa = request.session.get['name']
                #request.session['addedTo']
                unapendwa = request.session.get("addedTo", None)   # this gives you the options to return none if the key is not found  

                tryAnother = request.session['addedTo']
                print("This is another way " +str(tryAnother))
                print("this is your name "+str(unapendwa))
                orderObj = Order.objects.create(assignedTo=request.session.get('addedTo', None), cart=cart_obj, ordered_by=request.user, address=request.session.get('anuani', None), mobile=request.session.get('namba', None), email = request.session.get('pepe', None), order_status="Order received", district=request.session.get('wilaya', None), ward=request.session.get('kito', None), street=request.session.get('mtaa', None), zipcode=request.session.get('kod', None), orderID=request.session.get('idNO', None))        
                cart_obj.is_ordered = True
                # create the object of the post so as to post to the required laundryman/company
                postObj = Post.objects.create(
                physical_address = request.session['anuani'],
                district = request.session['wilaya'],
                ward = request.session['kito'],
                contact = request.session['namba'],
                street = request.session['mtaa'],
                code =  request.session['kod'],
                head = "New Job",
                body = "Hey dude you have got a new job here",
                receiver = request.session.get('addedTo', None),
                mode = cart_obj.mode,
                startDate = cart_obj.arrived_at,
                finishDate = cart_obj.finished_at,
                total = cart_obj.total,
                items = seliarized_json
                )

                name_list = []
                quantity_list = []
                json_data = postObj.items
                json_list = eval(json_data)   #this only used to convert json found in string(complex json inside the string) like "[a:{},b:{a:{}}" to list
                noOfElements = len(json_list)
                print(str(noOfElements))
                for no in range(noOfElements):
                    prod_id = json_list[no]['fields']['product']
                    productObj = Product.objects.get(id=prod_id)
                    cartProduct = productObj.cartproduct_set.all()
                    for cproduct in cartProduct:
                        name_list.append(cproduct.product.title)
                        quantity_list.append(cproduct.quantity)
                dictOfnameandquantity = dict(zip(name_list, quantity_list))
                print(str(dictOfnameandquantity))
                serialize = json.dumps(dictOfnameandquantity)
                postObj.items = serialize
                postObj.save()
                print(str(postObj.items))
                # then after that let's send the mail to the selected/assigned laundryman/compan
                # the name of the  assigned laundryman/company is stored in variable 'name'
                assignedObj = User.objects.get(username=request.session.get('addedTo', None))
                assignedEmail = assignedObj.email
                print(assignedEmail)
                send_mail(
                    'New Job',
                    'We would like to inform you have been booked for laundry job, for more information login to your account and navigate to notification bar',
                    'mweuc654@gmail.com',
                    [assignedEmail],
                )

                return HttpResponseRedirect('/confirmed/')
                #del request.session['cart_id']
                #del request.session['addedTo']
    
    else:
        accNo = request.session['accNo']
    
    context = {'accNo': accNo}
    
    # if i'm  not having the enough balance then i will remain on the same page
    return render(request, 'payment/changeno.html', context)