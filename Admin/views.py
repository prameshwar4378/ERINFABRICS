from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout

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


def admin_logout(request):
    logout(request)
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
                form.save()  
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