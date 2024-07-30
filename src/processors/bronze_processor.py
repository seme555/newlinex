"""Bronze layer: Raw data ingestion with no validation."""
from datetime import datetime
from typing import Dict, Any
from src.processors.base_processor import BaseProcessor
from src.generators.sales_generator import SalesDataGenerator
from src.models.schemas import Product, Customer


class BronzeProcessor(BaseProcessor):
    """
    Bronze layer processor - ingests raw data without validation.
    Accepts dirty data intentionally for downstream cleaning.
    """
    
    def _validate_config(self) -> None:
        """Validate Bronze-specific configuration."""
        self.bronze_bucket = self._get_bucket('bronze')
        self.generator = SalesDataGenerator()
