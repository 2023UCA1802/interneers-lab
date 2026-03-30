def product_serializer(product):
    return {
        "id": str(product.id),
        "name": product.name,
        "brand": str(product.brand.id) if product.brand else None,
        "categories": [str(c.id) for c in product.categories],
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