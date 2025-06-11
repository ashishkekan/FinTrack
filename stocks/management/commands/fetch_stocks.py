import csv
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from stocks.models import StockTransaction


class Command(BaseCommand):
    help = "Import stock transactions from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            user = User.objects.get(id=2)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ User with id=2 does not exist."))
            return
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            created_count = 0
            for raw_row in reader:
                # Clean header keys and values
                row = {key.strip(): value.strip() for key, value in raw_row.items()}
                print(row)
                symbol = row["Stock symbol"].strip()
                price = float(row["Price per share"].strip())
                trans_type = row["Transaction Type"].strip().upper()
                quantity = int(row["Quantity"].strip())

                if trans_type not in dict(StockTransaction.TRANSACTION_TYPES):
                    self.stdout.write(
                        self.style.WARNING(f"⚠️ Invalid transaction type: {trans_type}")
                    )
                    continue

                StockTransaction.objects.create(
                    user=user,
                    stock_symbol=symbol,
                    price_per_share=price,
                    transaction_type=trans_type,
                    quantity=quantity,
                    transaction_date=datetime.now(),
                )
                created_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ {created_count} transactions imported successfully."
                )
            )
