from ..models import Product
from bson import ObjectId
from bson.errors import InvalidId


class ProductRepository:
    """
    Product Repository Layer

    This class handles all database interactions related to the Product model.
    It abstracts CRUD operations and query logic from the service layer.

    Responsibilities:
        - Fetch products (with filters)
        - Retrieve product by ID
        - Create new products
        - Update existing products
        - Delete products
        - Detect duplicate products

    Note:
        This layer directly interacts with MongoDB via MongoEngine.
    """

    @staticmethod
    def get_all(filters=None):
        """
        Retrieve all products with optional filtering and sorting.

        Args:
            filters (dict, optional):
                Dictionary containing filter options such as:
                - updated_after (datetime): Fetch products updated after a certain time
                - sort (str): Sorting option (e.g., "latest")

        Returns:
            list: List of Product objects
        """
        query = Product.objects()

        if filters:
            if filters.get("updated_after"):
                query = query.filter(updated_at__gt=filters["updated_after"])

            if filters.get("sort") == "latest":
                query = query.order_by("-created_at")

        return list(query)

    @staticmethod
    def get_by_id(product_id):
        """
        Retrieve a single product by its ID.

        Args:
            product_id (str): MongoDB ObjectId as a string

        Returns:
            Product | None:
                - Product object if found
                - None if invalid ID or not found
        """
        try:
            ObjectId(product_id)  # Validate ObjectId format
        except (InvalidId, TypeError):
            return None

        return Product.objects(id=product_id).first()

    @staticmethod
    def create(data):
        """
        Create and save a new product.

        Args:
            data (dict): Dictionary containing product fields

        Returns:
            Product: The created Product object
        """
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product_id, data):
        """
        Update an existing product.

        Args:
            product_id (str): MongoDB ObjectId as a string
            data (dict): Fields to update

        Returns:
            Product | None:
                - Updated product if successful
                - None if product does not exist or ID is invalid
        """
        try:
            ObjectId(product_id)
        except (InvalidId, TypeError):
            return None

        product = Product.objects(id=product_id).first()
        if not product:
            return None

        # Dynamically update fields
        for key, value in data.items():
            setattr(product, key, value)

        product.save()
        return product

    @staticmethod
    def delete(product_id):
        """
        Delete a product by ID.

        Args:
            product_id (str): MongoDB ObjectId as a string

        Returns:
            bool:
                - True if deletion was successful
                - False if product not found or invalid ID
        """
        try:
            ObjectId(product_id)
        except (InvalidId, TypeError):
            return False

        product = Product.objects(id=product_id).first()
        if not product:
            return False

        product.delete()
        return True

    @staticmethod
    def find_duplicate(data):
        """
        Check if a duplicate product exists.

        Duplicate criteria:
            - name
            - category
            - brand
            - price

        Args:
            data (dict): Product data to check

        Returns:
            Product | None:
                - Existing product if duplicate found
                - None if no duplicate exists
        """
        return Product.objects(
            name=data["name"],
            category=data["category"],
            brand=data["brand"],
            price=data["price"]
        ).first()