from django.db import models
from django.conf import settings
import uuid

# ORDER MODEL
class Order(models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders')

    address = models.ForeignKey(
        'accounts.UserAddress',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders')

    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING)

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)

    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status']),]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

# ORDER ITEM MODEL

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items')

    variant = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.CASCADE,
        related_name='order_items')

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'
        unique_together = ('order', 'variant')

    def __str__(self):
        return f"{self.order.id} - {self.variant} ({self.quantity})"

# PAYMENT MODEL

class Payment(models.Model):

    class PaymentMethod(models.TextChoices):
        CARD = 'CARD', 'Card'
        UPI = 'UPI', 'UPI'
        NETBANKING = 'NETBANKING', 'Net Banking'
        COD = 'COD', 'Cash on Delivery'
        WALLET = 'WALLET', 'Wallet'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment')

    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices)

    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False)

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING)

    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments'
        indexes = [
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id}"