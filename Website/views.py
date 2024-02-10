from django.shortcuts import render,redirect,get_object_or_404
from Admin.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F, ExpressionWrapper, Sum, DecimalField

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
    print(request.session.get('cart', []))
    context={ 
        'product':p_details,
        'p_variant_image':p_variant_image,
        }
    return render(request,"product_details.html",context)


from django.core.exceptions import ObjectDoesNotExist

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        products = CartItem.objects.filter(cart=cart.id)

    except ObjectDoesNotExist:
        cart = None
        products = None
    return render(request, 'cart.html', {'products': products})


def add_to_cart(request, product_id):
    user = request.user
    print(user)
    cart, created = Cart.objects.get_or_create(user=user)
    product = Product.objects.get(id=product_id)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request,'Item added in cart')
    return redirect('/')
 
def update_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
            subtotal = cart_item.product.price * quantity
            grand_total = CartItem.objects.filter(cart__user=request.user).aggregate(
                total=Sum(F('product__price') * F('quantity'), output_field=DecimalField())
            )['total']

            return JsonResponse({'subtotal': subtotal,'grand_total':grand_total})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item does not exist.'}, status=400)
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def delete_item_from_cart(request, id):
    try: 
        cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
        cart_item.delete()
        return redirect('/cart')
    except CartItem.DoesNotExist:
        return redirect('/cart')