from mongoengine.errors import ValidationError
from ..models import Product, Brand
from ..repositories.product_repository import ProductRepository
from bson import ObjectId
from bson.errors import InvalidId


class ProductService:

    @staticmethod
    def create_product(data):
        name = data.get("name")
        brand_id = data.get("brand_id")

        if not name or not name.strip():
            raise ValueError("Product name is required")

        if not brand_id:
            raise ValueError("Brand ID is required")

        try:
            object_id = ObjectId(brand_id)
        except InvalidId:
            raise ValueError("Invalid brand ID")

        brand = Brand.objects(id=object_id).first()

        if not brand:
            raise ValueError("Brand not found")

        existing = Product.objects(name=name, brand=brand).first()
        if existing:
            raise ValueError("Duplicate product")

        product = Product(name=name.strip(), brand=brand)

        return ProductRepository.save(product)

    @staticmethod
    def bulk_upload(csv_reader):
        products = []
        errors = []
        
        
        from bson import ObjectId
        from bson.errors import InvalidId

        for index, row in enumerate(csv_reader, start=1):

            name = row.get("name")
            brand_id = row.get("brand_id")

            if not name or not brand_id:
                errors.append(f"Row {index}: Missing name or brand_id")
                continue

            try:
                object_id = ObjectId(brand_id)
            except InvalidId:
                errors.append(f"Row {index}: Invalid brand_id")
                continue

            brand = Brand.objects(id=object_id).first()

            if not brand:
                errors.append(f"Row {index}: Brand not found")
                continue

            products.append(Product(
                name=name.strip(),
                brand=brand
            ))
        if products:
            ProductRepository.bulk_insert(products)

        return {
            "created": len(products),
            "errors": errors
        }