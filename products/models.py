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

    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
