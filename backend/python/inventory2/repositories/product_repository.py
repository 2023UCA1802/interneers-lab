from ..models import Product
from bson import ObjectId
from bson.errors import InvalidId

class ProductRepository:

    @staticmethod
    def get_all(filters=None):
        query = Product.objects()

        if filters:
            if filters.get("updated_after"):
                query = query.filter(updated_at__gt=filters["updated_after"])

            if filters.get("sort") == "latest":
                query = query.order_by("-created_at")

        return list(query)

    @staticmethod
    def get_by_id(product_id):
        try:
            ObjectId(product_id)
        except (InvalidId, TypeError):
            return None

        return Product.objects(id=product_id).first()

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product_id, data):
        try:
            ObjectId(product_id)
        except (InvalidId, TypeError):
            return None

        product = Product.objects(id=product_id).first()
        if not product:
            return None

        for key, value in data.items():
            setattr(product, key, value)

        product.save()
        return product

    @staticmethod
    def delete(product_id):
        try:
            ObjectId(product_id)
        except (InvalidId, TypeError):
            return False

        product = Product.objects(id=product_id).first()
        if not product:
            return False

        product.delete()
        return True
    
    @staticmethod
    def find_duplicate(data):
        return Product.objects(
            name=data["name"],
            category=data["category"],
            brand=data["brand"],
            price=data["price"]
        ).first()