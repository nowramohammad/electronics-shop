from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.http import FileResponse, Http404
from django.conf import settings
import os

def download_image(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        image_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
        
        # Check if file exists
        if not os.path.exists(image_path):
            raise Http404("Image not found.")
        
        # Serve the file as a downloadable response
        response = FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename={product.image.name}'
        return response
    except Product.DoesNotExist:
        raise Http404("Product not found.")
    
# to signup but not sure if it came first
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

#this in for the home page
def index(request):
    products  = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

#the detail prouduct page 
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

#cart page when login
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# when adding product to cart
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# at the removal product from cart
@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')

