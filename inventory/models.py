from django.db import models
from products.models import Product


class Inventory(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product",)  #

    def __str__(self):
        return f"{self.product.name} - ({self.quantity})"
