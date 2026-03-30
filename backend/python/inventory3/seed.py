from .models import ProductCategory

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