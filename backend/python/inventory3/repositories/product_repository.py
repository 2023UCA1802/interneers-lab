from ..models import Product,ProductCategory

class ProductRepository:

    @staticmethod
    def get_by_id(product_id):
        return Product.objects.get(id=product_id)

    @staticmethod
    def get_by_category(category_id):
        return Product.objects(categories=category_id)
    
    @staticmethod
    def save(product):
        return product.save()
    
    @staticmethod
    def bulk_insert(products):
        return Product.objects.insert(products,load_bulk=False)
    
    

     
    @staticmethod
    def add_products_to_category(category_id, product_id):
        product=Product.objects.get(id=product_id)
        category=ProductCategory.objects.get(id=category_id)
        
        if category not in product.categories():
            product.categories.append(category)
            product.save()
        
    @staticmethod
    def remove_products_from_category(category_id,product_id):
        product=Product.objects.get(id=product_id)
        category=ProductCategory.objects.get(id=category_id)

        if category in product.categories():
            product.categories.remove(category)
            product.save()




