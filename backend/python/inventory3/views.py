from django.views import View
from django.http import JsonResponse
import json
from .services.category_service import CategoryService
from .repositories.product_repository import ProductRepository
from .utils.serializers import brand_serializer,category_serializer,product_serializer

# Create your views here.
