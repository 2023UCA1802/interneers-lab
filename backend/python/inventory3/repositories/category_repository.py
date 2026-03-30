from ..models import Product,ProductCategory

class CategoryRepository:
    
    @staticmethod
    def create(data):
        return ProductCategory(**data).save()
    
    @staticmethod
    def get_all():
        return ProductCategory.objects()
    
    @staticmethod
    def get_by_id(category_id):
        return ProductCategory.objects.get(id=category_id)
    
    @staticmethod
    def update(category_id, data):
        category=ProductCategory.objects.get(id=category_id)
        category.update(**data)
        category.reload()
        return category
    
    @staticmethod
    def delete(category_id):
        ProductCategory.objects(id=category_id).delete()
    
    