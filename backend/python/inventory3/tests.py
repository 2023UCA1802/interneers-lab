import unittest
from parameterized import parameterized
from inventory3.services.product_service import ProductService
from inventory3.services.category_service import CategoryService
from inventory3.models import Product, Brand, ProductCategory
from unittest.mock import patch, MagicMock
from types import SimpleNamespace



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


class ProductServiceMockTest(unittest.TestCase):

    @patch("inventory3.services.product_service.ProductRepository.save")
    @patch("inventory3.services.product_service.Product.objects")
    @patch("inventory3.services.product_service.Brand.objects")
    def test_create_product_success(self, mock_brand, mock_product, mock_save):

        data = {
            "name": "Shoes",
            "brand_id": "507f1f77bcf86cd799439011"
        }

        mock_brand.return_value.first.return_value = SimpleNamespace(id="123")

   
        mock_product.return_value.first.return_value = None

        mock_save.return_value = SimpleNamespace(name="Shoes", brand=SimpleNamespace(id="123"))

        result = ProductService.create_product(data)

        self.assertEqual(result.name, "Shoes")
        mock_save.assert_called_once()

    @patch("inventory3.services.product_service.Product.objects")
    @patch("inventory3.services.product_service.Brand.objects")
    def test_duplicate_product(self, mock_brand, mock_product):

        data = {
            "name": "Shoes",
            "brand_id": "123"
        }

        mock_brand.return_value.first.return_value = MagicMock()

        mock_product.return_value.first.return_value = MagicMock()

        with self.assertRaises(ValueError):
            ProductService.create_product(data)
    
    @patch("inventory3.services.product_service.Brand.objects")
    def test_invalid_brand(self, mock_brand):

        data = {
            "name": "Shoes",
            "brand_id": "123"
        }

        mock_brand.return_value.first.return_value = None

        with self.assertRaises(ValueError):
            ProductService.create_product(data)

class CategoryServiceMockTest(unittest.TestCase):

    @patch("inventory3.services.category_service.CategoryRepository.create")
    @patch("inventory3.services.category_service.CategoryRepository.get_all")
    def test_create_category_success(self, mock_get_all, mock_create):

        data = {
            "name": "Food",
            "description": "All food"
        }

        mock_get_all.return_value.filter.return_value.first.return_value = None

        mock_create.return_value = SimpleNamespace(**data)

        result = CategoryService.create_category(data)

        self.assertEqual(result.name, "Food")
        mock_create.assert_called_once()
    
    @patch("inventory3.services.category_service.CategoryRepository.get_all")
    def test_duplicate_category(self, mock_get_all):

        mock_get_all.return_value.filter.return_value.first.return_value = MagicMock()

        with self.assertRaises(ValueError):
            CategoryService.create_category({
                "name": "Food",
                "description": "All food"
            })

class ProductBulkMockTest(unittest.TestCase):

    @patch("inventory3.services.product_service.ProductRepository.bulk_insert")
    @patch("inventory3.services.product_service.Brand")
    def test_bulk_upload_success(self, mock_brand, mock_bulk):

        valid_id = "507f1f77bcf86cd799439011"

        rows = [
            {"name": "A", "brand_id": valid_id},
            {"name": "B", "brand_id": valid_id}
        ]

        mock_brand.objects.return_value.first.return_value = MagicMock()

        result = ProductService.bulk_upload(rows)

        self.assertEqual(result["created"], 2)
        self.assertEqual(len(result["errors"]), 0)
        mock_bulk.assert_called_once()



