from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductVariant
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = ['Boys', 'Girls', 'Newborn']
        for c in categories:
            cat, _ = Category.objects.get_or_create(name=c)

            for i in range(1, 8):
                product = Product.objects.create(
                    category=cat,
                    name=f"{c} Product {i}",
                    description="Sample description",
                    base_price=random.randint(100, 500)
                )

                for size in ['XS','S','M','L','XL']:
                    for color in ['Red', 'Blue']:
                        ProductVariant.objects.create(
                            product=product,
                            size=size,
                            color=color,
                            price=product.base_price,
                            stock=random.randint(1, 20)
                        )

        self.stdout.write("Sample data created")
