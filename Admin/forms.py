from django import forms
from .models import *
from django.core.exceptions import ValidationError  
from ckeditor.widgets import CKEditorWidget
 
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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)