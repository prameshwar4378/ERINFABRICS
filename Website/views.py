from django.shortcuts import render,redirect,get_object_or_404
from Admin.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F, ExpressionWrapper, Sum, DecimalField
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD

=======
from Admin.forms import *
>>>>>>> 263e44feef7f7de6cb964753e8594d21f6fe281d
def test(request):
    return render(request,'test.html')

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

@login_required
def cart(request):
    try: 
        cart = Cart.objects.get(user=request.user)
 
        products = CartItem.objects.filter(cart=cart.id)
        grand_total_amount = CartItem.objects.filter(cart__user=request.user).aggregate(
                total=Sum(F('product__price') * F('quantity'), output_field=DecimalField())
            )['total']

    except ObjectDoesNotExist: 
        cart = None
        products = None
<<<<<<< HEAD
    return render(request, 'cart.html', {'products': products,'grand_total_amount':grand_total_amount})

@login_required
=======
        grand_total_amount=None
    return render(request, 'cart.html', {'products': products,'grand_total_amount':grand_total_amount})
 
>>>>>>> 263e44feef7f7de6cb964753e8594d21f6fe281d
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        request.session['interested_product_id_login'] = product_id
        return redirect('/login')
    user = request.user
    print(user)
    cart, created = Cart.objects.get_or_create(user=user)
    product = Product.objects.get(id=product_id)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request,'Item added in cart')
    return redirect(f'/product_details/{product_id}')
 
@login_required
def update_cart_item(request):
    if request.method == 'POST':
        print("this is test")
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

@login_required
def delete_item_from_cart(request, id):
    try: 
        cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
        cart_item.delete()
        return redirect('/cart')
    except CartItem.DoesNotExist:
        return redirect('/cart')

 
def checkout(request):
    try: 
        cart = Cart.objects.get(user=request.user)
        if not cart:
            return redirect('/')
        products = CartItem.objects.filter(cart=cart.id)
        grand_total_amount = CartItem.objects.filter(cart__user=request.user).aggregate(
                total=Sum(F('product__price') * F('quantity'), output_field=DecimalField())
            )['total']
        user_details=UserProfile.objects.get(user=request.user)
 
    except ObjectDoesNotExist:
        cart = None
        products = None
        grand_total_amount=None
    return render(request, 'checkout.html', {'products': products,'grand_total_amount':grand_total_amount,'user_details':user_details})
 

def update_profile_from_checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        phone_number = request.POST.get('phone_number')
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.user.first_name = full_name  # Assuming 'full_name' corresponds to the first name
        user_profile.address = address
        user_profile.pin_code = pin_code
        user_profile.phone_number = phone_number
        # Save changes
        user_profile.user.save()  # Save changes to the User model
        user_profile.save()  # Save changes to the UserProfile model
        
        return redirect('/checkout')
    else:
        return redirect('/')  # Redirect if not a POST request

def create_order(request):
    # Get the logged-in user
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    grand_total_amount = CartItem.objects.filter(cart__user=request.user).aggregate(
            total=Sum(F('product__price') * F('quantity'), output_field=DecimalField())
        )['total']
    if cart:
        order = Order.objects.create(user=user, total_price=grand_total_amount, status='Pending')
        for cart_item in cart.cartitem_set.all():  # Iterate over cart items
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        cart.delete()
        request.session['order_id_for_success_page'] = order.order_id
        return redirect('/order_success')  # Redirect to a success page after order creation
    else:
        # Handle the case where the user does not have any items in their cart
        return render(request, 'empty_cart.html')


def order_success(request):
    order_id=request.session.get('order_id_for_success_page')
    return render(request, 'order_success.html',{'order_id':order_id})
    