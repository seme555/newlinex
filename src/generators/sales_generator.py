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
