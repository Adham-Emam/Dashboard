from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand_name",
        "price",
        "discounted_price",
        "barcode",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "brand_name", "is_active", "created_at")
    search_fields = ("name", "category", "brand_name", "barcode")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "category",
                    "brand_name",
                    "price",
                    "discounted_price",
                    "barcode",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )


admin.site.register(Product, ProductAdmin)
