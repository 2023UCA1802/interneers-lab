from mongoengine import Document, StringField, ReferenceField, ListField, ValidationError


class Brand(Document):
    """
    Represents a product brand.

    Fields:
        name (str): Unique brand name
        description (str): Description of the brand

    Constraints:
        - name must be unique
        - description is required
    """
    name = StringField(required=True, unique=True)
    description = StringField(required=True)


class ProductCategory(Document):
    """
    Represents a product category.

    Fields:
        name (str): Unique category name
        description (str): Description of the category

    Constraints:
        - name must be unique
        - description is required
    """
    name = StringField(required=True, unique=True)
    description = StringField(required=True)


class Product(Document):
    """
    Represents a product in the inventory.

    Fields:
        name (str): Product name
        brand (Brand): Reference to the brand (required)
        categories (list[ProductCategory]): List of categories the product belongs to

    Behavior:
        - A product must always have a brand
        - Categories can be assigned later (optional)

    Relationships:
        - Many-to-One: Product → Brand
        - Many-to-Many: Product ↔ Categories
    """
    name = StringField(required=True)

    brand = ReferenceField(Brand, required=True)

    categories = ListField(
        ReferenceField(ProductCategory)
    )
    
    meta = {
    "indexes": ["name", "brand", "categories"]
    }


      