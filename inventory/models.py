from django.db import models
from products.models import Product


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "location")

    def __str__(self):
        return f"{self.product.name} - {self.location} ({self.quantity})"
