from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from io import TextIOWrapper
import csv
from .services.category_service import CategoryService
from .services.product_service import ProductService
from .repositories.product_repository import ProductRepository
from .utils.serializers import category_serializer, product_serializer

category_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=["name", "description"]
)

class CategoryController(APIView):

    @swagger_auto_schema(
        operation_description="Get all categories",
        responses={200: "List of categories"}
    )
    def get(self, request):
        categories = CategoryService.get_all_categories()
        return Response([category_serializer(c) for c in categories])

   
    @swagger_auto_schema(
        operation_description="Create a new category",
        request_body=category_schema,
        responses={
            201: "Category created successfully",
            400: "Validation error"
        }
    )
    def post(self, request):
        try:
            category = CategoryService.create_category(request.data)
            return Response(category_serializer(category), status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CategoryDetailController(APIView):

    @swagger_auto_schema(
    operation_description="Update a category",
    request_body=category_schema,
    responses={200: "Updated", 400: "Error"}
    )
    def put(self, request, pk):
        try:
            category = CategoryService.update_category(pk, request.data)
            return Response(category_serializer(category))
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
    operation_description="Delete a category",
    responses={200: "Deleted"}
    )
    def delete(self, request, pk):
        CategoryService.delete_category(pk)
        return Response({"message": "Deleted"})
    
class CategoryProductsController(APIView):

    @swagger_auto_schema(
    operation_description="Delete a category",
    responses={200: "Deleted"}
    )
    def get(self, request, category_id):
        products = CategoryService.get_products(category_id)
        return Response([product_serializer(p) for p in products])

class AddRemoveProductController(APIView):


    @swagger_auto_schema(
        operation_description="Add product to category",
        responses={200: "Product added"}
    )
    def post(self, request, category_id, product_id):
        product = ProductRepository.get_by_id(product_id)
        CategoryService.add_product(category_id, product)
        return Response({"message": "Added"})

    @swagger_auto_schema(
        operation_description="Remove product from category",
        responses={200: "Product removed"}
    )
    def delete(self, request, category_id, product_id):
        product = ProductRepository.get_by_id(product_id)
        CategoryService.remove_product(category_id, product)
        return Response({"message": "Removed"})

class BulkUploadController(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Bulk upload products via CSV",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="CSV file"
            )
        ],
        responses={
            200: "Upload successful",
            400: "CSV required"
        }
    )
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "CSV required"}, status=400)

        decoded = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(decoded)

        ProductService.bulk_upload(reader)

        return Response({"message": "Bulk upload successful"})

class ProductApi(APIView):
    @swagger_auto_schema(
    operation_description="Get products with filters",
    manual_parameters=[
        openapi.Parameter('categories', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('brand_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    )
    def get(self, request):
        params = request.GET.dict()
        products = ProductService.get_all_products(params)
        return Response([product_serializer(p) for p in products])