from django.shortcuts import render,redirect,get_object_or_404
from Admin.models import *
# Create your views here.
def index(request):
    products=Product.objects.filter().select_related()
    context={
        'products':products,
        }
    return render(request,"index.html",context)


def product_details(request,id):
    p_details=Product.objects.get(id=id)
    p_variant_image=ProductVariant.objects.filter(product=id).select_related()
    context={
        'product':p_details,
        'p_variant_image':p_variant_image,
        }
    return render(request,"product_details.html",context)