class CategoryServiceUnitTest(unittest.TestCase):

    # 1. Create Category Success
    @patch("inventory3.services.category_service.CategoryRepository.create")
    @patch("inventory3.services.category_service.CategoryRepository.get_all")
    def test_create_category_success(self, mock_get_all, mock_create):

        data = {"name": "Food", "description": "All food"}

        mock_get_all.return_value.filter.return_value.first.return_value = None

  

        mock_create.return_value = MagicMock()
        mock_create.return_value.name = "Food"
        result = CategoryService.create_category(data)
        self.assertEqual(result.name, "Food")
        mock_create.assert_called_once_with(data)

    # 2. Missing Name
    def test_create_category_missing_name(self):

        with self.assertRaises(ValueError):
            CategoryService.create_category({"description": "Test"})

    # 3. Empty Name
    def test_create_category_empty_name(self):

        with self.assertRaises(ValueError):
            CategoryService.create_category({"name": "   ", "description": "Test"})

    # 4. Duplicate Category
    @patch("inventory3.services.category_service.CategoryRepository.get_all")
    def test_create_category_duplicate(self, mock_get_all):

        mock_get_all.return_value.filter.return_value.first.return_value = MagicMock()

        with self.assertRaises(ValueError):
            CategoryService.create_category({
                "name": "Food",
                "description": "Test"
            })

    # 5. Get All Categories
    @patch("inventory3.services.category_service.CategoryRepository.get_all")
    def test_get_all_categories(self, mock_get_all):

        mock_get_all.return_value = ["cat1", "cat2"]

        result = CategoryService.get_all_categories()

        self.assertEqual(len(result), 2)

    # 6. Update Category Success
    @patch("inventory3.services.category_service.CategoryRepository.update")
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_update_category_success(self, mock_get_by_id, mock_update):

        mock_get_by_id.return_value = MagicMock()

        updated = MagicMock()
        updated.name = "Updated"
        mock_update.return_value = updated

        result = CategoryService.update_category("id", {"name": "Updated"})

        self.assertEqual(result.name, "Updated")

    # 7. Update Category Not Found
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_update_category_not_found(self, mock_get_by_id):

        mock_get_by_id.return_value = None

        with self.assertRaises(ValueError):
            CategoryService.update_category("id", {"name": "Test"})

    # 8. Update Category Empty Name
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_update_category_empty_name(self, mock_get_by_id):

        mock_get_by_id.return_value = MagicMock()

        with self.assertRaises(ValueError):
            CategoryService.update_category("id", {"name": "   "})

    # 9. Delete Category Success
    @patch("inventory3.services.category_service.CategoryRepository.delete")
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_delete_category_success(self, mock_get_by_id, mock_delete):

        mock_get_by_id.return_value = MagicMock()

        CategoryService.delete_category("id")

        mock_delete.assert_called_once_with("id")

    # 10. Delete Category Not Found
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_delete_category_not_found(self, mock_get_by_id):

        mock_get_by_id.return_value = None

        with self.assertRaises(ValueError):
            CategoryService.delete_category("id")

    # 11. Get Products Success
    @patch("inventory3.services.category_service.ProductRepository.get_by_category")
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_get_products_success(self, mock_get_by_id, mock_get_products):

        category = MagicMock()
        mock_get_by_id.return_value = category
        mock_get_products.return_value = ["p1", "p2"]

        result = CategoryService.get_products("id")

        self.assertEqual(len(result), 2)

    # 12. Get Products Category Not Found
    @patch("inventory3.services.category_service.CategoryRepository.get_by_id")
    def test_get_products_category_not_found(self, mock_get_by_id):

        mock_get_by_id.return_value = None

        with self.assertRaises(ValueError):
            CategoryService.get_products("id")


class ProductServiceParameterizedTest(unittest.TestCase):

    # Invalid Inputs (name, brand_id)
    @parameterized.expand([
        ("missing_name", "", "507f1f77bcf86cd799439011"),
        ("missing_brand", "Shoes", ""),
        ("both_missing", None, None),
        ("empty_name", "   ", "507f1f77bcf86cd799439011"),
    ])
    def test_create_product_invalid_inputs(self, _, name, brand_id):

        with self.assertRaises(ValueError):
            ProductService.create_product({
                "name": name,
                "brand_id": brand_id
            })

    # Invalid ObjectId
    @parameterized.expand([
        ("invalid_id_1", "Shoes", "123"),
        ("invalid_id_2", "Shoes", "abc"),
    ])
    def test_invalid_brand_id(self, _, name, brand_id):

        with self.assertRaises(ValueError):
            ProductService.create_product({
                "name": name,
                "brand_id": brand_id
            })

    # Brand not found
    @parameterized.expand([
        ("valid_but_not_found", "Shoes", "507f1f77bcf86cd799439011"),
    ])
    @patch("inventory3.services.product_service.Brand.objects")
    def test_brand_not_found(self, _, name, brand_id, mock_brand):

        mock_brand.return_value.first.return_value = None

        with self.assertRaises(ValueError):
            ProductService.create_product({
                "name": name,
                "brand_id": brand_id
            })

    # Duplicate product
    @parameterized.expand([
        ("duplicate_case", "Shoes", "507f1f77bcf86cd799439011"),
    ])
    @patch("inventory3.services.product_service.Product.objects")
    @patch("inventory3.services.product_service.Brand.objects")
    def test_duplicate_product(self, _, name, brand_id, mock_brand, mock_product):

        mock_brand.return_value.first.return_value = MagicMock()
        mock_product.return_value.first.return_value = MagicMock()

        with self.assertRaises(ValueError):
            ProductService.create_product({
                "name": name,
                "brand_id": brand_id
            })


class CategoryServiceParameterizedTest(unittest.TestCase):

    # Invalid category names
    @parameterized.expand([
        ("empty_name", ""),
        ("spaces_only", "   "),
        ("none_name", None),
    ])
    def test_invalid_category_name(self, _, name):

        with self.assertRaises(ValueError):
            CategoryService.create_category({
                "name": name,
                "description": "Test"
            })

    # Duplicate category
    @parameterized.expand([
        ("duplicate_food", "Food"),
        ("duplicate_electronics", "Electronics"),
    ])
    @patch("inventory3.services.category_service.CategoryRepository.get_all")
    def test_duplicate_category(self, _, name, mock_get_all):

        mock_get_all.return_value.filter.return_value.first.return_value = MagicMock()

        with self.assertRaises(ValueError):
            CategoryService.create_category({
                "name": name,
                "description": "Test"
            })