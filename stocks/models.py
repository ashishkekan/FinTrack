from django.contrib.auth.models import User
from django.db import models


class StockTransaction(models.Model):
    TRANSACTION_TYPES = (
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.stock_symbol} - {self.transaction_type} - {self.quantity} shares"
