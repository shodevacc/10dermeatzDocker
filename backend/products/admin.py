from django.contrib import admin
from django import forms
from django.urls import path
from django.contrib.auth.models import Group
from .models import products,DeliveryAddress,OrderItem,Order,deliveryPersonelle,OTP,CaoruselImages,CategoryInfo
from django.contrib.admin.helpers import Fieldset
from django.contrib.admin.helpers import AdminForm


class DeliveryAdmin(admin.ModelAdmin):
    list_display=['__str__','user']
    search_fields=['address','user__username']
    class Meta:
        model=DeliveryAddress



class OrderItemAdmin(admin.ModelAdmin):
    list_display=['__str__','user']
    search_fields=['user__username']
    class Meta:
        model=OrderItem


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields=['delivery_Personelle','completed','deliveryAddress']
        exclude=['items']
       
class OrderForm1(forms.ModelForm):

    class Meta:
        model = Order
        fields=['delivery_Personelle','completed','items','deliveryAddress']
       

class OrderAdmin(admin.ModelAdmin):
    #date_hierarchy = 'date_added'
    list_display=['__str__','user','completed','date_added']
    search_fields=['user__username','created','completed']
    list_filter=['completed']
    change_list_template='admin/order/order_change_list.html'
    change_form_template='admin/order/order_change_form.html'
    

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = OrderForm
        else: #if staff there will be a different form returned 
            kwargs['form'] = OrderForm
        return super().get_form(request, obj, **kwargs)

    
    def send_message(self,request,message):
        print("THE NEW MESSAGE IS ",message)
       
    def getOrderItems(self,id):
        instance=self.model.objects.get(pk=id) #get the cuurent order object
        items=instance.items.all() #Queryset of all the objects
       
        return items

    def getTotal(self,id):
        instance=self.model.objects.get(pk=id) #get the cuurent order object
        return instance.total

   

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['id']=object_id
        extra_context['orderItems'] = self.getOrderItems(id=object_id)
        extra_context['Total'] = self.getTotal(id=object_id)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    
    def changelist_view(self,request, extra_context=None):
         #print("THE LIST REUQEST IS",dir(request))
         context={}
         print(request.method)
         if(request.method=='POST' or request.method=='GET'):
             context['action']='reload'
             print("POST")
        
        
         return super(OrderAdmin,self).changelist_view(
             request, extra_context=context
         )

    class Media:
        js=("admin.js")



# Register your models here.
admin.site.site_header="10DerMeatz"
admin.site.title="ok"
admin.site.site_title="10DerMeatz Admin"
admin.site.register(DeliveryAddress,DeliveryAdmin)
admin.site.register(products)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.unregister(Group)
admin.site.register(deliveryPersonelle)
admin.site.register(OTP)
admin.site.register(CaoruselImages)
admin.site.register(CategoryInfo)