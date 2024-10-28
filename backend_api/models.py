from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=160, null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=160, null=True)
    date_of_birth = models.CharField(max_length=10, null=True)  
    avatar = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    images = models.JSONField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    sold = models.IntegerField()
    view = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    class Status(models.IntegerChoices):
        IN_CART = -1, 'In Cart'
        ALL = 0, 'All'
        WAIT_FOR_CONFIRMATION = 1, 'Wait for Confirmation'
        WAIT_FOR_GETTING = 2, 'Wait for Getting'
        IN_PROGRESS = 3, 'In Progress'
        DELIVERED = 4, 'Delivered'
        CANCELLED = 5, 'Cancelled'
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=Status.choices, default=Status.IN_CART)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
