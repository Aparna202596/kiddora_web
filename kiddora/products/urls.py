from django.urls import path
from . import views
from .views_cart import add_to_cart, update_cart, remove_from_cart
from .views_wishlist import toggle_wishlist

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.product_list, name='category_products'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/update/', update_cart, name='update_cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),

    # Wishlist
    path('wishlist/toggle/', toggle_wishlist, name='toggle_wishlist'),
]


