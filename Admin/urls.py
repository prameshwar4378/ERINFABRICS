from django.contrib import admin
from django.urls import path
from Admin.views import  *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('product_list', product_list,name="product_list"),
    path('product_creation_form', product_creation_form,name="product_creation_form"),
    path('product_dashboard/<int:id>', product_dashboard,name="product_dashboard"),
    path('variant_creation_form', variant_creation_form,name="variant_creation_form"),
    path('delete_product/<int:id>', delete_product,name="delete_product"),
    path('delete_variant/<int:id>', delete_variant,name="delete_variant"),
    path('update_product/<int:id>', update_product,name="update_product"),

    path('order_list/', order_list,name="order_list"),
    path('order_dashboard/<int:id>', order_dashboard,name="order_dashboard"),
    path('update_order_status/', update_order_status,name="update_order_status"),
    path('delete_order/<int:id>', delete_order, name="delete_order"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)