from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

products = {}
product_id_counter = 1

product_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(type=openapi.TYPE_STRING),
        "brand": openapi.Schema(type=openapi.TYPE_STRING),
        "price": openapi.Schema(type=openapi.TYPE_NUMBER),
        "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    required=["name", "price","category","description","brand","quantity"]
)

def validate_product_data(data):
    errors = {}

    if not data.get("name"):
        errors["name"] = "Product name is required."

    if not data.get("category"):
        errors["category"] = "Product category is required."

    if not data.get("description"):
        errors["description"] = "Product description is required."

    if not data.get("brand"):
        errors["brand"] = "Product brand is required."

    if not data.get("quantity"):
        errors["quantity"] = "Product quantity is required."
    else:
        try:
            quantity = int(data["quantity"])
            if quantity < 0:
                errors["quantity"] = "Quantity cannot be negative."
        except ValueError:
            errors["quantity"] = "Quantity must be an integer."

    if "price" not in data:
        errors["price"] = "Price field is required."
    else:
        try:
            price = float(data["price"])
            if price < 0:
                errors["price"] = "Price must be a positive number."
        except ValueError:
            errors["price"] = "Price must be numeric."


    return errors

@swagger_auto_schema(
    method="post",
    operation_description="Create a new product",
    request_body=product_schema,
    responses={
        201: "Product created successfully",
        400: "Validation error"
    }
)
@api_view(["POST"])
def create_product(request):
    global product_id_counter

    data = request.data
    errors = validate_product_data(data)

    if errors:
        return Response(
            {
                "status": "error",
                "message": "Validation failed",
                "errors": errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    product = {
        "id": product_id_counter,
        "name": data.get("name"),
        "description": data.get("description"),
        "category": data.get("category"),
        "brand": data.get("brand"),
        "price": float(data.get("price")),
        "quantity": int(data.get("quantity", 0)),
    }

    products[product_id_counter] = product
    product_id_counter += 1

    return Response(
        {
            "status": "success",
            "message": "Product created successfully",
            "data": product
        },
        status=status.HTTP_201_CREATED
    )

@swagger_auto_schema(
    method="get",
    operation_description="Get all products with pagination",
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={200: "List of products"}
)
@api_view(["GET"])
def get_products(request):

    try:
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 5))
    except ValueError:
        return Response(
            {
                "status": "error",
                "message": "page and page_size must be integers"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if page <= 0 or page_size <= 0:
        return Response(
            {
                "status": "error",
                "message": "page and page_size must be positive integers"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    product_list = list(products.values())

    start = (page - 1) * page_size
    end = start + page_size

    paginated_products = product_list[start:end]

    return Response(
        {
            "status": "success",
            "page": page,
            "page_size": page_size,
            "total_products": len(product_list),
            "data": paginated_products
        }
    )

@swagger_auto_schema(
    method="get",
    operation_description="Get product by ID",
    responses={
        200: "Product found",
        404: "Product not found"
    }
)
@api_view(["GET"])
def get_product(request, product_id):

    product = products.get(product_id)

    if not product:
        return Response(
            {
                "status": "error",
                "message": f"Product with id {product_id} not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "status": "success",
            "data": product
        }
    )

@swagger_auto_schema(
    method="put",
    operation_description="Update an existing product",
    request_body=product_schema,
    responses={
        200: "Product updated successfully",
        400: "Validation error",
        404: "Product not found"
    }
)
@api_view(['PUT'])
def update_product(request, product_id):

    if product_id not in products:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    data = request.data
    errors = validate_product_data(data)

    if errors:
        return Response({"errors": errors}, status=400)

    product = products[product_id]

    product["name"] = data.get("name", product["name"])
    product["description"] = data.get("description", product["description"])
    product["category"] = data.get("category", product["category"])
    product["brand"] = data.get("brand", product["brand"])
    product["price"] = float(data.get("price", product["price"]))
    product["quantity"] = int(data.get("quantity", product["quantity"]))

    return Response(product)

@swagger_auto_schema(
    method="delete",
    operation_description="Delete a product",
    responses={
        200: "Deleted successfully",
        404: "Product not found"
    }
)
@api_view(['DELETE'])
def delete_product(request, product_id):

    if product_id not in products:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    del products[product_id]

    return Response(
        {"message": "Product deleted successfully"},
        status=status.HTTP_200_OK
    )


