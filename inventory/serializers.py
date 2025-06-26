from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Inventory
        fields = ["id", "product", "location", "quantity", "product_name"]
        read_only_fields = ["id", "product_name"]
        extra_kwargs = {
            "product": {"required": True},
            "location": {"required": True},
            "quantity": {"required": True, "min_value": 0},
        }

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
