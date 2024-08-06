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
