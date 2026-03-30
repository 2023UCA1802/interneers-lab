from ..models import Product, ProductCategory


class ProductRepository:
    """
    Repository layer for handling Product-related database operations.

    This class abstracts MongoEngine queries and provides a clean
    interface for the service layer.
    """

    @staticmethod
    def get_by_id(product_id):
        """
        Retrieve a product by its ID.

        Args:
            product_id (str or ObjectId): Unique product identifier

        Returns:
            Product: The matching product document

        Raises:
            DoesNotExist: If product is not found
        """
        return Product.objects.get(id=product_id)

    @staticmethod
    def get_by_category(category_id):
        """
        Retrieve all products belonging to a specific category.

        Args:
            category_id (str or ObjectId): Category identifier

        Returns:
            QuerySet[Product]: List of products in the category
        """
        return Product.objects(categories=category_id)

    @staticmethod
    def save(product):
        """
        Save or update a product.

        Args:
            product (Product): Product instance to save

        Returns:
            Product: Saved product document
        """
        return product.save()

    @staticmethod
    def bulk_insert(products):
        """
        Insert multiple products in bulk.

        Args:
            products (list[Product]): List of product instances

        Returns:
            list: Inserted product documents

        Note:
            load_bulk=False improves performance for large inserts.
        """
        return Product.objects.insert(products, load_bulk=False)

    @staticmethod
    def add_products_to_category(category_id, product_id):
        """
        Add a product to a category.

        Args:
            category_id (str or ObjectId): Category identifier
            product_id (str or ObjectId): Product identifier

        Returns:
            None

        Note:
            Prevents duplicate category assignment.
        """
        product = Product.objects.get(id=product_id)
        category = ProductCategory.objects.get(id=category_id)

        if category not in product.categories:
            product.categories.append(category)
            product.save()

    @staticmethod
    def remove_products_from_category(category_id, product_id):
        """
        Remove a product from a category.

        Args:
            category_id (str or ObjectId): Category identifier
            product_id (str or ObjectId): Product identifier

        Returns:
            None

        Note:
            Only removes if the relationship exists.
        """
        product = Product.objects.get(id=product_id)
        category = ProductCategory.objects.get(id=category_id)

        if category in product.categories:
            product.categories.remove(category)
            product.save()