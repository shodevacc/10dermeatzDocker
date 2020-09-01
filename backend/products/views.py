from django.shortcuts import render
from .models import products,CaoruselImages 
from django.conf import settings


# Create your views here.
def home_view(request):
    
    context={'carousel':CaoruselImages.objects.all()}
    return render(request,'pages/home.html',context)

def category_view(request,*args,**kwargs):
    items=products.objects.filter(category=kwargs['category'],available=True)
    print("request",request.user)
    print("args",args)
    print("kwargs",kwargs)
    context={'category':kwargs['category'],'items':items}
    return render(request,'pages/category.html',context)

def product_detail_view(request,*args,**kwargs):
    item=products.objects.get(id=kwargs['id'])
    print("request",request.user)
    print("args",args)
    print("kwargs",kwargs)
    context={'id':kwargs['id'],'item':item}
    return render(request,'pages/ProductDetail.html',context)

def checkout_view(request,*args,**kwargs):
    
    print("request",request.user)
    print("args",args)
    print("kwargs",kwargs)
    context={}
    return render(request,'pages/checkout.html',context)

def payment_view(request):
    context={'stripe':stripe}
    return render(request,'pages/payment.html',context)

def payment_success_view(request):
    context={}
    return render(request,'pages/payment_success.html',context)

def payment_fail_view(request):
    context={}
    return render(request,'pages/payment_fail.html',context)