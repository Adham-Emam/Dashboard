from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100, null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    barcode = models.CharField(max_length=13, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_barcode():
        import random

        while True:
            barcode = str(random.randint(1000000000000, 9999999999999))
            if not Product.objects.filter(barcode=barcode).exists():
                return barcode

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
