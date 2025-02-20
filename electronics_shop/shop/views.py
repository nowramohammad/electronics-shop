from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order, Cart
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.db import models

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
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
#this in for the home page
def home(request):
    products  = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})
#add to cart path
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

# creat the order path 
def create_order(request):
    # You can implement order creation logic here
    return HttpResponse("Order creation page")

#the detail prouduct page 
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

#cart page when login
@login_required
def cart(request):
    # Get the cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Filter CartItem objects based on the cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate the total price for each item
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    # Render the cart template with the cart items
    return render(request, 'shop/cart.html', {'cart_items': cart_items})


# when adding product to cart

# at the removal product from cart
@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, completed=False).first()
    return render(request, 'shop/cart.html', {'order': order})
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.products.set([item.product for item in cart.cartitem_set.all()])
    order.save()
    cart.cartitem_set.all().delete()  # Clear the cart
    return render(request, 'checkout.html', {'order': order})