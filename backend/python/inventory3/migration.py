from .models import Product, ProductCategory


def migrate_products():
    # Create default category
    default_category = ProductCategory.objects(name="Uncategorized").first()

    if not default_category:
        default_category = ProductCategory(
            name="Uncategorized",
            description="Default category"
        ).save()

    # Assign to products with no categories
    products = Product.objects(categories__size=0)

    for product in products:
        product.categories.append(default_category)
        product.save()