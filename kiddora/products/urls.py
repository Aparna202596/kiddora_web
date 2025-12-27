from django.urls import path
from .views import (
    home_view,
    category_list_view,
    sub_category_view,
    product_list_view,
    product_detail_view
)

app_name = 'products'

urlpatterns = [
    path('', home_view, name='home'),
    path('categories/', category_list_view, name='category_list'),
    path('products/', product_list_view, name='product_list'),
    path('subcategory/<int:subcategory_id>/', sub_category_view, name='subcategory_products'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail'),
]
