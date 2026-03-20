from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.product_service import ProductService
from .utils.serializers import serialize_product


class ProductListCreateView(APIView):

    def get(self, request):
        params = request.GET.dict()
        products = ProductService.get_all_products(params)
        return Response([serialize_product(p) for p in products])

    def post(self, request):
        try:
            product = ProductService.create_product(request.data)
            return Response(serialize_product(product), status=201)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class ProductDetailView(APIView):

    def get(self, request, pk):
        product = ProductService.get_product(pk)
        if not product:
            return Response({"error": "Not found"}, status=404)
        return Response(serialize_product(product))

    def put(self, request, pk):
        try:
            product = ProductService.update_product(pk, request.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        if not product:
            return Response({"error": "Not found"}, status=404)

        return Response(serialize_product(product))

    def delete(self, request, pk):
        success = ProductService.delete_product(pk)
        if not success:
            return Response({"error": "Not found"}, status=404)
        return Response({"message": "Deleted successfully"})