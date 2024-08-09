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
                        SELECT
                            CAST(transaction_id AS VARCHAR) AS transaction_id,
                            CAST(customer_id AS BIGINT) AS customer_id,
                            CAST(product_id AS BIGINT) AS product_id,
                            CAST(quantity AS BIGINT) AS quantity,
                            unit_price,
                            total_amount,
                            CAST(transaction_timestamp AS TIMESTAMP) as transaction_timestamp,
                            payment_method,
                            CAST(store_id AS BIGINT) AS store_id,
                            status,
                            '{date_partition}' as partition_date,
                            CURRENT_TIMESTAMP as processed_at
                        FROM read_json_auto('{bronze_path}')
                    ),
                    cleaned_data AS (
                        SELECT *
                        FROM raw_data
                        WHERE 
                            -- Remove nulls in required fields
                            transaction_id IS NOT NULL
                            AND customer_id IS NOT NULL
                            AND product_id IS NOT NULL
                            AND transaction_timestamp IS NOT NULL
                            
                            -- Remove future timestamps
                            AND transaction_timestamp <= CURRENT_TIMESTAMP
                            
                            -- Remove zero/negative quantities
                            AND quantity > 0
                            
                            -- Remove negative amounts
                            AND total_amount > 0
                            
                            -- Remove mismatched totals (0.01 tolerance)
                            AND ABS(total_amount - (quantity * unit_price)) <= 0.01
                            
                            -- Valid payment methods
                            AND payment_method IN ('credit_card', 'debit_card', 'cash', 'digital_wallet')
                            
                            -- Valid statuses
                            AND status IN ('completed', 'pending', 'cancelled')
                            
                            -- Valid product ID range
                            AND product_id > 0 
                            AND product_id <= {self.num_products}
                    )
                    SELECT * FROM cleaned_data
                """).arrow()

            records_read = arrow_table.num_rows
            records_cleaned = records_read

            self.logger.info(
                f"âœ“ Cleaned data: {records_read} â†’ {records_cleaned} records "
                f"({records_read - records_cleaned} removed)"
            )

            silver_path = f"s3://{self.silver_bucket}/sales"
            arrow_to_write, duplicates_removed = self._deduplicate(
                arrow_table,
                silver_path
            )

            records_written = 0
            if arrow_to_write is not None and arrow_to_write.num_rows > 0:
                self._write_to_delta(arrow_to_write, silver_path)
                records_written = arrow_to_write.num_rows

                # Track metrics
                self._track_metrics(
                    layer='silver',
