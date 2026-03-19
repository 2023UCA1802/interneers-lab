def serialize_product(product):
    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "brand": product.brand,
        "quantity": product.quantity,
        "price": product.price,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }