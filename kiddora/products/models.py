from django.db import models

# CATEGORY
class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'categories'
        ordering = ['category_name']

    def __str__(self):
        return self.category_name

# SUBCATEGORY
class Subcategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories')
    subcategory_name = models.CharField(max_length=100)
    class Meta:
        db_table = 'subcategories'
        unique_together = ('category', 'subcategory_name')
        ordering = ['subcategory_name']

    def __str__(self):
        return f"{self.category.category_name} → {self.subcategory_name}"

# PRODUCT
class Product(models.Model):
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='products')
    product_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(
        max_length=100,
        unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'products'
        ordering = ['product_name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active']),]

    def __str__(self):
        return self.product_name

# PRODUCT VARIANT
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants')
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    barcode = models.CharField(
        max_length=100,
        unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'product_variants'
        unique_together = ('product', 'color', 'size')
        indexes = [
            models.Index(fields=['barcode']),]
    def __str__(self):
        return f"{self.product.product_name} ({self.color}, {self.size})"
# INVENTORY
class Inventory(models.Model):
    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='inventory')
    quantity_available = models.PositiveIntegerField(default=0)
    quantity_reserved = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'inventory'

    def __str__(self):
        return f"{self.variant} | Available: {self.quantity_available}"

