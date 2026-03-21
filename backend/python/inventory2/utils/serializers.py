def serialize_product(product):
    """
    Serialize a Product object into a JSON-compatible dictionary.

    This function converts a MongoEngine Product document into a
    Python dictionary that can be returned as an API response.

    It ensures:
        - ObjectId is converted to string
        - All relevant fields are included
        - Data is JSON serializable

    Args:
        product (Product): MongoEngine Product document instance

    Returns:
        dict: Serialized product with the following structure:
            {
                "id": str,
                "name": str,
                "description": str,
                "category": str,
                "brand": str,
                "quantity": int,
                "price": float,
                "created_at": datetime,
                "updated_at": datetime
            }
    """
    return {
        "id": str(product.id),  # Convert ObjectId → string for JSON
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "brand": product.brand,
        "quantity": product.quantity,
        "price": product.price,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }