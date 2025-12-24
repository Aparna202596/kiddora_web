from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, ProductVariant

def get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    variant = get_object_or_404(ProductVariant, id=variant_id)

    if variant.stock < quantity:
        return JsonResponse({'error': 'Insufficient stock'}, status=400)

    cart = get_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': quantity}
    )

    if not created:
        if item.quantity + quantity > variant.stock:
            return JsonResponse({'error': 'Stock limit exceeded'}, status=400)
        item.quantity += quantity
        item.save()

    return JsonResponse({
        'success': True,
        'item_qty': item.quantity,
        'cart_count': cart.items.count()
    })

@login_required
def update_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity'))

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if quantity > item.variant.stock:
        return JsonResponse({'error': 'Insufficient stock'}, status=400)

    item.quantity = quantity
    item.save()

    return JsonResponse({'success': True})

@login_required
def remove_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    item_id = request.POST.get('item_id')
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()

    return JsonResponse({'success': True})
@login_required
def view_cart(request):
    cart = get_cart(request.user)
    items = cart.items.select_related('variant__product').all()

    cart_data = []
    for item in items:
        cart_data.append({
            'item_id': item.id,
            'product_name': item.variant.product.name,
            'variant_size': item.variant.size,
            'variant_color': item.variant.color,
            'quantity': item.quantity,
            'price_per_item': item.variant.price,
            'total_price': item.variant.price * item.quantity
        })
    return JsonResponse({'cart_items': cart_data})

@login_required
def clear_cart(request):
    cart = get_cart(request.user)
    cart.items.all().delete()
    return JsonResponse({'success': True})

@login_required

def cart_summary(request):
    cart = get_cart(request.user)
    total_items = sum(item.quantity for item in cart.items.all())
    total_price = sum(item.quantity * item.variant.price for item in cart.items.all())

    return JsonResponse({
        'total_items': total_items,
        'total_price': total_price
    })      

@login_required
def apply_coupon(request):  

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    coupon_code = request.POST.get('coupon_code')
    # Placeholder for coupon validation logic
    if coupon_code == "DISCOUNT10":
        discount = 10  # Example fixed discount
        return JsonResponse({'success': True, 'discount': discount})
    else:
        return JsonResponse({'error': 'Invalid coupon code'}, status=400)

@login_required
def remove_coupon(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Placeholder for coupon removal logic
    return JsonResponse({'success': True})

@login_required
def save_for_later(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    item_id = request.POST.get('item_id')
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # Placeholder for saving item for later logic
    item.delete()

    return JsonResponse({'success': True})

@login_required
def move_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Placeholder for moving saved item back to cart logic
    return JsonResponse({'success': True})

@login_required
def update_cart_item_quantity(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    item_id = request.POST.get('item_id')
    action = request.POST.get('action')  # 'increment' or 'decrement'

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == 'increment':
        if item.quantity < item.variant.stock:
            item.quantity += 1
            item.save()
        else:
            return JsonResponse({'error': 'Stock limit reached'}, status=400)
    elif action == 'decrement':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            return JsonResponse({'error': 'Minimum quantity is 1'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

    return JsonResponse({'success': True, 'new_quantity': item.quantity})

        