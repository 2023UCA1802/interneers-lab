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

        required_fields = ["name", "description", "category", "brand", "price", "quantity"]

        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                raise ValueError(f"{field} is required")

        data["name"] = data["name"].strip()
        data["description"] = data["description"].strip()
        data["category"] = data["category"].strip()
        data["brand"] = data["brand"].strip()

    
        existing = ProductRepository.find_duplicate(data)
        if existing:
            raise ValueError("Duplicate product already exists")

        if data["price"] <= 0:
            raise ValueError("Price must be greater than 0")

        if data["quantity"] <= 0:
            raise ValueError("Quantity must be greater than 0")

        return ProductRepository.create(data)

    @staticmethod
    def update_product(product_id, data):

        if "name" in data:
            data["name"] = data["name"].strip()

        if "description" in data:
            data["description"] = data["description"].strip()

        if "category" in data:
            data["category"] = data["category"].strip()

        if "brand" in data:
            data["brand"] = data["brand"].strip()

      
        check_fields = ["name", "category", "brand", "price"]
        if all(field in data for field in check_fields):
            existing = ProductRepository.find_duplicate(data)
            if existing and str(existing.id) != str(product_id):
                raise ValueError("Duplicate product already exists")

        if "price" in data and data["price"] <= 0:
            raise ValueError("Price must be greater than 0")

        if "quantity" in data and data["quantity"] < 0:
            raise ValueError("Quantity must be greater than 0")

        return ProductRepository.update(product_id, data)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete(product_id)