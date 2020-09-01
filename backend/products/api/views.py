from django.http import JsonResponse
import requests
import json
import random
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
#Models
from products.models import products,DeliveryAddress,OrderItem,Order,deliveryPersonelle,OTP
from django.contrib.auth.models import User
#
from rest_framework.generics import ListAPIView, RetrieveAPIView
#Serializer
from .serializers import productSerializer,UserSerializer,DeliveryAddressSerializer,OrderItemSerializer,CustomSerializer,CheckoutCartSerializer
#With Decorators
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework import status
#FOR GENERIC VIEWS
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
#Authentication
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
# This is your real test secret API key.
msg91_key="339801AsT2c6iC5f43fd30P1"
#Custom Authentication
from rest_framework import authentication
from rest_framework import exceptions




class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
##############################################PRODUCT STUFF#################################################################
class productListView(ListAPIView):
    queryset=products.objects.all()
    serializer_class=productSerializer

class productDetailView(RetrieveAPIView):
    queryset=products.objects.all()
    serializer_class=productSerializer


##############################################PRODUCT STUFF#################################################################

class tester( APIView):
    authentication_classes = []

    def post(self, request, format=None):
        print("THE DATA IS",request.data)
        return Response({'received data': request.data})

@api_view(['GET'])
def productCategory(request,**kwargs):
    if request.method=='GET':
        product=products.objects.filter(category__iexact=kwargs['category'],available=True)
        
        serializer=productSerializer(product,many=True,context={'request':request})
        print(kwargs['category'])
        
        return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['GET'])
def productDetail(request,**kwargs):
    if request.method=='GET':
        print("THE FILES ARE",request.FILES)
        try:
            product=products.objects.get(pk=kwargs['pk'],available=True)
        except products.DoesNotExist:
            return Response("Product doesnt exist or not avaialble",status=status.HTTP_404_NOT_FOUND)
        else:
            serializer=productSerializer(product,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)



##############################################SIGNUP STUFF#################################################################
#SIGN UP USING OTP
@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def SignUP_OTP(request,**kwargs):#GET the Number from the request and send OTP
    username=request.data.get("username")
    name=request.data.get("name")
    CurrentUser=User.objects.filter(username=username)
    if(CurrentUser.count()>0):
        return Response("User Already Exist. Please LogIn",status=status.HTTP_409_CONFLICT)
    else:
        print(CurrentUser.count())
        otp=random.randint(1000,9999)
        print("THE OTP IS",otp)
        CurrentUserOTP,created=OTP.objects.get_or_create(username=username)
        CurrentUserOTP.otp=otp
        CurrentUserOTP.name=name
        CurrentUserOTP.save()
        Send_OTP(username,otp)
        return Response(f"OTP SENT TO {username}")

@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def signup_OTP_verify(request,**kwargs):#get the OTP from the user and then Check if they are the same
    userOTP=int(request.data.get("OTP"))
    username=request.data.get("username")
    CurrentUserOTP=OTP.objects.get(username=username)
    print("OTP is",userOTP,type(userOTP))
    print("Saved OTP is",CurrentUserOTP.otp,type(CurrentUserOTP.otp))
    verified=confirm_OTP(CurrentUserOTP.otp,userOTP)
    if (verified):
        #Create the user
        CurrentUser=User.objects.create_user(username=username,first_name=CurrentUserOTP.name)
        token=Token.objects.create(user=CurrentUser)
        CurrentUserOTP.delete()
        return Response({'key':token.key,"name":CurrentUser.first_name},status=status.HTTP_201_CREATED)
    else:
        return Response("Wrong OTP.Try again.",status=status.HTTP_400_BAD_REQUEST)
    


def confirm_OTP(actual_OTP,user_OTP):#Check if two OTP are same
    if(actual_OTP==user_OTP):
        return True
    else:
        return False


