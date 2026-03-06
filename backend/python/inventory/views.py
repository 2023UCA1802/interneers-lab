from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


products = {}
product_id_counter = 1


def validate_product_data(data):
    errors = {}

    if not data.get("name"):
        errors["name"] = "Product name is required."

    if "price" not in data:
        errors["price"] = "Price field is required."
    else:
        try:
            price = float(data["price"])
            if price < 0:
                errors["price"] = "Price must be a positive number."
        except ValueError:
            errors["price"] = "Price must be numeric."

    if "quantity" in data:
        try:
            quantity = int(data["quantity"])
            if quantity < 0:
                errors["quantity"] = "Quantity cannot be negative."
        except ValueError:
            errors["quantity"] = "Quantity must be an integer."

    return errors

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


