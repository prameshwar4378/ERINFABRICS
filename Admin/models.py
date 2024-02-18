# In your models.py file within your Django app

from django.db import models
from django.contrib.auth.models import User 
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import Sum
import uuid

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

ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted by Admin', 'Accepted by Admin'),
        ('Regected by Admin', 'Regected by Admin'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Regected by Customer', 'Regected by Customer'),
    )

class Order(models.Model):
    order_id = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Pending')
    order_notes = models.CharField(max_length=250, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True)
    delivery_date = models.DateTimeField(null=True)
    payment_mode = models.CharField(max_length=30, null=True)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = str(uuid.uuid4().hex[:10].upper())
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order.order_id} - {self.product.name} - Quantity: {self.quantity}"




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True)
    pin_code = models.CharField(max_length=20,null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    @property
    def total_products_in_cart(self):
        try:
            cart = Cart.objects.get(user=self.user)
            return cart.cartitem_set.count()
        except Cart.DoesNotExist:
            return 0
        


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"

    def total_price(self):
        return self.cartitem_set.aggregate(total_price=Sum('product__price'))['total_price'] or 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1,null=True)

    def __str__(self):
        return f"{self.cart} - {self.product.name} - Quantity: {self.quantity}"

