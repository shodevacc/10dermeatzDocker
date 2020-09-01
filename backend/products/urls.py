from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
app_name='products'

urlpatterns=[
    path('',home_view,name='home_view'),
    path('product/<slug:category>/',category_view,name='category_view'),
    path('detail/<int:id>/',product_detail_view,name='product_detail_view'),
    path('checkout/',checkout_view,name='checkout_view'),
    path('payment/',payment_view,name='payment_view'),
    path('paymentsuccess/',payment_success_view,name='payment_success_view'),
    path('paymentfail/',payment_fail_view,name='payment_fail_view'),
    
]


#if settings.DEBUG:
    #urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)