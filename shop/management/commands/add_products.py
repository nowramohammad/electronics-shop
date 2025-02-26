from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Adds products with images and prices'

    def handle(self, *args, **kwargs):
        products_data = [
            {"name": "Product 1", "image": "products/images/IMG_1420.jpg", "price": 100.00},
            {"name": "Product 2", "image": "products/images/IMG_1421.jpg", "price": 120.00},
            {"name": "Product 3", "image": "products/images/IMG_1422.AVIF", "price": 150.00},
            {"name": "Product 4", "image": "products/images/IMG_1423.jpg", "price": 90.00},
        ]

        products = [Product(**product_data) for product_data in products_data]
        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS('Successfully added products'))
