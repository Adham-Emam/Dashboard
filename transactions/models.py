from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from products.models import Product
from inventory.models import Inventory

User = get_user_model()


class Transaction(models.Model):
    notes = models.TextField(blank=True, null=True)

    performed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.pk} by User {self.performed_by}"

    class Meta:
        ordering = ["-created_at"]


class TransactionItem(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        if not self.pk:  # only on create
            inventory = Inventory.objects.get(product=self.product)
            inventory.quantity -= self.quantity
            inventory.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        ordering = ["transaction__created_at", "product__name"]
