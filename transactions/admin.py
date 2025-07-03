from django.contrib import admin
from .models import Transaction, TransactionItem


class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 0
    readonly_fields = ("total_price",)

    def total_price(self, obj):
        return obj.quantity * obj.price

    total_price.short_description = "Total Price"


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "notes", "performed_by", "created_at"]
    search_fields = ["id", "performed_by__email"]
    list_filter = ["created_at", "performed_by__email"]
    inlines = [TransactionItemInline]


admin.site.register(Transaction, TransactionAdmin)
