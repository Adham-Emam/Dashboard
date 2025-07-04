from django.contrib import admin
from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "product_name")
    list_filter = ("product",)
    search_fields = ("product__name",)
    autocomplete_fields = ("product",)

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Product Name"


admin.site.register(Inventory, InventoryAdmin)
