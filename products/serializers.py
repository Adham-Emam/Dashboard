from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "discounted_price",
            "brand_name",
            "category",
            "barcode",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "barcode",
        ]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
            "price": {"required": True},
            "barcode": {"required": False, "allow_blank": True},
        }

        def validate(self, data):
            if data.get("discounted_price") is not None:
                discounted_price = data["discounted_price"]
                price = data["price"]
                if discounted_price >= price:
                    raise serializers.ValidationError(
                        "Discounted price must be lower than price"
                    )

                data["price"] = price - discounted_price

            if data.get("barcode") and len(data["barcode"]) != 13:
                raise serializers.ValidationError("Barcode must be 13 characters long")

            return data
