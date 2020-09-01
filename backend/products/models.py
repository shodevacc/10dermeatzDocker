from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete,m2m_changed,pre_delete
from rest_framework.authtoken.models import Token
import math
category_choices=(('poultry','POULTRY'),
                    ('mutton','MUTTON'),
                    ('seafood','SEAFOOD')
                    )

# Create your models here.

class products(models.Model):
        
        img=models.ImageField(upload_to='Product_Images')
        title=models.CharField(max_length=50,null=False)
        sub_title=models.CharField(max_length=40,default=None)
        Small_description=models.CharField(max_length=200)
        large_description=models.CharField(max_length=500)
        price=models.FloatField(null=False)
        available=models.BooleanField(default=True)
        category=models.CharField(max_length=15,choices=category_choices,default='ADD SOON')
        

        def get_img_url(self):
            return self.img.url

        def __str__(self):
            return self.title

        def search(self,string):
            print(string)

        
class DeliveryAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    tag=models.CharField(max_length=25,default="My Address")
    address=models.CharField(max_length=200,null=True,blank=True)
    landmark=models.CharField(max_length=100,null=True,blank=True)
    houseNumber=models.CharField(max_length=100,null=True,blank=True)
    addInfo=models.CharField(max_length=100,null=True,blank=True)
    lat=models.CharField(max_length=30,null=True,blank=True)
    lng=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.tag


class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE,blank=True,related_name='products')
    quantity=models.FloatField(default=1)
    weight=models.FloatField(default=500)
    price=models.FloatField(default=0)
    date_added=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.price=self.quantity*(self.weight*self.product.price/1000)
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"Item:{self.product.title} Quantity:{self.quantity} weight:{self.weight} price:{self.price} \n\n"

class deliveryPersonelle(models.Model):
    number=models.CharField(max_length=10)
    name=models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Order(models.Model):
    deliveryAddress=models.OneToOneField(DeliveryAddress,on_delete=models.SET_NULL,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    delivery_Personelle=models.OneToOneField(deliveryPersonelle,on_delete=models.SET_NULL,null=True)
    items=models.ManyToManyField(OrderItem)
    completed=models.BooleanField(default=False)
    date_added=models.DateTimeField(auto_now_add=True)
    total=models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return self.user.username



class OTP(models.Model):
    username=models.CharField(max_length=15)
    name=models.CharField(max_length=40,null=True,blank=True)
    otp=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.username

def deleteOrder(sender,instance,**kwargs):
    instance.items.all().delete()


def OrderItemChanged(sender,instance,**kwargs):
    print("KWARGS IN CHANGED",kwargs)
    if kwargs['action']=='post_remove' or kwargs['action']=='post_add':
       updateTotal(instance)
       

def updateTotal(order):
    total=0.0
    for i in order.items.all():
        total+=i.price
    order.total=math.ceil(total)
    order.save()


def saveOrder(sender,instance,**kwargs):
    try:
        order=Order.objects.get(user=instance.user)
    except Order.DoesNotExist:
        pass
    else:
        updateTotal(order)
        

pre_delete.connect(deleteOrder,sender=Order) #Before you delete the order delete all items associated with it
post_save.connect(saveOrder,sender=OrderItem)#After saving an Orderitem update the order total
post_delete.connect(saveOrder,sender=OrderItem)#After deleting an OrderItem update the total
m2m_changed.connect(OrderItemChanged,sender=Order.items.through)#IF an item has been added or removed to my order, update the total


class CaoruselImages(models.Model):
    CaoruselImage=models.ImageField(upload_to="Carousel_Images")

    def get_img_url(self):
            return self.CaoruselImage.url

    def __str__(self):
        return f'Caorusel Image {self.id}'

        
class CategoryInfo(models.Model):
    CategoryImages=models.ImageField(upload_to="Category_Images")
    category=models.CharField(max_length=15,choices=category_choices,default='ADD SOON')
    categoryInfo=models.CharField(max_length=200,default='ADDING DESCRIPTION SOON')

    def get_img_url(self):
        return self.CategoryImages.url

    def __str__(self):
        return f'Category {self.category}'