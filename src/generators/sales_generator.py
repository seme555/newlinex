"""Sales data generator with dirty data simulation."""
from faker import Faker
from faker_commerce import Provider
import random
from datetime import datetime, timedelta
from typing import List, Dict
from src.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SalesDataGenerator:
    """Generate synthetic sales data with realistic data quality issues."""

    def __init__(self):
        # Use different seed each time for variety
        self.fake = Faker()
        self.fake.add_provider(Provider)
        Faker.seed(int(datetime.utcnow().timestamp()))
        random.seed(int(datetime.utcnow().timestamp()))
        self.num_products = get_config('data_generation', 'num_products', default=50)
        self.num_customers = get_config('data_generation', 'num_customers', default=1000)
        self.num_stores = get_config('data_generation', 'num_stores', default=20)

    def generate_sales(self, num_records: int = None) -> List[Dict]:
        """Generate incremental sales transactions with realistic data quality issues."""
        if num_records is None:
            num_records = get_config('data_generation', 'sales_records_per_run', default=100)

        sales = []
        base_time = datetime.utcnow()

        for i in range(num_records):
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(10.0, 500.0), 2)

            # Base sale record
            sale = {
                "transaction_id": self.fake.uuid4(),  # Always unique
                "customer_id": int(random.randint(1, self.num_customers)),
                "product_id": random.randint(1, self.num_products),
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": round(quantity * unit_price, 2),
                "transaction_timestamp": (
                    base_time - timedelta(minutes=random.randint(0, 1440))  # Last 24 hours
                ).isoformat(),
                "payment_method": random.choice([
                    "credit_card", "debit_card", "cash", "digital_wallet"
                ]),
                "store_id": random.randint(1, self.num_stores),
                "status": random.choice(["completed", "pending", "cancelled"]),
            }