#For the deafault Django user
class SignUpUserView(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin
                        ,mixins.CreateModelMixin):

    
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
                        
    serializer_class=UserSerializer
    queryset=User.objects.all()

    def get(self,request,id=0):
        print("request",request)
        print("data",request.data)
       
        #HTTP_AUTHORIZATION': 'Token 027fa96b46619922b649ee5fb367a4ee58daca50', 'HTTP_PASSWORD': 'gogetadragon'
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request,id=0):
        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():
            print("INFOPOST",request.data)
            print(request)
            print(dir(request))
            print(request.data)
            print(request._user)
            user=User.objects.create_user(username=request.data.get("username"))
            token=Token.objects.create(user=user)
            return Response({'key':token.key,"name":user.first_name},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




def Send_OTP(number,otp):
    message=f"Hi,{otp} is your verification code. Thanks for using 10DerMeatz. Please use this to confirm your account."
    payload = {
                "sender": "SOCKET",
                "route": "4",
                "country": "91",
                "unicode": "1",
                "sms": [
                    {
                    "message": message,
                    "to": [
                        number
                    ]
                    }
                ]
                }

    headers = {
        'authkey': msg91_key,
        'content-type': "application/json"
        }
    x=requests.post("https://api.msg91.com/api/v2/sendsms",headers=headers,json=payload)
        
    print(x.content)
    print(message)
    



    

##############################################SIGNUP STUFF#################################################################
























##############################################LOGIN STUFF#################################################################
#For Login. Send USername and password in body. return token and other stuff
@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def Login_OTP(request,**kwargs):#get the OTP from the user and then Check if they are the same
     
     try:
        username=request.data.get("username")
        CurrentUser=User.objects.get(username=username)
     except:
        return Response("User Not Found.",status=status.HTTP_400_BAD_REQUEST)
     else:
        otp=random.randint(1000,9999)
        CurrentUserOTP,created=OTP.objects.get_or_create(username=username)
        CurrentUserOTP.otp=otp
        CurrentUserOTP.save()
        Send_OTP(username,otp)
        return Response(f"OTP sent to {username}")
   
    
@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def Login_OTP_verify(request,**kwargs):#get the OTP from the user and then Check if they are the same
    
    userOTP=int(request.data.get("OTP")) #OTP entered by the user
   
    username=request.data.get("username") #Username entered by the user
    try:
        CurrentUserOTP=OTP.objects.get(username=username)#Get the OTP stored in the backend
    except OTP.DoesNotExist:
        return Response("OTP Does Not Exist. TRY Resending an OTP.",status=status.HTTP_400_BAD_REQUEST)
    else:
        verified=confirm_OTP(CurrentUserOTP.otp,userOTP)
        if (verified):
            print("Verified")
            #Login the user 
            CurrentUser=User.objects.get(username=username)
            print("CURRENT USWR IS THERE")
            token=Token.objects.get(user=CurrentUser)
            print("CURRENT TOKEN IS THERE")
            CurrentUserOTP.delete()
            return Response({'key':token.key,"name":CurrentUser.first_name},status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Wrong OTP.Try again.",status=status.HTTP_400_BAD_REQUEST)
    




class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print("USER US",user)

        return Response({
            'key': token.key,
            'user_id': user.pk,
            'name':user.first_name
        })


##############################################SIGNUP STUFF#################################################################





























##############################################DELIVERY ADDRESS STUFF#################################################################
# Delivery Address
@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Delivery_Address_View(request,pk):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    token=request.META.get('HTTP_AUTHORIZATION').split()[-1] #Get the token from header
    CurrentUser=Token.objects.get(key=token).user  #Get the user from the token
    CurrentUserDeliveryAddresses=DeliveryAddress.objects.filter(user=CurrentUser) #current user Addresses. If none it returns an empty QuerySet.
   

    if request.method=='GET': # get one users Delivery Addresses and return the data as Json 

        serializer=DeliveryAddressSerializer(CurrentUserDeliveryAddresses,many=True) #Serialize a query set
        return Response(serializer.data)

    elif request.method=='POST':#get the data and if valid save as Json
        
        #Create a new deliveryAdrees for the currrent user
        newDeliveryAddress=DeliveryAddress.objects.create(user=CurrentUser,
                                                        tag=request.data.get('tag'),
                                                        address=request.data.get('address'),
                                                        landmark=request.data.get('landmark'),
                                                        houseNumber=request.data.get('houseNumber'),
                                                        addInfo=request.data.get('addInfo'),
                                                        lat=request.data.get('lat'),
                                                        lng=request.data.get('lng'))
        
        serializer=DeliveryAddressSerializer(newDeliveryAddress) #Serialize The new object into Json and send it as a response
        print("NEW USER PRO CREATED",serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    elif request.method=='PUT': #Get the list in the frontend. Send the pk of the address to update.
        try:
            UserDeliveryAddressesUpdate=CurrentUserDeliveryAddresses[pk]
        except IndexError: #Check if the address exists
            print("The Address doesnt exist")
            return Response("Address Doesnt Exist",status=status.HTTP_204_NO_CONTENT)
        else:
            print("THE CURRENT Address",UserDeliveryAddressesUpdate.id)
            UserDeliveryAddressesUpdate.tag=request.data.get('tag')
            UserDeliveryAddressesUpdate.address=request.data.get('address')
            UserDeliveryAddressesUpdate.landmark=request.data.get('landmark')
            UserDeliveryAddressesUpdate.houseNumber=request.data.get('houseNumber')
            UserDeliveryAddressesUpdate.addInfo=request.data.get('addInfo')
            UserDeliveryAddressesUpdate.save()
            return Response("UPDATED",status=status.HTTP_200_OK)

    elif request.method=='DELETE':
        try:
            UserDeliveryAddressesDelete=CurrentUserDeliveryAddresses[pk]
        except IndexError: #Check if the address exists
            print("The Address doesnt exist")
            return Response("Address Doesnt Exist",status=status.HTTP_204_NO_CONTENT)
        UserDeliveryAddressesDelete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Select Delivery Address
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Delivery_Address_Select_View(request,pk):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    print("THE SELECTIN TOKEN IS",request.META.get('HTTP_AUTHORIZATION'))
    token=request.META.get('HTTP_AUTHORIZATION').split()[-1] #Get the token from header
    CurrentUser=Token.objects.get(key=token).user  #Get the user from the token
    CurrentUserDeliveryAddresses=DeliveryAddress.objects.filter(user=CurrentUser) #current user Addresses. If none it returns an empty QuerySet.
    CurrentUserOrder=Order.objects.get(user=CurrentUser) #Get the cuurent user order

    if request.method=='POST':#get the data and if valid save as Json
        print("DARA",request.data,type(request.data))
        add=CurrentUserDeliveryAddresses[pk]
        CurrentUserOrder.deliveryAddress=add
        CurrentUserOrder.save()
        serializer=DeliveryAddressSerializer(add) #Serialize The new object into Json and send it as a response


        return Response(serializer.data,status=status.HTTP_201_CREATED)


##############################################DELIVERY ADDRESS STUFF#################################################################


















































##############################################ORDER ITEM STUFF#################################################################

@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def OrderItem_View(request,pk):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    token=request.META.get('HTTP_AUTHORIZATION').split()[-1] #Get the token from header
    try:
        CurrentUser=Token.objects.get(key=token).user  #Get the user from the token
    except Token.DoesNotExist:
        return Response("User Does Not Exist",status=status.HTTP_400_BAD_REQUEST)

    print("USER=",CurrentUser)
    CurrentUserOrderItems=OrderItem.objects.filter(user=CurrentUser) #current user Addresses. If none it returns an empty QuerySet.
    print("THE FUCNTIONS STUFF",CurrentUserOrderItems)
   

    if request.method=='GET': # get one users order items and diaplay the data as Json 
        serializer=CustomSerializer(CurrentUserOrderItems,many=True)
        return Response(serializer.data)

    elif request.method=='POST':#POST the data and if valid save as Json
        items=request.data
        newOrderitems=[]
        order,created=Order.objects.get_or_create(user=CurrentUser) #Get a tuple (order object,Boolean of created or not)
        for item in items:
            #Create a new Order Item for the currrent user
            newOrderItem=OrderItem.objects.create(user=CurrentUser,
                                                product=products.objects.get(title=item['title']),
                                                quantity=float(item['quantity']),
                                                weight=float(item['weight']),
                                                )
            newOrderitems.append(newOrderItem)
            order.items.add(newOrderItem)#Add the item into the order for the user
        serializer=CustomSerializer(newOrderitems,many=True) #Serialize The new object into Json and send it as a response
        

        # product=products.objects.get(title=request.data.get('title'))
        # #Create a new Order Item for the currrent user
        # newOrderItem=OrderItem.objects.create(user=CurrentUser,
        #                                     product=product,
        #                                     quantity=request.data.get('quantity'),
        #                                     weight=request.data.get('weight'),
        #                                     )
        # #Add the item into the order for the user
        # order,created=Order.objects.get_or_create(user=CurrentUser) #Get a tuple (order object,Boolean of created or not)
        # order.items.add(newOrderItem)
        # serializer=OrderItemSerializer(newOrderItem) #Serialize The new object into Json and send it as a response
        # print("NEW USER PRO CREATED",serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    elif request.method=='PUT': #Get the list in the frontend. Send the pk of the address to update.
        try:
            OrderItemUpdate=CurrentUserOrderItems[pk]
        except IndexError: #Check if the orderItem exists
            print("The Item doesnt exist")
            return Response("Item Doesnt Exist",status=status.HTTP_204_NO_CONTENT)
        else:
            print("THE CURRENT OrderItem",OrderItemUpdate.id)
            OrderItemUpdate.quantity=request.data.get('quantity')
            OrderItemUpdate.save()
            serializer=OrderItemSerializer(OrderItemUpdate)
            return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method=='DELETE':
        try:
            OrderItemDelete=CurrentUserOrderItems[pk]
        except IndexError: #Check if the OrderItem exists
            if(pk==999):
                CurrentUserOrderItems.delete()#Delete everything 
                return Response("ITEMS HAVE BEEN DELETED",status=status.HTTP_204_NO_CONTENT)
            return Response("Items not found",status=status.HTTP_400_BAD_REQUEST)
        else:
            OrderItemDelete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

##############################################ORDER ITEM STUFF#################################################################
























##############################################STRIPE STUFF#################################################################
def calculate_order_amount(amount):
    #Take in ruppes and return paisa
    return (amount*100)

@api_view(['POST'])
def create_payment(request):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    token=request.META.get('HTTP_AUTHORIZATION').split()[-1] #Get the token from header
    CurrentUser=Token.objects.get(key=token).user  #Get the user from the token
    CurrentOrder=Order.objects.get(user=CurrentUser)
    print("STRIPE GOT CURRENTORDER")
    print("IT IS  APOSTS BICHHH",request.data)
    try:
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(CurrentOrder.total),#CurrentOrder.total,
            currency='inr'
        )
        return Response({
        'clientSecret': intent['client_secret']
    })
    except Exception as e:
        return Response("error="+str(e),status=status.HTTP_403_FORBIDDEN)
    else:
        return Response("Success",status=status.HTTP_202_ACCEPTED)




@api_view(['POST'])
def my_webhook_view(request):
  print("WEBHOOK",request.method)  
  
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  try:
    event = stripe.Event.construct_from(
      json.loads(payload),sig_header ,stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return Response(status=status.HTTP_400_BAD_REQUEST)

  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return Response(status=status.HTTP_400_BAD_REQUEST)

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    print('PaymentIntent was successful!')
  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    print('PaymentMethod was attached to a Customer!')
  # ... handle other event types
  else:
    # Unexpected event type
    return Response(status=status.HTTP_400_BAD_REQUEST)

  return Response(status=status.HTTP_200_OK)
##############################################STRIPE STUFF#################################################################




















##############################################ORDER STUFF#################################################################
#To get the total for the order
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_checkout_cart(request):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    try:
        token=request.META.get('HTTP_AUTHORIZATION').split()[-1] #Get the token from header
        CurrentUser=Token.objects.get(key=token).user  #Get the user from the token
        CurrentUserOrderItems=OrderItem.objects.filter(user=CurrentUser) #current user Addresses. If none it returns an empty QuerySet.
    except Token.DoesNotExist:
        return Response("Access Denied",status=status.HTTP_400_BAD_REQUEST)
    
    else:
        try:
            serializer=CustomSerializer(CurrentUserOrderItems,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except AttributeError:
            return Response([],status=status.HTTP_200_OK)


##############################################ORDER STUFF#################################################################






















    




##############################################MSG91 STUFF#################################################################
@api_view(['POST'])
def send_message_view(request,**kwargs):
    account_sid = 'AC16f349e20bad6a918c3a9be4f3c15839'
    auth_token = '2b5a0649fb1974fdd3ffb9716287a6d5'
    print(kwargs)
    deliveryPerson=deliveryPersonelle.objects.get(pk=kwargs['deliveryPersonelleID'])
    order=Order.objects.get(pk=kwargs['orderID'])
    body=f"Order Number:{(kwargs['orderID'])} \n"
    body+=f"ADDRESS:{(order.deliveryAddress.address)} \n"
    body+=f"HOUSE/FLAT NO.:{(order.deliveryAddress.houseNumber)} \n"
    body+=f"LANDMARK:{(order.deliveryAddress.landmark)} \n"
    body+=f"ADDITIONAL INFO:{(order.deliveryAddress.addInfo)} \n"
    body+=f"Location: https://maps.google.com/?q={order.deliveryAddress.lat},{order.deliveryAddress.lng}"
    
    payload = {
                "sender": "SOCKET",
                "route": "4",
                "country": "91",
                "unicode": "1",
                "sms": [
                    {
                    "message": body,
                    "to": [
                        deliveryPerson.number
                    ]
                    }
                ]
                }
    headers = {
        'authkey': msg91_key,
        'content-type': "application/json"
        }
    x=requests.post("https://api.msg91.com/api/v2/sendsms",headers=headers,json=payload)
    print("BODY",body)
    print(x.content)
    
    return HttpResponseRedirect('/admin/products/order/'+str(kwargs['orderID'])+'/change/')



##############################################MSG91 STUFF#################################################################


