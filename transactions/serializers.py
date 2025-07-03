from rest_framework import serializers
from .models import Transaction, TransactionItem
from inventory.models import Inventory


class TransactionItemSerializer(serializers.ModelSerializer):
    # product_id = serializers.PrimaryKeyRelatedField(
    #     source="product", queryset=TransactionItem.objects.all(), write_only=True
    # )
    # product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TransactionItem
        fields = "__all__"
        read_only_fields = ["transaction"]

    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        try:
            inventory = Inventory.objects.get(product=product)
            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough inventory for product {product.name}."
                )
        except Inventory.DoesNotExist:
            raise serializers.ValidationError(
                f"No inventory record found for product {product.name}."
            )
        return data


class TransactionSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True)

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["create_at", "performed_by"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        transaction = Transaction.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            inventory = Inventory.objects.get(product=product)

            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough inventory for product {product.name}."
                )
            TransactionItem.objects.create(
                transaction=transaction, product=product, quantity=quantity
            )

        return transaction
