from django.test import TestCase
from rest_framework.test import APIClient
from inventory.views import products


class ProductAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        response = self.client.post("/week2/products/create/", {
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 50000,
            "quantity": 10
        }, format="json")

        # Ensure setup worked
        self.assertEqual(response.status_code, 201)
        self.product_id = response.json()["data"]["id"]

    def tearDown(self):
        products.clear()

    #  CREATE
    def test_create_product_success(self):
        response = self.client.post("/week2/products/create/", {
            "name": "Phone",
            "description": "Gaming laptop",
            "category": "Electronics",
            "brand": "Dell",
            "price": 20000,
            "quantity": 5,
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "success")

    #  CREATE INVALID
    def test_create_product_invalid(self):
        response = self.client.post("/week2/products/create/", {
            "price": -100
        }, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

    # GET ALL
    def test_get_products(self):
        response = self.client.get("/week2/products/get/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    # INVALID PAGINATION
    def test_get_products_invalid_pagination(self):
        response = self.client.get("/week2/products/get/?page=abc")

        self.assertEqual(response.status_code, 400)

    # GET SINGLE
    def test_get_single_product(self):
        response = self.client.get(f"/week2/products/{self.product_id}/get/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["id"], self.product_id)

    # GET INVALID
    def test_get_invalid_product(self):
        response = self.client.get("/week2/products/999/get/")

        self.assertEqual(response.status_code, 404)

    #  UPDATE
    def test_update_product(self):
        response = self.client.put(
            f"/week2/products/{self.product_id}/update/",
            {
                "name": "Updated Laptop",
                "description": "Gaming laptop",
                "category": "Electronics",
                "brand": "Dell",
                "price": 45000,
                "quantity": 8
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Laptop")

    # UPDATE INVALID DATA
    def test_update_invalid_product(self):
        response = self.client.put(
            f"/week2/products/{self.product_id}/update/",
            {
                "price": -100
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    # UPDATE NON-EXISTENT
    def test_update_nonexistent_product(self):
        response = self.client.put(
            "/week2/products/999/update/",
            {
                "name": "Test",
                "price": 100
            },
            format="json"
        )

        self.assertEqual(response.status_code, 404)

    # DELETE
    def test_delete_product(self):
        response = self.client.delete(f"/week2/products/{self.product_id}/delete/")

        self.assertEqual(response.status_code, 200)

        # Verify deletion
        get_response = self.client.get(f"/week2/products/{self.product_id}/")
        self.assertEqual(get_response.status_code, 404)

    #  DELETE INVALID
    def test_delete_invalid_product(self):
        response = self.client.delete("/week2/products/999/delete/")

        self.assertEqual(response.status_code, 404)