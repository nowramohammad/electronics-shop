from django.test import TestCase
from .models import Product

class ProductTests(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            price=19.99,
            image="products/images/test.jpg"
        )
        self.assertEqual(product.name, "Test Product")