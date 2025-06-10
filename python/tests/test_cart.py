from unittest import TestCase

from model_objects import Product, ProductUnit
from shopping_cart import ShoppingCart


class TestCart(TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.apple = Product("apple", ProductUnit.KILO)
        self.brush = Product("brush", ProductUnit.EACH)

    def test_add_item_quantity(self):
        self.cart.add_item_quantity(self.apple, 2.5)
        self.assertEqual(1, len(self.cart.items))
        self.assertEqual(2.5, self.cart.product_quantities[self.apple])

    def test_add_multiple_items(self):
        self.cart.add_item_quantity(self.apple, 2.5)
        self.cart.add_item_quantity(self.brush, 1.0)
        self.assertEqual(2, len(self.cart.items))
        self.assertEqual(2.5, self.cart.product_quantities[self.apple])
        self.assertEqual(1, self.cart.product_quantities[self.brush])
    
    