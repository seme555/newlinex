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
