from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator

def product_list(request, slug=None):
    products = Product.objects.filter(is_active=True)
    category = None

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'products/product_list.html', {
        'products': products,
        'category': category
    })
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': product.variants.all(),
        'images': product.images.all(),
        'reviews': product.reviews.all(),
    })