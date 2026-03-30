from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository

class CategoryService:

    @staticmethod
    def create_category(data):
        return CategoryRepository.create(data)
    
    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()
    
    @staticmethod
    def update_category(category_id,data):
        return CategoryRepository.update(category_id,data)
    
    @staticmethod
    def delete_category(category_id):
        CategoryRepository.delete(category_id)

    @staticmethod
    def get_products(category_id):
        category = CategoryRepository.get_by_id(category_id)
        return ProductRepository.get_by_category(category)
    
    @staticmethod
    def add_product(category_id,product):
        category = CategoryRepository.get_by_id(category_id)
        
        if category not in product.categories:
            product.categories.append(category)
            ProductRepository.save(product)
    
    @staticmethod
    def remove_product(category_id,product):
        category = CategoryRepository.get_by_id(category_id)

        if category in product.categories:
            product.categories.remove(category)
            ProductRepository.save(product)
    
    
