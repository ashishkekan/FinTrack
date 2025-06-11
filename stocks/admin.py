from django.contrib import admin

from .models import StockTransaction


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "stock_symbol",
        "transaction_type",
        "quantity",
        "price_per_share",
        "transaction_date",
    )
    list_filter = ("user", "stock_symbol", "transaction_type")
    search_fields = ("stock_symbol", "user__username")
    date_hierarchy = "transaction_date"
