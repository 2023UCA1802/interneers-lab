from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from inventory2.services.product_service import ProductService
from inventory2.models import Product
from types import SimpleNamespace

class ProductValidationTestCase(TestCase):

    def setUp(self):
        self.client=APIClient()

    # Test case for success in creating product
    def test_create_product_success(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": 10
        }

        product= ProductService.create_product(data)
        self.assertEqual(product.name,"Laptop")
        self.assertEqual(product.description,"Gaming laptop")
        self.assertEqual(product.category,"Electronics")
        self.assertEqual(product.brand,"Dell")
        self.assertEqual(product.price,50000)
        self.assertEqual(product.quantity,10)

    def test_create_product_noarguments(self):

        data={}

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    def test_create_product_twoarguments(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for negative price error
    def test_create_product_invalid_price(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": -50000,
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for negative quantity error
    def test_create_product_invalid_quantity(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": -10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for price value equal to 0
    def test_create_product_edgecase_price(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 0,
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for quantity equal to 0
    def test_create_product_edgecase_quantity(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": 0
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for missing brand
    def test_create_product_missing_brand(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "price": 50000,
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for missing category
    def test_create_product_missing_category(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",          
            "brand": "Dell",
            "price": 50000,
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for missing name
    def test_create_product_missing_name(self):

        data={
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for missing description
    def test_create_product_missing_description(self):

        data={
            "name": "Laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for missing price
    def test_create_product_missing_price(self):
        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "quantity": 10
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)

    # Test case for missing quantity
    def test_create_product_missing_quantity(self):

        data={
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
        }

        with self.assertRaises(ValueError):
           ProductService.create_product(data)
    
    

    def test_duplicate_product(self):

        data = {
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 20000,
            "quantity": 50
        }

        # Create first product
        ProductService.create_product(data)

        # Try duplicate
        with self.assertRaises(ValueError):
            ProductService.create_product(data)
            
    def tearDown(self):
        Product.objects.delete()



class ProductAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        response = self.client.post("/products/", {
            "name": "Laptop",
            "description": "Enterprise laptop",
            "category": "Electronics",
            "brand": "Asus",
            "price": 40000,
            "quantity": 1
        }, content_type="application/json")

        self.product_id = response.json()["id"]

    def tearDown(self):
        Product.objects.delete()

    # Test case for Getting all products
    def test_get_all_products(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)
    
    # Test case for getting single product
    def test_get_single_product(self):
        response = self.client.get(f"/products/{self.product_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.product_id)

    # Test case for getting error for entering invalid id
    def test_get_invalid_product(self):
        response = self.client.get("/products/invalid_id/")

        self.assertIn(response.status_code, [400, 404])
    
    # Test cases for updating product
    def test_update_product(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "name": "Updated Laptop",
                "description": "Updated desc",
                "category": "Electronics",
                "brand": "Dell",
                "price": 45000,
                "quantity": 8
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")

    
    def test_update_product_missing_description(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "name": "Updated Laptop",
                "category": "Electronics",
                "brand": "Dell",
                "price": 45000,
                "quantity": 8
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")

  
    def test_update_product_missing_name(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "description": "Updated desc",
                "category": "Electronics",
                "brand": "Dell",
                "price": 45000,
                "quantity": 8
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Updated desc")

   
    def test_update_product_missing_quantity(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "name": "Updated Laptop",
                "description": "Updated desc",
                "category": "Electronics",
                "brand": "Dell",
                "price": 45000,
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")

   
    def test_update_product_missing_price(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "name": "Updated Laptop",
                "description": "Updated desc",
                "category": "Electronics",
                "brand": "Dell",
                "quantity": 8
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")

   
    def test_update_product_missing_brand(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "name": "Updated Laptop",
                "description": "Updated desc",
                "category": "Electronics",
                "price": 45000,
                "quantity": 8
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")

  
    def test_update_product_missing_category(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "name": "Updated Laptop",
                "description": "Updated desc",
                "brand": "Dell",
                "price": 45000,
                "quantity": 8
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")
    
    # Test case for updating invalid price
    def test_update_invalid_price(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "price": -100
            },
            content_type="application/json"
        )

        self.assertIn(response.status_code, [400, 422])

    # Test case for updating edgecase price
    def test_update_edgecase_price(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "price": 0
            },
            content_type="application/json"
        )

        self.assertIn(response.status_code, [400, 422])

    # Test case for updating invalid quantity
    def test_update_invalid_quantity(self):
        response = self.client.put(
            f"/products/{self.product_id}/",
            {
                "quantity": -100
            },
            content_type="application/json"
        )

        self.assertIn(response.status_code, [400, 422])
    
    # Test case for deleting product
    def test_delete_product(self):
        response = self.client.delete(f"/products/{self.product_id}/")

        self.assertEqual(response.status_code, 200)


        get_response = self.client.get(f"/products/{self.product_id}/")
        self.assertIn(get_response.status_code, [400, 404])
    
    # Test case for deleting invalid product
    def test_delete_invalid_product(self):
        response = self.client.delete("/products/invalid_id/")

        self.assertIn(response.status_code, [400, 404])



class ProductServiceMockTest(TestCase):

    # MOCK SUCCESS CASE
    @patch("inventory2.services.product_service.ProductRepository.create")
    @patch("inventory2.services.product_service.ProductRepository.find_duplicate")
    def test_create_product_success(self, mock_filter, mock_create):

        data = {
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": 10
        }

        # STUB: No duplicate
        mock_filter.return_value = None

        # STUB: Fake product
        mock_product = SimpleNamespace(**data)
        mock_create.return_value = mock_product

        result = ProductService.create_product(data)

        self.assertEqual(result.name, "Laptop")
        self.assertEqual(result.price, 50000)

        mock_filter.assert_called_once()
        mock_create.assert_called_once()


    # DUPLICATE PRODUCT
    @patch("inventory2.services.product_service.ProductRepository.find_duplicate")
    def test_duplicate_product(self, mock_filter):

        data = {
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 20000,
            "quantity": 50
        }

        # STUB: Product already exists
        mock_filter.return_value.exists.return_value = True

        with self.assertRaises(ValueError):
            ProductService.create_product(data)

        mock_filter.assert_called_once()