from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository
from bson import ObjectId
from bson.errors import InvalidId

class CategoryService:

    @staticmethod
    def create_category(data):
       
        name = data.get("name")
        if not name or not name.strip():
            raise ValueError("Category name is required")

        existing = CategoryRepository.get_all().filter(name=name).first()
        if existing:
            raise ValueError("Category with this name already exists")

        return CategoryRepository.create(data)

    
    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()
    

    @staticmethod
    def update_category(category_id, data):
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found")

        if "name" in data and not data["name"].strip():
            raise ValueError("Name cannot be empty")

        return CategoryRepository.update(category_id, data)
    

    @staticmethod
    def delete_category(category_id):
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found")

        CategoryRepository.delete(category_id)


    @staticmethod
    def get_products(category_id):
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found")

        return ProductRepository.get_by_category(category)
    

    @staticmethod
    def add_product(category_id, product):
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
    
    
