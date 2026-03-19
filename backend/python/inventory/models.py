from django.db import models
from django.utils import timezone


class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    
    def __str__(self):
        return self.name

class Product(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category=models.ForeignKey(
        Category,on_delete=models.CASCADE,related_name="products"
    )
    brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True,related_name="products")
    price=models.DecimalField(max_digits=10,decimal_places=2)

    quantity_in_stock=models.PositiveIntegerField(
        default=0,
        help_text="Number of items available in the warehouse"
    )
    stock_keeping_unit=models.CharField(max_length=100,unique=True,help_text="Stock keeping unit to identify the items uniquely")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ProductModel2(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name