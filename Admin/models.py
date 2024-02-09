# In your models.py file within your Django app

from django.db import models
from django.contrib.auth.models import User 
from ckeditor.fields import RichTextField
class Product(models.Model):
    p_code = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=255)
    product_details = RichTextField(null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    strikethrough = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/',null=True)
    washing_instruction = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name
 
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name=models.CharField( max_length=100,null=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.name} - {self.color}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class CartItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} - {self.product_variant.color}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
