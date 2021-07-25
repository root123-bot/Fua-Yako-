from django.shortcuts import render
import requests
import  json
from django.http import HttpResponseRedirect
# Create your views here.
def get_jsonResponse(request):
    response = requests.get('http://127.0.0.1:8000/paymentAPI/')

    listOfAccount = []
    print(response)
    response_json = response.json() # this changes our results in url to json to access data
    amount = response_json[0]['balance']
    print(amount)

    listObj = response_json # eval passed should be string/bytes/code
    noOfElements = len(listObj)
    print(str(noOfElements))

    for no in range(noOfElements):
        accountNo = listObj[no]['account_number']
        print(str(accountNo))
        listOfAccount.append(accountNo)
        
    # then this listOfAccount will have a list of accountNo

    print(str(listOfAccount))

    # then check if the account number/phone number entered by user found inside the list

    accNo = request.POST.get('number', None)

    if accNo in listOfAccount:
        print('good its found')
        # then get the account balance associated with this account number
        itsIndex = listObj.index(accNo)
        print(str(itsIndex))

        parentIndex = listObj.index(itsIndex)
        print(str(parentIndex))

        # if we get parentIndex which is 0, 1, 2 then get the associated balance

        associatedBalance = listObj[parentIndex]['balance']

        print(associatedBalance)
        return HttpResponseRedirect('/')
    
    else:
        print('phone number not found')


    context = {}
    return render(request, 'payment/pay_page.html',context)




def handlingPaymentNumber(request):
    # this method will be used to change the payment number  if user want so
    accNo = request.session['accNo']
    if request.method == 'POST':
        # from that page of pay_page.html we should capture what user post
        card_no = request.POST.get('changeNo', None)
        
        # then if we capture that user entered number then we should change our session of  number to be of another

        request.session['accNo'] = card_no
        accNo = request.session['accNo']
        # after changing that we should redirect the user to the same page but the accNo should be updated
        print("This is the value of accNo at post "+ str(accNo))
        #there is no need to redirect since we want to be redirected to the same page, so no need to redirect and this way is good for that scenario
        #return HttpResponseRedirect('handlingPaymentNumber/')
    else:
        accNo = request.session['accNo']
        print(str(accNo))
    print(str(accNo))
    context = {'accNo': accNo}
    return render(request, 'payment/changeno.html', context)


"""
def updated(request):
    if request.method == 'GET':
        accNo = request.GET.get('number', None)
        return HttpResponseRedirect('updatedPhone/')
    else:
        accNo = '0784434323'
    context = {'accNo':accNo}
    return render(request, 'payment/pay_page.html', context)
"""


"""
def handlingPaymentNumber(request):
    if request.method == 'POST':
        accNo = request.POST.get('pay', None)
        if accNo:
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
                        
"""