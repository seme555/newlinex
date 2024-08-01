"""Gold layer: Business aggregations as Delta tables with parallel processing."""
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import pyarrow as pa
import pyarrow.compute as pc
from deltalake import DeltaTable, write_deltalake
from deltalake.exceptions import TableNotFoundError

from src.processors.base_processor import BaseProcessor
from src.utils.database import DuckDBClient
from src.utils.metrics import track_table_size


class GoldProcessor(BaseProcessor):
    """
    Gold layer processor - creates business aggregations.
    Uses ThreadPoolExecutor for parallel table processing.
    """
    
    def _validate_config(self) -> None:
        """Validate Gold-specific configuration."""
        self.bronze_bucket = self._get_bucket('bronze')
        self.silver_bucket = self._get_bucket('silver')
        self.gold_bucket = self._get_bucket('gold')
        self.storage_options = self.storage.get_storage_options()
        
        self.logger.info(
            f"Gold config: bronze={self.bronze_bucket}, "
            f"silver={self.silver_bucket}, gold={self.gold_bucket}"
        )
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Create daily business metrics as Delta tables.
        Processes all aggregations in parallel using ThreadPoolExecutor.
        
        Returns:
            {
                "daily_sales_summary": {"status": "success", "rows": 1},
                "product_performance": {"status": "success", "rows": 50},
                "customer_segments": {"status": "success", "rows": 150},
                "overall_status": "success"
            }
        """
        try:
            date = datetime.utcnow().strftime("%Y-%m-%d")
            
            # Load Silver data once (shared across all aggregations)
            sales_df = self._load_silver_data()
            
            if sales_df is None or len(sales_df) == 0:
                self.logger.warning("No Silver data available, skipping aggregation")
                return {
