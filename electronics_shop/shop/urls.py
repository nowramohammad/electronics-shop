from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    #path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/', views.create_order, name='create_order'),
    #for the auth login logout path
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/add_feedback/', views.add_feedback, name='add_feedback'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('product/<int:product_id>/download/', views.download_image, name='download_image'),
    path('checkout/', views.checkout, name='checkout'),
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]