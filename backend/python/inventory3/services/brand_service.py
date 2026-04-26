from ..models import Brand
from ..repositories.brand_repository import BrandRepository


class BrandService:
    """
    Service layer for handling Brand-related business logic.

    Responsibilities:
    - Validate input data
    - Prevent duplicates
    - Coordinate with repository layer
    """

    @staticmethod
    def get_all_brands():
        """
        Retrieve all brands.

        Returns:
            QuerySet[Brand]: All brand documents
        """
        return BrandRepository.get_all()

    @staticmethod
    def create_brand(data):
        """
        Create a new brand with validation.

        Args:
            data (dict): Brand data (name, description)

        Returns:
            Brand: Created brand object

        Raises:
            ValueError: If name/description is missing, or brand already exists
        """
        name = data.get("name")
        description = data.get("description")

        if not name or not name.strip():
            raise ValueError("Brand name is required")

        if not description or not description.strip():
            raise ValueError("Brand description is required")

        if Brand.objects(name=name.strip()).first():
            raise ValueError("A brand with this name already exists")

        return BrandRepository.create({"name": name.strip(), "description": description.strip()})

    @staticmethod
    def update_brand(brand_id, data):
        """
        Update an existing brand.

        Args:
            brand_id (str): ID of the brand to update
            data (dict): Fields to update

        Returns:
            Brand: Updated brand document

        Raises:
            DoesNotExist: If brand not found
        """
        update_fields = {}
        if data.get("name"):
            update_fields["set__name"] = data["name"].strip()
        if data.get("description"):
            update_fields["set__description"] = data["description"].strip()
        return BrandRepository.update(brand_id, update_fields)

    @staticmethod
    def delete_brand(brand_id):
        """
        Delete a brand by ID.

        Args:
            brand_id (str): ID of the brand to delete
        """
        BrandRepository.delete(brand_id)
