from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from io import TextIOWrapper
import csv
from .services.category_service import CategoryService
from .services.product_service import ProductService
from .repositories.product_repository import ProductRepository
from .utils.serializers import category_serializer, product_serializer


class CategoryController(APIView):

    def get(self, request):
        categories = CategoryService.get_all_categories()
        return Response([category_serializer(c) for c in categories])

    def post(self, request):
        try:
            category = CategoryService.create_category(request.data)
            return Response(category_serializer(category), status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CategoryDetailController(APIView):

    def put(self, request, pk):
        try:
            category = CategoryService.update_category(pk, request.data)
            return Response(category_serializer(category))
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def delete(self, request, pk):
        CategoryService.delete_category(pk)
        return Response({"message": "Deleted"})
    
class CategoryProductsController(APIView):

    def get(self, request, category_id):
        products = CategoryService.get_products(category_id)
        return Response([product_serializer(p) for p in products])

class AddRemoveProductController(APIView):

    def post(self, request, category_id, product_id):
        product = ProductRepository.get_by_id(product_id)
        CategoryService.add_product(category_id, product)
        return Response({"message": "Added"})

    def delete(self, request, category_id, product_id):
        product = ProductRepository.get_by_id(product_id)
        CategoryService.remove_product(category_id, product)
        return Response({"message": "Removed"})

class BulkUploadController(APIView):

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "CSV required"}, status=400)

        decoded = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(decoded)

        ProductService.bulk_upload(reader)

        return Response({"message": "Bulk upload successful"})