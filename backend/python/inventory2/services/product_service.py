from ..repositories.product_repository import ProductRepository


class ProductService:
    """
    Product Service Layer

    This class contains business logic for managing products.
    It acts as an intermediary between the controller (views)
    and the repository (database layer).

    Responsibilities:
        - Validate incoming data
        - Apply business rules (e.g., no duplicates, valid price/quantity)
        - Normalize input data (e.g., strip strings)
        - Delegate database operations to the repository layer
    """

    @staticmethod
    def get_all_products(params):
        """
        Fetch all products with optional filters.

        Args:
            params (dict): Query parameters such as:
                - updated_after (datetime)
                - sort (str, e.g., "latest")

        Returns:
            list: List of Product objects
        """
        return ProductRepository.get_all(params)

    @staticmethod
    def get_product(product_id):
        """
        Retrieve a single product by ID.

        Args:
            product_id (str): MongoDB ObjectId

        Returns:
            Product | None:
                - Product if found
                - None if not found or invalid ID
        """
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def create_product(data):
        """
        Create a new product after validation and business checks.

        Steps:
            1. Validate required fields
            2. Normalize string inputs (strip spaces)
            3. Check for duplicate product
            4. Validate price and quantity
            5. Save product via repository

        Args:
            data (dict): Product data containing:
                - name
                - description
                - category
                - brand
                - price
                - quantity

        Returns:
            Product: Created product object

        Raises:
            ValueError:
                - If required fields are missing
                - If duplicate product exists
                - If price <= 0
                - If quantity <= 0
        """

        required_fields = ["name", "description", "category", "brand", "price", "quantity"]

        # Validate required fields
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                raise ValueError(f"{field} is required")

        # Normalize string fields
        data["name"] = data["name"].strip()
        data["description"] = data["description"].strip()
        data["category"] = data["category"].strip()
        data["brand"] = data["brand"].strip()

        # Check duplicate product
        existing = ProductRepository.find_duplicate(data)
        if existing:
            raise ValueError("Duplicate product already exists")

        # Validate price
        if data["price"] <= 0:
            raise ValueError("Price must be greater than 0")

        # Validate quantity
        if data["quantity"] <= 0:
            raise ValueError("Quantity must be greater than 0")

        return ProductRepository.create(data)

    @staticmethod
    def update_product(product_id, data):
        """
        Update an existing product with validation and business rules.

        Steps:
            1. Normalize string fields if present
            2. Check for duplicate product (excluding current product)
            3. Validate price and quantity (if provided)
            4. Update product via repository

        Args:
            product_id (str): MongoDB ObjectId
            data (dict): Fields to update

        Returns:
            Product | None:
                - Updated product if successful
                - None if product not found

        Raises:
            ValueError:
                - If duplicate product exists
                - If price <= 0
                - If quantity < 0
        """

        # Normalize string fields if present
        if "name" in data:
            data["name"] = data["name"].strip()

        if "description" in data:
            data["description"] = data["description"].strip()

        if "category" in data:
            data["category"] = data["category"].strip()

        if "brand" in data:
            data["brand"] = data["brand"].strip()

        # Duplicate check (only if sufficient fields provided)
        check_fields = ["name", "category", "brand", "price"]
        if all(field in data for field in check_fields):
            existing = ProductRepository.find_duplicate(data)
            if existing and str(existing.id) != str(product_id):
                raise ValueError("Duplicate product already exists")

        # Validate price
        if "price" in data and data["price"] <= 0:
            raise ValueError("Price must be greater than 0")

        # Validate quantity
        if "quantity" in data and data["quantity"] < 0:
            raise ValueError("Quantity must be greater than 0")

        return ProductRepository.update(product_id, data)

    @staticmethod
    def delete_product(product_id):
        """
        Delete a product by ID.

        Args:
            product_id (str): MongoDB ObjectId

        Returns:
            bool:
                - True if deletion successful
                - False if product not found or invalid ID
        """
        return ProductRepository.delete(product_id)