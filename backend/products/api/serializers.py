from rest_framework import serializers
from products.models import products,DeliveryAddress,OrderItem,Order
from django.contrib.auth.models import User


#A way to convert to and from Json 
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer): #Built in dajngo model
    class Meta:
        model=User
        fields=('username','email','first_name','password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeliveryAddress
        fields=('id','tag','address','landmark','houseNumber','addInfo')
  
#for the orderItems
class CustomSerializer(serializers.Serializer):
    product=productSerializer()
    quantity=serializers.FloatField()
    weight=serializers.FloatField()
    price=serializers.FloatField()
    

    def create(self, validated_data): #To create an object with the validated data
        print("THE VALIDATED DATA IS",validated_data)
        return 

#For the final order
class CheckoutCartSerializer(serializers.Serializer):
    items=CustomSerializer()
    total=serializers.FloatField()