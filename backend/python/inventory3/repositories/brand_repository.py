from ..models import Brand


class BrandRepository:
    """
    Repository layer for handling Brand-related database operations.

    This class abstracts MongoEngine queries and provides a clean
    interface for the service layer.
    """

    @staticmethod
    def create(data):
        """
        Create a new brand.

        Args:
            data (dict): Dictionary containing brand fields (name, description)

        Returns:
            Brand: The created brand document
        """
        return Brand(**data).save()

    @staticmethod
    def get_all():
        """
        Retrieve all brands.

        Returns:
            QuerySet[Brand]: List of all brands
        """
        return Brand.objects()

    @staticmethod
    def get_by_id(brand_id):
        """
        Retrieve a brand by its ID.

        Args:
            brand_id (str or ObjectId): Unique brand identifier

        Returns:
            Brand: The matching brand document

        Raises:
            DoesNotExist: If brand is not found
        """
        return Brand.objects.get(id=brand_id)

    @staticmethod
    def update(brand_id, data):
        """
        Update an existing brand.

        Args:
            brand_id (str or ObjectId): ID of the brand to update
            data (dict): Fields to update

        Returns:
            Brand: Updated brand document

        Raises:
            DoesNotExist: If brand does not exist
        """
        brand = Brand.objects.get(id=brand_id)
        brand.update(**data)
        brand.reload()
        return brand

    @staticmethod
    def delete(brand_id):
        """
        Delete a brand by its ID.

        Args:
            brand_id (str or ObjectId): ID of the brand

        Returns:
            None
        """
        Brand.objects(id=brand_id).delete()
