"""Data quality validation using Soda Core."""
from typing import Dict, Any
from deltalake import DeltaTable
from deltalake.exceptions import TableNotFoundError

from src.processors.base_processor import BaseProcessor
from src.utils.database import DuckDBClient
from src.utils.metrics import track_quality_failure


class QualityChecker(BaseProcessor):
    """
    Quality checker processor - validates Silver data using Soda Core.
    Implements the same interface as other processors.
    """
    
    def _validate_config(self) -> None:
        """Validate quality checker configuration."""
        from src.config import get_config
        
        self.silver_bucket = self._get_bucket('silver')
        self.storage_options = self.storage.get_storage_options()
        self.checks_enabled = get_config('data_quality', 'enabled', default=True)
        self.checks_path = get_config('data_quality', 'checks_path')
        self.fail_on_error = get_config(
            'data_quality', 
            'fail_on_error', 
            default=False
        )
        
        if not self.checks_enabled:
            self.logger.info("Quality checks are DISABLED")
        else:
            self.logger.info(
                f"Quality checks enabled: checks_path={self.checks_path}, "
                f"fail_on_error={self.fail_on_error}"
