from unittest import TestCase
from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class TestSupermarket(TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.cart = ShoppingCart()

        # Products
        self.apple = Product("apple", ProductUnit.KILO)
        self.brush = Product("brush", ProductUnit.EACH)

        self.catalog.add_product(self.apple, 1.99)
        self.catalog.add_product(self.brush, 2.99)

    def test_empty_cart_zero_receipt(self):
        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(0, receipt.total_price())

    def test_one_product_in_cart_total_price(self):
        self.cart.add_item_quantity(self.apple, 2.5)

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(2.5 * 1.99, receipt.total_price())

    def test_multiple_products_in_cart_total_price(self):
        self.cart.add_item_quantity(self.apple, 2.5)
        self.cart.add_item_quantity(self.brush, 1.0)

        receipt = self.teller.checks_out_articles_from(self.cart)
        apple_total = 2.5 * 1.99
        brush_total = 1.0 * 2.99
        self.assertEqual(apple_total + brush_total, receipt.total_price())

    def test_ten_percent_discount(self):
        self.cart.add_item_quantity(self.apple, 2.5)
        self.teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.apple, 10.0
        )

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(2.5 * 1.99 * 0.9, receipt.total_price())

    # Fails - TODO: Fix Kilos/Decimal offer calculation
    def test_buy_three_for_two_in_kilos(self):
        self.cart.add_item_quantity(self.apple, 1)
        self.cart.add_item_quantity(self.apple, 1.5)
        self.cart.add_item_quantity(self.apple, 1)

        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.apple, 1)

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(2 * 1.99 +  (0.5 * 1.99), receipt.total_price())

    def test_buy_three_for_two_for_each(self):
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)

        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.brush, 1)

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(2 * 2.99, receipt.total_price())

    def test_buy_two_for_amount(self):
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)

        self.teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, self.brush, 1)

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(1, receipt.total_price())

    # Fails - TODO: Fix incorrect amount of sets
    def test_buy_two_for_amount_with_excess_products(self):
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)

        self.teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, self.brush, 1)

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(1 + 2.99, receipt.total_price())

    def test_buy_five_for_amount(self):
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)
        self.cart.add_item_quantity(self.brush, 1)

        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.brush, 5)

        receipt = self.teller.checks_out_articles_from(self.cart)
        self.assertEqual(5, receipt.total_price())