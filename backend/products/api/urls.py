from django.urls import path
from .views import *

urlpatterns=[
    path('productcategorylist/<slug:category>',productCategory,name="productlist"),#ProductCatrogry
    path('',productListView.as_view()),
    path('<pk>',productDetail),
    path('signup/',SignUpUserView.as_view(),name='signup'), #Built in Django model. Make Post requests.
    path('signupaddress/<int:pk>',Delivery_Address_View,name="signupprofile"), #For the delivery address
    path('selectaddress/<int:pk>',Delivery_Address_Select_View,name="signupprofile"), #Select the delivery address
    path('login/', CustomAuthToken.as_view(),name="gettoken"), #To login will return a token
    path('orderitem/<int:pk>', OrderItem_View,name="orderitem"),
    path('create-payment-intent/',create_payment,name="create payment"),
    path('checkout/',get_checkout_cart,name="checkout"),
    path('sendmessage/<int:orderID>/<int:deliveryPersonelleID>/',send_message_view,name="send message"),
   #OTP VERIFICATION
    path('signup_OTP_verify/',signup_OTP_verify,name="Verify"),#second
    path('signupOTP/',SignUP_OTP,name="OTP"),#First
    path('loginOTP/',Login_OTP,name="Login"),#First
    #path('loginOTP/',tester.as_view(),name="Login"),#First
    path('login_OTP_verify/',Login_OTP_verify,name="LoginVerify"),#second
    path('webhook/',my_webhook_view,name="my_webhook_view")

]


