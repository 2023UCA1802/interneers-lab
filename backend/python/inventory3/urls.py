from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', CategoryController.as_view()),
    path('categories/<str:pk>/', CategoryDetailController.as_view()),

    path('categories/<str:category_id>/products/', CategoryProductsController.as_view()),
    path('categories/<str:category_id>/products/<str:product_id>/', AddRemoveProductController.as_view()),

    path('products/bulk-upload/', BulkUploadController.as_view()),
]