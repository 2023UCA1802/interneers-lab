from ..repositories.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def get_all_products(params):
        return ProductRepository.get_all(params)

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def create_product(data):
        data["name"] = data["name"].strip()
        data["category"] = data.get("category", "").lower()
        data["brand"] = data.get("brand", "").lower()

        if data.get("price", 0) < 0:
            raise ValueError("Price cannot be negative")
        
        if data.get("quantity", 0) < 0:
            raise ValueError("Quantity cannot be negative")

        return ProductRepository.create(data)

    @staticmethod
    def update_product(product_id, data):
        return ProductRepository.update(product_id, data)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete(product_id)