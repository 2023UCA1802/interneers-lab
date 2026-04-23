def product_serializer(product):
    brand_name = "No Brand"
    try:
        if product.brand:
            brand_name = product.brand.name
    except:
        pass

    return {
        "id": str(product.id),
        "name": product.name,
        "brand": brand_name,
        "categories": [str(c.id) for c in product.categories],
        "description": getattr(product, "description", None),
        "price": getattr(product, "price", None),
        "stock": getattr(product, "stock", None),
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