from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from io import TextIOWrapper
import csv
from .services.category_service import CategoryService
from .services.product_service import ProductService
from .services.brand_service import BrandService
from .repositories.product_repository import ProductRepository
from .utils.serializers import category_serializer, product_serializer, brand_serializer

category_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=["name", "description"]
)

brand_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=["name", "description"]
)


class BrandController(APIView):

    @swagger_auto_schema(
        operation_description="Get all brands",
        responses={200: "List of brands"}
    )
    def get(self, request):
        brands = BrandService.get_all_brands()
        return Response([brand_serializer(b) for b in brands])

    @swagger_auto_schema(
        operation_description="Create a new brand",
        request_body=brand_schema,
        responses={201: "Brand created", 400: "Validation error"}
    )
    def post(self, request):
        try:
            brand = BrandService.create_brand(request.data)
            return Response(brand_serializer(brand), status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class BrandDetailController(APIView):

    @swagger_auto_schema(
        operation_description="Update a brand",
        request_body=brand_schema,
        responses={200: "Updated", 400: "Error"}
    )
    def put(self, request, brand_id):
        try:
            brand = BrandService.update_brand(brand_id, request.data)
            return Response(brand_serializer(brand))
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_description="Delete a brand",
        responses={200: "Deleted"}
    )
    def delete(self, request, brand_id):
        try:
            BrandService.delete_brand(brand_id)
            return Response({"message": "Brand deleted"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

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
        operation_description="Get a category",
        responses={200: "Category detail", 404: "Not found"}
    )
    def get(self, request, pk):
        try:
            category = CategoryService.get_category_by_id(pk)
            return Response(category_serializer(category))
        except Exception as e:
            return Response({"error": str(e)}, status=404)

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
        try:
            CategoryService.delete_category(pk)
            return Response({"message": "Deleted"})
        except Exception as e:
            return Response({"error": str(e)}, status=404)
    
class CategoryProductsController(APIView):

    @swagger_auto_schema(
        operation_description="Get products by category",
        responses={200: "List of products"}
    )
    def get(self, request, category_id):
        try:
            products = CategoryService.get_products(category_id)
            return Response([product_serializer(p) for p in products])
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_description="Create a product and assign it to a category",
        responses={201: "Created", 400: "Bad Request"}
    )
    def post(self, request, category_id):
        try:
            product = ProductService.create_product(request.data)
            CategoryService.add_product(category_id, product)
            return Response({"message": "Product created and assigned", "product": product_serializer(product)}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class AddRemoveProductController(APIView):


    @swagger_auto_schema(
        operation_description="Add product to category",
        responses={200: "Product added"}
    )
    def post(self, request, category_id, product_id):
        try:
            product = ProductRepository.get_by_id(product_id)
            CategoryService.add_product(category_id, product)
            return Response({"message": "Added"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_description="Remove product from category",
        responses={200: "Product removed"}
    )
    def delete(self, request, category_id, product_id):
        try:
            product = ProductRepository.get_by_id(product_id)
            CategoryService.remove_product(category_id, product)
            return Response({"message": "Removed"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

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
        try:
            params = request.GET.dict()
            products = ProductService.get_all_products(params)
            return Response([product_serializer(p) for p in products])
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ProductDetailController(APIView):

    @swagger_auto_schema(
        operation_description="Get a product",
        responses={200: "Product detail", 404: "Not found"}
    )
    def get(self, request, product_id):
        try:
            product = ProductService.get_product_by_id(product_id)
            return Response(product_serializer(product))
        except Exception as e:
            return Response({"error": str(e)}, status=404)

    @swagger_auto_schema(
        operation_description="Update a product",
        responses={200: "Updated", 400: "Error"}
    )
    def put(self, request, product_id):
        try:
            product = ProductService.update_product(product_id, request.data)
            return Response(product_serializer(product))
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_description="Delete a product",
        responses={200: "Deleted", 404: "Not found"}
    )
    def delete(self, request, product_id):
        try:
            ProductService.delete_product(product_id)
            return Response({"message": "Product deleted"})
        except Exception as e:
            return Response({"error": str(e)}, status=404)