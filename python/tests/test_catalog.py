from unittest import TestCase

from model_objects import Product, ProductUnit
from tests.fake_catalog import FakeCatalog


class TestCatalog(TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()

        # Products
        self.apple = Product("apple", ProductUnit.KILO)
        self.brush = Product("brush", ProductUnit.EACH)

    def test_add_product_to_catalog(self):
        self.catalog.add_product(self.apple, 1.99)
        self.assertEqual(1, len(self.catalog.products))
        self.assertIn("apple", self.catalog.products)
        self.assertEqual(self.catalog.products['apple'].unit, ProductUnit.KILO)

    def test_two_products_in_catalog(self):
        self.catalog.add_product(self.apple, 1.99)
        self.catalog.add_product(self.brush, 2.99)
        
        self.assertEqual(2, len(self.catalog.products))
        self.assertIn("apple", self.catalog.products)
        self.assertIn("brush", self.catalog.products)
        self.assertEqual(self.catalog.products['apple'].unit, ProductUnit.KILO)
        self.assertEqual(self.catalog.products['brush'].unit, ProductUnit.EACH)
    
    def test_single_product_price(self):
        self.catalog.add_product(self.apple, 1.99)
        self.assertEqual(1.99, self.catalog.unit_price(self.apple))

    