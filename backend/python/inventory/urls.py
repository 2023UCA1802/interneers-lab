from django.urls import path
from . import views

urlpatterns = [
    path('products/get/', views.get_products),
    path('products/create/', views.create_product),
    path('products/<int:product_id>/get/', views.get_product),
    path('products/<int:product_id>/update/', views.update_product),
    path('products/<int:product_id>/delete/', views.delete_product),
]