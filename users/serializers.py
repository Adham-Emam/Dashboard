from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "email": {
                "error_messages": {"unique": "This email is already registered."}
            },
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value
