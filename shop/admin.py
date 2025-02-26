from django.contrib import admin
from .models import Product
from .models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
# Register your models here.
