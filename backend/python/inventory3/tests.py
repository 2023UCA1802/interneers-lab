import unittest
from inventory3.services.product_service import ProductService
from inventory3.services.category_service import CategoryService
from inventory3.models import Product, Brand, ProductCategory


class ProductValidationTestCase(unittest.TestCase):

    def setUp(self):
        Product.drop_collection()
        Brand.drop_collection()

        self.brand = Brand(
            name="Nike",
            description="Sports brand"
        ).save()

    def tearDown(self):
        Product.drop_collection()
        Brand.drop_collection()

    def test_create_product_success(self):
        data = {
            "name": "Shoes",
            "brand_id": str(self.brand.id)
        }

        product = ProductService.create_product(data)

        self.assertEqual(product.name, "Shoes")
        self.assertEqual(product.brand.id, self.brand.id)

    def test_missing_name(self):
        with self.assertRaises(ValueError):
            ProductService.create_product({
                "brand_id": str(self.brand.id)
            })

    def test_missing_brand(self):
        with self.assertRaises(ValueError):
            ProductService.create_product({
                "name": "Shoes"
            })

    def test_invalid_brand(self):
        with self.assertRaises(ValueError):
            ProductService.create_product({
                "name": "Shoes",
                "brand_id": "invalid_id"
            })

    def test_duplicate_product(self):
        data = {
            "name": "Shoes",
            "brand_id": str(self.brand.id)
        }

        ProductService.create_product(data)

        with self.assertRaises(ValueError):
            ProductService.create_product(data)

class ProductBulkUploadTest(unittest.TestCase):

    def setUp(self):
        Product.drop_collection()
        Brand.drop_collection()

        self.brand = Brand(
            name="Adidas",
            description="Sports brand"
        ).save()

    def tearDown(self):
        Product.drop_collection()
        Brand.drop_collection()

    def test_bulk_upload_success(self):
        rows = [
            {"name": "A", "brand_id": str(self.brand.id)},
            {"name": "B", "brand_id": str(self.brand.id)}
        ]

        result = ProductService.bulk_upload(rows)

        self.assertEqual(result["created"], 2)
        self.assertEqual(len(result["errors"]), 0)

    def test_bulk_upload_with_errors(self):
        rows = [
            {"name": "A", "brand_id": str(self.brand.id)},
            {"name": "", "brand_id": str(self.brand.id)},   
            {"name": "C", "brand_id": "wrong"}              
        ]

        result = ProductService.bulk_upload(rows)

        self.assertEqual(result["created"], 1)
        self.assertEqual(len(result["errors"]), 2)


class CategoryValidationTest(unittest.TestCase):

    def setUp(self):
        ProductCategory.drop_collection()

    def tearDown(self):
        ProductCategory.drop_collection()

    def test_create_category_success(self):
        data = {"name": "Food", "description":"Test category"}
        category = CategoryService.create_category(data)

        self.assertEqual(category.name, "Food")

    def test_missing_name(self):
        with self.assertRaises(ValueError):
            CategoryService.create_category({})

    def test_duplicate_category(self):
        CategoryService.create_category({"name": "Food", "description":"test"})

        with self.assertRaises(ValueError):
            CategoryService.create_category({"name": "Food", "description":"test"})


class CategoryProductRelationTest(unittest.TestCase):

    def setUp(self):
        Product.drop_collection()
        Brand.drop_collection()
        ProductCategory.drop_collection()

        self.brand = Brand(name="Puma", description="test brand").save()
        self.category = ProductCategory(name="Sports", description="Test category").save() 
        self.product = Product(name="T-shirt", brand=self.brand).save()

    def test_add_product_success(self):
        CategoryService.add_product(self.category.id, self.product)

        updated = Product.objects.get(id=self.product.id)
        self.assertIn(self.category, updated.categories)

    def test_add_duplicate_product(self):
        CategoryService.add_product(self.category.id, self.product)

        with self.assertRaises(ValueError):
            CategoryService.add_product(self.category.id, self.product)

    def test_remove_product_success(self):
        CategoryService.add_product(self.category.id, self.product)
        CategoryService.remove_product(self.category.id, self.product)

        updated = Product.objects.get(id=self.product.id)
        self.assertNotIn(self.category, updated.categories)

    def test_remove_non_existing_relation(self):
        with self.assertRaises(ValueError):
            CategoryService.remove_product(self.category.id, self.product)

    def test_add_product_invalid_category(self):
        with self.assertRaises(ValueError):
            CategoryService.add_product("invalid_id", self.product)

