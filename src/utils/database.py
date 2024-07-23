"""DuckDB utilities."""
import duckdb
from src.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DuckDBClient:
    """DuckDB client with S3 configuration."""
    
    def __init__(self):
        self.conn = None
    
    def __enter__(self):
        """Context manager entry."""
        self.conn = self._create_connection()
        return self.conn
