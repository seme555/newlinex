"""Silver layer: Cleaned and deduplicated data in Delta Lake."""
from datetime import datetime
from typing import Dict, Any, Optional
import pyarrow as pa
import pyarrow.compute as pc
from deltalake import DeltaTable, write_deltalake
from deltalake.exceptions import TableNotFoundError

from src.processors.base_processor import BaseProcessor
from src.utils.database import DuckDBClient
from src.config import get_config


class SilverProcessor(BaseProcessor):
    """
    Silver layer processor - cleans, validates, and deduplicates data.
    Writes to Delta Lake for ACID transactions.
    """
    
    def _validate_config(self) -> None:
        """Validate Silver-specific configuration."""
        self.bronze_bucket = self._get_bucket('bronze')
        self.silver_bucket = self._get_bucket('silver')
        self.storage_options = self.storage.get_storage_options()
        self.num_products = get_config('data_generation', 'num_products', default=50)
        
        self.logger.info(
            f"Silver config: bronze={self.bronze_bucket}, "
            f"silver={self.silver_bucket}"
        )
    
    def process(self, bronze_key: str, **kwargs) -> Dict[str, Any]:
        """
        Process Bronze data to Silver Delta table.
        
        Args:
            bronze_key: S3 key of the Bronze data file
        
        Returns:
            {
                "records_read": int,
                "records_cleaned": int,
                "records_written": int,
                "duplicates_removed": int,
                "status": "success"
            }
        """
        try:
            date_partition = datetime.utcnow().strftime("%Y-%m-%d")
            bronze_path = f"s3://{self.bronze_bucket}/{bronze_key}"

            with DuckDBClient() as conn:
                arrow_table = conn.execute(f"""
                    WITH raw_data AS (
