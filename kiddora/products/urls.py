from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/', views.category_list_view, name='category_list'),
    path('products/', views.product_list_view, name='product_list'),
    path('subcategory/<int:subcategory_id>/', views.sub_category_view, name='subcategory_products'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
]
