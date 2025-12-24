from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Wishlist, Product
from products.models import ProductVariant  

@login_required
def toggle_wishlist(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        wishlist.delete()
        return JsonResponse({'wishlisted': False})

    return JsonResponse({'wishlisted': True})

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    products = [item.product for item in wishlist_items]

    return JsonResponse({
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
            } for product in products
        ]
    })

