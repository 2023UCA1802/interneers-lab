from django.db import models
from mongoengine import Document,StringField,FloatField,IntField,DateTimeField
import datetime

class Product(Document):
    """
    Product Document Model

    This model represents a product stored in MongoDB using MongoEngine.
    It contains basic product details such as name, description, category,
    brand, price, and quantity along with audit timestamps.

    Attributes:
        name (str): Name of the product.
        description (str): Short description of the product.
        category (str): Category to which the product belongs.
        brand (str): Brand name of the product.
        price (float): Price of the product (must be non-negative).
        quantity (int): Available stock quantity (must be non-negative).
        created_at (datetime): Timestamp when the product was created.
        updated_at (datetime): Timestamp when the product was last updated.
    """

    name = StringField(
        required=True,
        max_length=255,
        default="",
        help_text="Name of the product"
    )

    description = StringField(
        required=True,
        max_length=255,
        default="",
        help_text="Short description of the product"
    )

    category = StringField(
        required=True,
        max_length=255,
        default="",
        help_text="Category of the product (e.g., Electronics, Food)"
    )

    brand = StringField(
        required=True,
        max_length=255,
        default="",
        help_text="Brand of the product"
    )

    price = FloatField(
        required=True,
        default=0,
        help_text="Price of the product (must be >= 0)"
    )

    quantity = IntField(
        required=True,
        default=0,
        help_text="Available stock quantity (must be >= 0)"
    )

    created_at = DateTimeField(
        default=datetime.datetime.utcnow,
        help_text="Timestamp when the product was created"
    )

    updated_at = DateTimeField(
        default=datetime.datetime.utcnow,
        help_text="Timestamp when the product was last updated"
    )

    meta = {
        "collection": "products",
        "indexes": [
            "-created_at",   # Sort by newest first
            "-updated_at",   # Recently updated products
            "price",         # Filter/sort by price
            "name",          # Search by name
            "category",      # Filter by category
            "brand"          # Filter by brand
        ]
    }

    def save(self, *args, **kwargs):
        """
        Override save method to update the 'updated_at' timestamp.

        This ensures that every time a product is saved or updated,
        the 'updated_at' field reflects the current UTC time.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Product: The saved product instance.
        """
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)