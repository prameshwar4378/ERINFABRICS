from django import forms
from .models import *
from django.core.exceptions import ValidationError  
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','product_details','washing_instruction','description','price', 'strikethrough','image') 
        labels = { 
            'name': 'Product Name',  
            'strikethrough':'Strikethrough Price'
        }   
        widgets = {
            'product_details': CKEditorWidget(),
        }

class ProductUpdationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','product_details','washing_instruction','description','price', 'strikethrough','image') 
        labels = { 
            'name': 'Product Name',  
            'strikethrough':'Strikethrough Price',
            'product_details':''

        }   
        widgets = {
            'product_details': CKEditorWidget(),
        }

class VariantCreationForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ('name','image') 
 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    pin_code = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    full_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [ 'full_name','phone_number','address', 'pin_code', 'email', 'password1', 'password2',  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['password1', 'password2']:
            self.fields[field_name].help_text = None

class Update_Order_Status(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',) 
 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)