# Django Inventory Models Documentation

This document explains the Django models used for an inventory management system.  
The models define **Categories, Brands, and Products** stored in the database using the Django ORM.

---

# Imports

```python
from django.db import models
from django.utils import timezone
```

### `django.db.models`
Provides classes used to define database models.


### `django.utils.timezone`
Used to handle timezone-aware datetime objects.


---


# Category Model


```python
class Category(models.Model):
```

The Category model represents product categories such as:
- Electronics
- Clothing
- Books
- Furniture

### Fields
#### Name
```python
name=models.CharField(max_length=100,unique=True)
```
- CharField stores short text values.
- max_length=100 limits the length of the text.
- unique=True ensures that each category name is unique.

#### Description
```python
description=models.TextField()
```
- TextField is used for long text.
- blank=True means the field is optional.



#### String Representation
```python
def __str__(self):
    return self.name
```
This method defines how the object appears in:
- Django Admin
- Django shell
- Query results

Similarly for ``Brand`` Model
```python
class Brand(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    
    def __str__(self):
        return self.name
```
Now, ``Product`` Model contains the above things along with the foreign keys from these models as shown below

```python
category=models.ForeignKey(
Category,on_delete=models.CASCADE,related_name="products"
)
```
It creates a many-to-one relationship between Product and Category i.e. One category can have multiple products.
#### Parameters

- ForeignKey → relationship between models
- on_delete=models.CASCADE → if a category is deleted, all related products are also deleted
- related_name="products" → allows reverse lookup

Similarly ``Brand`` Model is also used in this as foreign key along with some other fields

```python
price=models.DecimalField(max_digits=10,decimal_places=2)
```
Stores product price and ```max_digits=10``` denotes that there can be maximum 10 digits with 2 decimal places denoted by ```decimal_places=2```


```python
quantity_in_stock=models.PositiveIntegerField(default=0, help_text="Number of items available in the warehouse"
)
```
Stores how many items are available in stock.
- Only positive integers allowed
- Default value is 0

```python
stock_keeping_unit=models.CharField(
    max_length=100,
    unique=True,
    help_text="Stock keeping unit to identify the items uniquely"
)
```
SKU is a unique identifier used in inventory systems.
```python
created_date = models.DateTimeField(auto_now_add=True)
```
Stores when the product was created and automatically sets when the object is first created.

```python
updated_at = models.DateTimeField(auto_now=True)
```
Stores the last update timestamp and it is automatically updated whenever the product is modified.

```python
is_active = models.BooleanField(default=True)
```
Used to enable or disable products.

We also created a simplified version of it which is ```ProductModel2```

```python
class ProductModel2(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
```


## Restful APIs

# Product API Endpoints

The following URL routes define the **CRUD operations** for managing products in the Django application.

```python
path('products/', views.get_products), # for getting all the products
path('products/create/', views.create_product), # for creating any product
path('products/<int:product_id>/', views.get_product), # for getting a single product by choosing their id
path('products/<int:product_id>/update/', views.update_product), # for updating the product by using their product id
path('products/<int:product_id>/delete/', views.delete_product), # for deleting the product by using their product id
```