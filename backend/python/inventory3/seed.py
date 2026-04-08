from inventory3.models import Brand, ProductCategory, Product

DEFAULT_CATEGORIES = [
    {"name": "Food", "description": "All food items"},
    {"name": "Kitchen Essentials", "description": "Kitchen products"},
    {"name": "Electronics", "description": "Electronic items"},
]


def seed_categories():
    for cat in DEFAULT_CATEGORIES:
        existing = ProductCategory.objects(name=cat["name"]).first()
        if not existing:
            ProductCategory(**cat).save()




def seed_test_data():
    """
    Seed test database with minimal required data.

    Returns:
        dict: Created objects (brand, category, product)
    """

    brand = Brand(
        name="TestBrand",
        description="Test brand"
    ).save()

    category = ProductCategory(
        name="TestCategory",
        description="Test category"
    ).save()

    product = Product(
        name="TestProduct",
        brand=brand,
        categories=[category]
    ).save()

    return {
        "brand": brand,
        "category": category,
        "product": product
    }