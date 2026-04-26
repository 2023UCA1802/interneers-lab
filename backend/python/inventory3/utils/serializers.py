from mongoengine.errors import DoesNotExist

def product_serializer(product):
    brand_id = None
    try:
        if product.brand:
            brand_id = str(product.brand.id)
    except DoesNotExist:
        brand_id = "Deleted Brand"

    category_ids = []
    if product.categories:
        for c in product.categories:
            try:
                category_ids.append(str(c.id))
            except DoesNotExist:
                continue

    return {
        "id": str(product.id),
        "name": product.name,
        "brand": brand_id,
        "categories": category_ids,
    }

def category_serializer(category):
    return {
        "id": str(category.id),
        "name": category.name,
        "description": category.description,
    }

def brand_serializer(brand):
    return {
        "id": str(brand.id),
        "name": brand.name,
        "description": brand.description,
    }