from django.test import TestCase
from .models import Product, Cart, CartItem, User

class ProductTests(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            price=19.99,
            image="products/images/test.jpg"
        )
        self.assertEqual(product.name, "Test Product")
class CartTestCase(TestCase):
    def test_add_item_to_cart(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        product = Product.objects.create(name='Test Product', price=10.00)
        cart = Cart.objects.create(user=user)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

        self.assertEqual(cart.cart_items.count(), 1)
        self.assertEqual(cart.cart_items.first().quantity, 2)