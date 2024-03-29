from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout as django_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db import IntegrityError


def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('/admin/product_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'admin_login.html', {'form': form})


def create_new_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        phone_number = request.POST.get('phone_number')
        full_name = request.POST.get('full_name')
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.username = phone_number
                user.first_name = full_name
                user.save()
                # Create UserProfile associated with the created user
                UserProfile.objects.create(user=user, address=address, pin_code=pin_code, phone_number=phone_number)
                # Log in the user
                login(request, user)
                messages.success(request, "Account created successfully.")

                interested_product_id_login=request.session.get('interested_product_id_login')
                if interested_product_id_login:
                    del request.session['interested_product_id_login']
                    return redirect(f'/product_details/{interested_product_id_login}')
                else:
                    return redirect('/')
            else:
                messages.error(request, "Failed to create account. Please check the provided information.")
        except IntegrityError as e:
            if 'UNIQUE constraint failed: auth_user.username' in str(e):
                messages.error(request, "Mobile number already exists. Please try to login.")
            else:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_new_account.html', {'form': form})


def login_account(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                interested_product_id_login=request.session.get('interested_product_id_login')
                if interested_product_id_login:
                    del request.session['interested_product_id_login']
                    return redirect(f'/product_details/{interested_product_id_login}')
                else:
                    return redirect('/')
            else:
                # Return an 'invalid login' error message
                return render(request, 'login_account.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login_account.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect('/login')


def product_list(request):
    form = ProductCreationForm()
    products = Product.objects.all().select_related()  # Fetch all products
    context = {
        'form': form,
        'products': products  # Renamed 'data' to 'products' for clarity
    }
    return render(request, "product_list.html", context)
    
def product_creation_form(request):
    try: 
        if request.method == 'POST': 
            form = ProductCreationForm(request.POST, request.FILES) 
            if form.is_valid():
                saved_form = form.save()
                product=Product.objects.get(id=saved_form.id) 
                ProductVariant.objects.create(product=product,image=saved_form.image,name='name')
                messages.success(request, 'Record Created Successfully ...!')
                return redirect('/admin/product_list')
            else:
                # Form is not valid, handle the error
                for field, errors in form.errors.items():
                     print(f'\n{field.capitalize()}: {", ".join(errors)}')
            
                return redirect('/admin/product_list')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, '404.html', {'error_message': str(e)}, status=500)

def delete_product(request,id):
        pi=Product.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Product Deleted Successfully!!!')
        return redirect('/admin/product_list')

    
def update_product(request, id):
    # try:
        product_instance = get_object_or_404(Product, id=id)
        form = ProductUpdationForm(request.POST or None, request.FILES or None, instance=product_instance)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Updated Successfully!')
                return redirect(f'/admin/product_dashboard/{id}')
            else:
                error_message = ', '.join([f"{field}: {error[0]}" for field, error in form.errors.items()])
                messages.warning(request, error_message)
                return redirect('/admin/product_list')
        else:
            return render(request, 'update_product.html', {'form': form})
    # except Exception as e: 
    #     return render(request, '404.html')


def product_dashboard(request,id):
    product_data = get_object_or_404(Product, id=id) 
    product_variant_data=ProductVariant.objects.filter(product=product_data).select_related()
    variant_form=VariantCreationForm()  
    context={
        'variant_form':variant_form,
        'product_data':product_data,
        'product_variant_data':product_variant_data,
        'id':id,
        }
    return render(request, 'product_dashboard.html',context)



def variant_creation_form(request):
    # try: 
        if request.method == 'POST':
            form = VariantCreationForm(request.POST, request.FILES)
            product_id = request.POST.get('product_id') 
            product = Product.objects.get(id=product_id)
            
            if form.is_valid():
                variant = form.save(commit=False)
                variant.product = product
                variant.save()

                messages.success(request, 'Record Created Successfully ...!')
                return redirect(f'/admin/product_dashboard/{product_id}')
            else:
                # Form is not valid, handle the error
                messages.error(request, 'Error in form submission. Please check the form.')
                return redirect(f'/admin/product_dashboard/{product_id}')
    # except Exception as e:
    #     # Handle other exceptions
    #     messages.error(request, f'An error occurred: {str(e)}')
    #     return render(request, '404.html', {'error_message': str(e)}, status=500)



def delete_variant(request,id):
        pi=ProductVariant.objects.get(pk=id)
        id=pi.product.id
        pi.delete()
        messages.success(request,'Product Deleted Successfully!!!')
        return redirect(f'/admin/product_dashboard/{id}')



def order_list(request):
    orders = Order.objects.all().select_related()  # Fetch all products
    context = {
        'orders': orders,
    }
    return render(request, "order_list.html", context)


def delete_order(request,id):
        pi=Order.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Order Deleted Successfully!!!')
        return redirect('/admin/order_list')


def order_dashboard(request,id):
    order_data = get_object_or_404(Order, id=id) 
    customer_profile = get_object_or_404(UserProfile, user=order_data.user) 
    order_item=OrderItem.objects.filter(order=order_data).select_related()
    Form_Update_Status = Update_Order_Status(instance=order_data)
    context={
        'order_data':order_data,
        'order_item':order_item,
        'customer_profile':customer_profile,
        'Form_Update_Status':Form_Update_Status,
        'id':id,
        }
    return render(request, 'order_dashboard.html',context)




def update_order_status(request):
    if request.method == 'POST':
        form = Update_Order_Status(request.POST)
        order_id=request.POST.get('order_id')
        status=request.POST.get('status')
        Order.objects.filter(id=order_id).update(status=status)
        print(order_id)
        return redirect(f'/admin/order_dashboard/{order_id}')
    else:
        return redirect('/admin/order_list')
    



    