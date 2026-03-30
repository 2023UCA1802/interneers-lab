from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository
from bson import ObjectId
from bson.errors import InvalidId


class CategoryService:
    """
    Service layer for handling business logic related to ProductCategory.

    This layer validates input, enforces business rules, and interacts
    with the repository layer for database operations.
    """

    @staticmethod
    def create_category(data):
        """
        Create a new category with validation.

        Args:
            data (dict): Category data (name, description)

        Returns:
            ProductCategory: Created category object

        Raises:
            ValueError: If name is missing or duplicate
        """
        name = data.get("name")

        if not name or not name.strip():
            raise ValueError("Category name is required")

        existing = CategoryRepository.get_all().filter(name=name).first()
        if existing:
            raise ValueError("Category with this name already exists")

        return CategoryRepository.create(data)

    @staticmethod
    def get_all_categories():
        """
        Retrieve all categories.

        Returns:
            QuerySet[ProductCategory]: List of all categories
        """
        return CategoryRepository.get_all()

    @staticmethod
    def update_category(category_id, data):
        """
        Update an existing category.

        Args:
            category_id (str/ObjectId): Category identifier
            data (dict): Fields to update

        Returns:
            ProductCategory: Updated category

        Raises:
            ValueError: If category not found or invalid data
        """
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found")

        if "name" in data and not data["name"].strip():
            raise ValueError("Name cannot be empty")

        return CategoryRepository.update(category_id, data)

    @staticmethod
    def delete_category(category_id):
        """
        Delete a category.

        Args:
            category_id (str/ObjectId): Category identifier

        Raises:
            ValueError: If category does not exist
        """
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found")

        CategoryRepository.delete(category_id)

    @staticmethod
    def get_products(category_id):
        """
        Get all products belonging to a category.

        Args:
            category_id (str/ObjectId): Category identifier

        Returns:
            QuerySet[Product]: Products in category

        Raises:
            ValueError: If category not found
        """
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found")

        return ProductRepository.get_by_category(category)

    @staticmethod
    def add_product(category_id, product):
        """
        Add a product to a category.

        Args:
            category_id (str): Category ID
            product (Product): Product instance

        Raises:
            ValueError: If invalid ID, category not found, or duplicate relation
        """
        try:
            object_id = ObjectId(category_id)
        except InvalidId:
            raise ValueError("Invalid category ID")

        category = CategoryRepository.get_by_id(object_id)

        if not category:
            raise ValueError("Category not found")

        if category in product.categories:
            raise ValueError("Product already in category")

        product.categories.append(category)
        ProductRepository.save(product)

    @staticmethod
    def remove_product(category_id, product):
        """
        Remove a product from a category.

        Args:
            category_id (str): Category ID
            product (Product): Product instance

        Raises:
            ValueError: If invalid ID, category not found, or relation missing
        """
        try:
            object_id = ObjectId(category_id)
        except InvalidId:
            raise ValueError("Invalid category ID")

        category = CategoryRepository.get_by_id(object_id)

        if not category:
            raise ValueError("Category not found")

        if category not in product.categories:
            raise ValueError("Product is not in this category")

        product.categories.remove(category)
        ProductRepository.save(product)