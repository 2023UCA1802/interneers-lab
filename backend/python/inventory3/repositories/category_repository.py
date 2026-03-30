from ..models import Product, ProductCategory


class CategoryRepository:
    """
    Repository layer for handling ProductCategory database operations.

    This class abstracts direct database interactions using MongoEngine
    and provides a clean interface for the service layer.
    """

    @staticmethod
    def create(data):
        """
        Create a new product category.

        Args:
            data (dict): Dictionary containing category fields
                         (e.g., name, description)

        Returns:
            ProductCategory: The created category document

        Raises:
            ValidationError: If required fields are missing or invalid
        """
        return ProductCategory(**data).save()

    @staticmethod
    def get_all():
        """
        Retrieve all product categories.

        Returns:
            QuerySet[ProductCategory]: List of all categories
        """
        return ProductCategory.objects()

    @staticmethod
    def get_by_id(category_id):
        """
        Retrieve a category by its ID.

        Args:
            category_id (str or ObjectId): Unique identifier of the category

        Returns:
            ProductCategory: The matching category document

        Raises:
            DoesNotExist: If category is not found
            ValidationError: If ID format is invalid
        """
        return ProductCategory.objects.get(id=category_id)

    @staticmethod
    def update(category_id, data):
        """
        Update an existing category.

        Args:
            category_id (str or ObjectId): ID of the category to update
            data (dict): Fields to update

        Returns:
            ProductCategory: Updated category document

        Raises:
            DoesNotExist: If category does not exist
        """
        category = ProductCategory.objects.get(id=category_id)
        category.update(**data)
        category.reload()
        return category

    @staticmethod
    def delete(category_id):
        """
        Delete a category by its ID.

        Args:
            category_id (str or ObjectId): ID of the category

        Returns:
            None

        Note:
            This performs a hard delete from the database.
        """
        ProductCategory.objects(id=category_id).delete()