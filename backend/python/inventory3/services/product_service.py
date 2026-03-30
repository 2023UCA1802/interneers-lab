from mongoengine.errors import ValidationError
from ..models import Product, Brand
from ..repositories.product_repository import ProductRepository
from bson import ObjectId
from bson.errors import InvalidId


class ProductService:
    """
    Service layer for handling Product-related business logic.

    Responsibilities:
    - Validate input data
    - Apply filtering logic
    - Handle ObjectId conversion
    - Prevent duplicates
    - Coordinate with repository layer
    """

    @staticmethod
    def get_all_products(filters):
        """
        Fetch products with optional filtering.

        Supported Filters:
            - categories (comma-separated category IDs)
            - brand_id (single brand ID)
            - name (partial match search)

        Args:
            filters (dict): Query parameters from request

        Returns:
            QuerySet[Product]: Filtered list of products

        Raises:
            ValueError: If category IDs are invalid
        """
        query = Product.objects()

        # Filter by categories (multiple)
        category_ids = filters.get("categories")
        if category_ids:
            try:
                object_ids = [ObjectId(cid) for cid in category_ids.split(",")]
            except InvalidId:
                raise ValueError("Invalid category ID in filters")

            query = query.filter(categories__in=object_ids)

        # Filter by brand
        if filters.get("brand_id"):
            query = query.filter(brand=filters["brand_id"])

        # Filter by product name (case-insensitive search)
        if filters.get("name"):
            query = query.filter(name__icontains=filters["name"])

        return query

    @staticmethod
    def create_product(data):
        """
        Create a new product with validation.

        Args:
            data (dict): Product data (name, brand_id)

        Returns:
            Product: Created product object

        Raises:
            ValueError:
                - If name is missing or empty
                - If brand_id is missing or invalid
                - If brand does not exist
                - If duplicate product exists
        """
        name = data.get("name")
        brand_id = data.get("brand_id")

    
        if not name or not name.strip():
            raise ValueError("Product name is required")

  
        if not brand_id:
            raise ValueError("Brand ID is required")

       
        try:
            object_id = ObjectId(brand_id)
        except InvalidId:
            raise ValueError("Invalid brand ID")

        brand = Brand.objects(id=object_id).first()
        if not brand:
            raise ValueError("Brand not found")

        existing = Product.objects(name=name, brand=brand).first()
        if existing:
            raise ValueError("Duplicate product")

     
        product = Product(name=name.strip(), brand=brand)

        return ProductRepository.save(product)

    @staticmethod
    def bulk_upload(csv_reader):
        """
        Bulk upload products from CSV input.

        Each row must contain:
            - name
            - brand_id

        Args:
            csv_reader (iterator): CSV DictReader object

        Returns:
            dict:
                {
                    "created": int,   # number of successfully created products
                    "errors": list    # list of error messages per row
                }

        Behavior:
            - Skips invalid rows
            - Collects errors instead of failing entire upload
            - Inserts valid products in bulk

        Raises:
            None (errors are collected instead)
        """
        products = []
        errors = []

        for index, row in enumerate(csv_reader, start=1):

            name = row.get("name")
            brand_id = row.get("brand_id")

          
            if not name or not brand_id:
                errors.append(f"Row {index}: Missing name or brand_id")
                continue

          
            try:
                object_id = ObjectId(brand_id)
            except InvalidId:
                errors.append(f"Row {index}: Invalid brand_id")
                continue

          
            brand = Brand.objects(id=object_id).first()
            if not brand:
                errors.append(f"Row {index}: Brand not found")
                continue

        
            products.append(Product(
                name=name.strip(),
                brand=brand
            ))

        if products:
            ProductRepository.bulk_insert(products)

        return {
            "created": len(products),
            "errors": errors
        }