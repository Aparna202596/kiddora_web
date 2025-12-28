from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from core.decorators import admin_required
from accounts.models import CustomUser
from core.decorators import user_login_required
from orders.models import Order, OrderItem, Payment
from products.models import Category, Subcategory, Product

User = get_user_model()

def notlogged_home_view(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).order_by('-id')[:8]

    return render(request, 'core/notlogged_home.html', {
        'categories': categories,
        'products': products
    })

def aboutus_view(request):
    return render(request, 'core/about_us.html')

def contactus_view(request):
    return render(request, 'core/contact_us.html')

def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')

def terms_conditions_view(request):
    return render(request, 'core/terms_conditions.html')

def return_policy_view(request):
    return render(request, 'core/return_policy.html')

def cookie_policy_view(request):
    return render(request, 'core/cookie_policy.html')

def blog_view(request):
    return render(request, 'core/blog.html')

@user_login_required
def home_view(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).order_by('-id')[:8]

    return render(request, 'core/home.html', {
        'categories': categories,
        'products': products
    })

@login_required
@admin_required
def admin_dashboard_view(request):
    today = now()
    last_30_days = today - timedelta(days=30)
    previous_30_days = today - timedelta(days=60)
# TOTAL ORDERS
    total_orders = Order.objects.count()    
# TOTAL REVENUE / SALES
    total_revenue = Payment.objects.filter(     
        payment_status='SUCCESS').aggregate(
        total=Sum('order__final_amount'))['total'] or 0
# PRODUCTS SOLD
    products_sold = OrderItem.objects.aggregate(   
        total=Sum('quantity'))['total'] or 0
# NEW CUSTOMERS (LAST 30 DAYS)
    new_customers = CustomUser.objects.filter(   
        date_joined__gte=last_30_days).count()
# CUSTOMER GROWTH %
    current_users = CustomUser.objects.filter(
        date_joined__gte=last_30_days).count()
# PREVIOUS USERS (30-60 DAYS AGO)
    previous_users = CustomUser.objects.filter(
        date_joined__gte=previous_30_days,
        date_joined__lt=last_30_days).count()
    if previous_users > 0:
        customer_growth = round(
            ((current_users - previous_users) / previous_users) * 100, 2
        )
    else:
        customer_growth = 100 if current_users > 0 else 0
    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_sales": total_revenue,
        "products_sold": products_sold,
        "new_customers": new_customers,
        "customer_growth": customer_growth,
    }
    return render(request, "core/admin_dashboard.html", context)

@staff_member_required
def user_management_view(request):
    search_query = request.GET.get('q', '').strip()
    users = User.objects.all().order_by('-date_joined')
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query))
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'users': page_obj,
        'search_query': search_query
    }
    return render(request, 'admin_profile/customer_list.html', context)

@staff_member_required
def block_unblock_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.id == user.id:
        messages.error(request, "You cannot block your own account.")
        return redirect('accounts:admin_user_management')
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = "blocked" if not user.is_active else "unblocked"
        messages.success(request, f"User has been {status} successfully.")
    return redirect('accounts:admin_user_management')
