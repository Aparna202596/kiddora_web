from django.shortcuts import render, get_object_or_404
from .models import Category, Subcategory, Product

def home_view(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).order_by('-id')[:8]

    return render(request, 'core/home.html', {
        'categories': categories,
        'products': products
    })

def category_list_view(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'products/category_list.html', {
        'categories': categories
    })

def sub_category_view(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    products = Product.objects.filter(
        subcategory=subcategory,
        is_active=True
    )

    return render(request, 'products/product_list.html', {
        'subcategory': subcategory,
        'products': products
    })

def product_list_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/product_list.html', {
        'products': products
    })
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    variants = product.variants.filter(is_active=True)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants
    })
