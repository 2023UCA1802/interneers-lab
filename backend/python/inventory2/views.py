from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services.product_service import ProductService
from .utils.serializers import serialize_product


product_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "brand": openapi.Schema(type=openapi.TYPE_STRING),
        "price": openapi.Schema(type=openapi.TYPE_NUMBER),
        "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    required=["name", "description", "category", "brand", "price", "quantity"]
)

class ProductListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="Get all products",
        manual_parameters=[
            openapi.Parameter('updated_after', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('sort', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={200: "List of products"}
    )
    def get(self, request):
        params = request.GET.dict()
        products = ProductService.get_all_products(params)
        return Response([serialize_product(p) for p in products])


    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=product_request_schema,
        responses={
            201: "Product created successfully",
            400: "Validation error"
        }
    )
    def post(self, request):
        try:
            product = ProductService.create_product(request.data)
            return Response(serialize_product(product), status=201)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class ProductDetailView(APIView):

    @swagger_auto_schema(
        operation_description="Get a product by ID",
        responses={200: "Product found", 404: "Not found"}
    )
    def get(self, request, pk):
        product = ProductService.get_product(pk)
        if not product:
            return Response({"error": "Not found"}, status=404)
        return Response(serialize_product(product))


    @swagger_auto_schema(
        operation_description="Update a product",
        request_body=product_request_schema,
        responses={200: "Updated", 400: "Validation error", 404: "Not found"}
    )
    def put(self, request, pk):
        try:
            product = ProductService.update_product(pk, request.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        if not product:
            return Response({"error": "Not found"}, status=404)

        return Response(serialize_product(product))


    @swagger_auto_schema(
        operation_description="Delete a product",
        responses={200: "Deleted", 404: "Not found"}
    )
    def delete(self, request, pk):
        success = ProductService.delete_product(pk)
        if not success:
            return Response({"error": "Not found"}, status=404)
        return Response({"message": "Deleted successfully"})