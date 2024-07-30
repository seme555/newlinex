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
        self.logger.info(f"Bronze bucket: {self.bronze_bucket}")
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Ingest sales data to Bronze layer.
        
        Returns:
            {
                "key": "s3_key_path",
                "count": record_count,
                "timestamp": "2024-01-01T12:00:00"
            }
        """
        try:
            # Generate sales data (with intentional dirty data)
            sales_data = self.generator.generate_sales()
            
            if not sales_data:
                self.logger.warning("No sales data generated")
                return {"key": None, "count": 0, "status": "skipped"}
            
            # Create timestamped key for incremental loading
            timestamp = datetime.utcnow()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            key = f"sales/sales_{timestamp_str}.json"
            
            # Upload to Bronze (NO VALIDATION - accept dirty data)
            self.storage.upload_json(
                bucket=self.bronze_bucket,
                key=key,
                data=sales_data
            )
            
            # Track metrics
            self._track_metrics(
                layer='bronze',
