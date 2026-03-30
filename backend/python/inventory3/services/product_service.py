from ..models import Product, Brand
from ..repositories.product_repository import ProductRepository

class ProductService:

    @staticmethod
    def create_product(data):
        brand = Brand.objects(id=data.get("brand_id")).first()

        if not brand:
            raise Exception("Brand is required")
        
        product = Product(name = data.get("name"), brand=brand)

        return ProductRepository.save(product)
    
    @staticmethod
    def bulk_upload(csv_reader):
        products=[]

        for row in csv_reader:
            brand = Brand.objects(id.row.get("brand_id")).first()

            if not brand:
                continue

            products.append(Product(name=row.get("name"), brand=brand))

        return ProductRepository.bulk_insert(products)
    